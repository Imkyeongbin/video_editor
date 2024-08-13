import os
import subprocess

def build_ffmpeg_commands(trim_requests, concat_requests, upload_folder, final_filepath):
    commands = []

    # 트림 명령어 생성
    for trim in trim_requests:
        input_path = os.path.join(upload_folder, Video.query.get(trim.video_id).filename)
        output_path = f"{input_path}_trimmed.mp4"
        command = f"ffmpeg -i {input_path} -ss {trim.trim_start / 1000} -to {trim.trim_end / 1000} -c copy {output_path}"
        commands.append(command)

    # 이어 붙이기 명령어 생성
    if concat_requests:
        for concat in concat_requests:
            video_paths = [f"{os.path.join(upload_folder, Video.query.get(video_id).filename)}_trimmed.mp4" for video_id in concat.video_ids.split(',')]
            concat_file = "concat:" + "|".join(video_paths)
            command = f"ffmpeg -i '{concat_file}' -c copy {final_filepath}"
            commands.append(command)

    return commands

def execute_ffmpeg_commands(commands):
    for command in commands:
        subprocess.run(command, shell=True, check=True)
