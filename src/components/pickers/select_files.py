import flet as ft

def on_picked_file(e: ft.FilePickerResultEvent, files_list, page):
    if not e.files:
        return None, None, None
    
    files_list.controls.clear()
    
    video_name = [f.name.rsplit('.', 1)[0] for f in e.files]
    video_path = [f.path for f in e.files]
    
    for name in video_name:
        files_list.controls.append(ft.Text(f"{name} - Not converted"))

    page.update()

    return video_path, video_name, files_list

def folder(e: ft.FilePickerResultEvent, page, output_field):
    if not e.path:
        return None

    files_path = e.path
    output_field.value = files_path
    page.update()

    return files_path


def create_file_pickers(page, on_picked_file_callback, folder_callback):
    
    file_picker = ft.FilePicker(on_result=on_picked_file_callback)
    folder_picker = ft.FilePicker(on_result=folder_callback)
    
    page.overlay.append(file_picker)
    page.overlay.append(folder_picker)
    
    return file_picker, folder_picker