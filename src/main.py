import flet as ft
from components.video import convert_video as cnv
from components.pickers import select_file as sf


def main(page: ft.Page):

    video_path = None
    files_path = None
    video_name = None
    name_list = ft.ListView(expand=True, spacing=5, auto_scroll=True)

    
    page.title = "Davinci Re-Solver for Linux"
    page.padding = 10
    page.theme_mode = ft.ThemeMode.SYSTEM

    
    output_directory = ft.Text("Output Folder: Not selected")

    # Suffix field

    suffix = ""

    suffix_field = ft.TextField(
        value = "",
        label = "Add a suffix to the converted file name",
        hint_text = "_Example",
        on_change = lambda e: update_suffix(),
        width = 400,
        border_color = ft.Colors.GREY_800
        )
    
    def open_url():
        page.launch_url('https://github.com/racsuline/Davinci_Re-Solver')

    def update_suffix():
        nonlocal suffix
        if not suffix_field.value:
            return
        else:
            suffix = suffix_field.value
            return
    
    def on_picked_file(e):
        nonlocal video_path, video_name, name_list
        video_path, video_name, name_list = sf.on_picked_file(e, name_list, page)

    def folder(e):
        nonlocal files_path
        files_path = sf.folder(e, output_directory, page)

    def convert_video():
        nonlocal name_list
        cnv.convert_video(video_path, video_name, files_path, progress_bar, progress_text, page, suffix, name_list)

    burger = ft.PopupMenuButton(
            tooltip = "Main Menu",
            icon = ft.Icons.MENU,
            icon_color = ft.Colors.ON_SURFACE,
            items = [
                ft.PopupMenuItem(
                    content = ft.Text("Github Repo", theme_style=ft.TextThemeStyle.LABEL_MEDIUM, text_align = ft.TextAlign.CENTER),
                    on_click = lambda e: open_url()
                )
            ]
        )
    
    # VIDEO LIST AND STATUS Converted/Not Converted

    loaded_videos = ft.Container(
        name_list,
        border = ft.border.all(1, ft.Colors.GREY_800),
        border_radius = 2,
        height = 200,
        width = 400,
        bgcolor = ft.Colors.GREY_800,
        padding = 10
    )


    # Progress Bar, Text and Container
    progress_bar = ft.ProgressBar(value=0, visible=True, width = 500)
    progress_text = ft.Text("No conversion is running yet", visible=True)

    progress_container = ft.Container(
        content = ft.Column(
            [
                ft.Text("Status"),
                progress_text,
                progress_bar
            ],
            alignment = ft.MainAxisAlignment.CENTER
        ),
        border = ft.border.all(1, ft.Colors.GREY_800),
        border_radius = 2,
        width = 400,
        padding = 10
    )

    # Pickers
    file_pick, folder_pick = sf.create_file_pickers(
        page, 
        on_picked_file_callback=on_picked_file,
        folder_callback=folder
    )

    # BUTTONS
    select_output = ft.FilledButton(
        "Output Folder",
        icon = ft.Icons.FOLDER,                                                        
        on_click = lambda _: folder_pick.get_directory_path(dialog_title = "Choose a folder to save the converted files"),
        color = ft.Colors.WHITE,
        style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),),
        bgcolor = ft.Colors.YELLOW_800,
        tooltip = "Where converted videos will be saved"
        
    )

    select_video = ft.FilledButton(
        "Upload Videos",
        icon = ft.Icons.UPLOAD_FILE_ROUNDED,
        on_click = lambda _: file_pick.pick_files(allowed_extensions = ["mp4", "mov", "avi", "mkv", "flv", "webm", "wmv", "m4v"], allow_multiple= True, dialog_title = "Select Video Files"),
        color = ft.Colors.WHITE,
        style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),),
        bgcolor = ft.Colors.RED_800,
        tooltip = "Select video files to convert"
    )

    start_converting = ft.FilledButton(
        "Convert File",
        icon = ft.Icons.VIDEO_CHAT,                                                    
        on_click = lambda v: convert_video(),
        color = ft.Colors.WHITE,
        style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),),
        bgcolor = ft.Colors.GREEN_800
        
    )

    # LAYOUT
    page.add(
        ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    [
                        burger,
                        ft.Text(
                            "Convert your videos to edit them on Davinci Resolve!",
                            size = 20,
                            weight = "bold" # type: ignore
                        ),
                    ],
                    alignment = ft.MainAxisAlignment.CENTER
                ),
                ft.Column(
                    [
                        ft.Text("Choose Files"),
                        loaded_videos
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                output_directory,
                ft.Row(
                    [
                        suffix_field,
                    ],
                    alignment = ft.MainAxisAlignment.CENTER
                ),
                progress_container,
                ft.Divider(),
                ft.Container(
                    padding=10,
                    content=ft.SafeArea(
                        ft.Row(
                            [
                                select_output,
                                select_video,
                                start_converting
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            wrap=True
                        )
                    )
                )
            ]
        )
    )


ft.app(target = main)
