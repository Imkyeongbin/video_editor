import os
import asyncio
import subprocess
import multiprocessing
import platform
from models import Video

async def execute_command(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        print(f"Command failed: {command}")
        print(f"Error: {stderr.decode()}")
        raise subprocess.CalledProcessError(process.returncode, command)
    
    print(f"Command succeeded: {command}")
    return stdout, stderr

async def execute_ffmpeg_commands(commands):
    tasks = [execute_command(command) for command in commands]
    await asyncio.gather(*tasks)

def build_ffmpeg_commands(trim_requests, concat_requests, upload_folder, final_filepath):
    commands = []
    trimmed_videos = {}

    # 현재 운영체제를 판단
    is_windows = platform.system().lower() == 'windows'
    if is_windows:
        final_filepath = final_filepath.replace("\\", "/")

    # 현재 시스템의 CPU 코어 수에서 1을 뺀 값을 계산
    max_threads = max(1, multiprocessing.cpu_count() - 1)

    # 트림 명령어 생성
    for trim in trim_requests:
        input_path = os.path.join(upload_folder, Video.query.get(trim.video_id).filename)
        if is_windows:
            input_path = input_path.replace("\\", "/")
        
        # 확장자를 분리하여 처리
        base_name, ext = os.path.splitext(input_path)
        output_path = f"{base_name}_trimmed{ext}"
        
        # -threads 옵션을 max_threads로 설정
        command = f'ffmpeg -y -i "{input_path}" -ss {trim.trim_start / 1000} -to {trim.trim_end / 1000} -c copy -threads {max_threads} "{output_path}"'
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
            
            # -threads 옵션을 max_threads로 설정
            command = f'ffmpeg -y -f concat -safe 0 -i "{file_list_path}" -c copy -threads {max_threads} "{final_filepath}"'
            commands.append(command)

    return commands

# asyncio 작업을 위한 메인 함수
def process_videos_async(trim_requests, concat_requests, upload_folder, final_filepath):
    commands = build_ffmpeg_commands(trim_requests, concat_requests, upload_folder, final_filepath)
    try:
        asyncio.run(execute_ffmpeg_commands(commands))  # asyncio.run()으로 코루틴 실행
    except RuntimeError as e:
        print(f"Error: {e}")

