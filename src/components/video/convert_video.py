import subprocess
import threading
import flet as ft


def convert_thread(video_path, video_name, files_path, progress_bar, progress_text, page, suffix, name_list):
    if video_path is None:
        progress_text.value = "You need to select a file first"
        page.update()
        return
    
    if files_path is None:
        progress_text.value = "You need to select a folder first"
        page.update()
        return

    if files_path:
        try:
            progress_text.value = "Converting..."
            progress_bar.value = 0
            page.update()
            
            for path, name in zip(video_path, video_name):

                output_path = f"{files_path}/{name}{suffix}.mov"
                cmd = [
                    'ffmpeg',
                    '-y',
                    '-i', path,
                    '-c:v', 'dnxhd',
                    '-profile:v', 'dnxhr_hq',
                    '-pix_fmt', 'yuv422p',
                    '-c:a', 'pcm_s16le',
                    '-f', 'mov',
                    output_path
                ]

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )

                total_frames = None
                frame_count = 0

                for line in process.stderr:
                    if 'Duration' in line:
                        try:
                            time_str = line.split('Duration: ')[1].split(',')[0]
                            hours, minutes, seconds = map(float, time_str.split(':'))
                            total_frames = int((hours * 3600 + minutes * 60 + seconds) * 30)
                        except:
                            pass
                    
                    if 'frame=' in line:
                        try:
                            frame_str = line.split('frame=')[1].split()[0].strip()
                            frame_count = int(frame_str)
                            if total_frames:
                                progress = min(frame_count / total_frames, 1.0)
                                progress_bar.value = progress
                                progress_text.value = f"Converting {name} Progress: {progress * 100:.1f}%"
                                page.update()
                        except:
                            pass

                process.wait()
            
                if process.returncode == 0:
                    progress_text.value = "Video converted successfully!"
                    progress_bar.value = 1.0
                    progress_text.value = "Progress: 100%"

                    for control in name_list.controls:
                        if isinstance(control, ft.Text) and control.value.startswith(name):
                            control.value = f"{name} - Converted"
                            break

                    page.update()
                else:
                    progress_text.value = "An error occurred while converting the file"
            
            page.update()

        except Exception as e:
            progress_text.value = f"An error has occurred while converting the file: {e}"
            progress_bar.visible = False
            progress_text.visible = False
            page.update()

def convert_video(video_path, video_name, files_path, progress_bar, progress_text, page, suffix, name_list):
    thread = threading.Thread(target=convert_thread, args=(video_path, video_name, files_path, progress_bar, progress_text, page, suffix, name_list), daemon=True)
    thread.start()