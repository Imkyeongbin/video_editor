import os
import subprocess
import platform
from models import Video

def build_ffmpeg_commands(trim_requests, concat_requests, upload_folder, final_filepath):
    commands = ['ls uploads']
    trimmed_videos = {}

    # 현재 운영체제를 판단
    is_windows = platform.system().lower() == 'windows'
    if is_windows:
        final_filepath = final_filepath.replace("\\", "/")

    # 트림 명령어 생성
    for trim in trim_requests:
        input_path = os.path.join(upload_folder, Video.query.get(trim.video_id).filename)
        if is_windows:
            input_path = input_path.replace("\\", "/")
        
        # 확장자를 분리하여 처리
        base_name, ext = os.path.splitext(input_path)
        output_path = f"{base_name}_trimmed{ext}"
        
        command = f'ffmpeg -i "{input_path}" -ss {trim.trim_start / 1000} -to {trim.trim_end / 1000} -c copy "{output_path}"'
        commands.append(command)
        
        # 트림된 파일 이름을 딕셔너리에 저장 (경로 제외)
        trimmed_videos[trim.video_id] = os.path.basename(output_path)

    # 이어 붙이기 명령어 생성
    if concat_requests:
        for concat in concat_requests:
            video_paths = []
            for video_id in concat.video_ids.split(','):
                if video_id in trimmed_videos:
                    video_paths.append(trimmed_videos[video_id])
                else:
                    video_paths.append(os.path.basename(Video.query.get(video_id).filename))
            
            # 파일 리스트를 텍스트 파일로 저장
            file_list_path = os.path.join(upload_folder, "file_list.txt")
            with open(file_list_path, 'w') as f:
                for path in video_paths:
                    
                    f.write(f"file '{path}'\n")
            if is_windows:
                file_list_path = file_list_path.replace("\\", "/")
            
            # ffmpeg 명령어 생성
            command = f'ffmpeg -f concat -safe 0 -i "{file_list_path}" -c copy "{final_filepath}"'
            commands.append(command)

    return commands

def execute_ffmpeg_commands(commands):
    for command in commands:
        subprocess.run(command, shell=True, check=True)
