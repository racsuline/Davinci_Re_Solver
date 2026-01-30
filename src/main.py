import flet as ft

from components.pickers import select_files as sf
from components.conversions import convert_videos as cnv


def main(page: ft.Page):

    # Files Variables
    video_path = None
    files_path = None
    video_name = None
    files_list = ft.ListView(expand=True, spacing=5, auto_scroll=True)

    # Page Settings
    page.title = "Davinci Re-Solver for Linux"
    page.padding = 10
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE_ACCENT)

    # Functions
    def open_url():
        page.launch_url("https://codeberg.org/racsu/Davinci_Re-Solver")

    def update_suffix(e):
        nonlocal suffix
        suffix = suffix_field.value

    def update_output():
        nonlocal files_path
        if not output_field.value:
            return
        else:
            new_files_path = output_field.value
            if new_files_path:
                files_path = new_files_path
                page.update()
            return

    def on_picked_file(e):
        nonlocal video_path, video_name, files_list
        new_video_path, new_video_name, new_files_list = sf.on_picked_file(e, files_list, page)
        if new_video_path is not None:
            video_path = new_video_path
            video_name = new_video_name
            files_list = new_files_list

    def on_new_output(e):
        nonlocal files_path
        new_files_path = sf.folder(e, page, output_field)
        if new_files_path:
            files_path = new_files_path

    def convert_video():
        nonlocal files_list
        cnv.convert_video(video_path,video_name,files_path,progress_bar,progress_text,page,suffix,files_list)

    def file_clear():
        nonlocal files_list, video_path, video_name
        video_path = None
        video_name = None 
        files_list.controls.clear()
        progress_bar.value = 0
        progress_text.value = "No conversion is running yet"
        page.update()

    # CONTAINER FOR VIDEO LIST AND STATUS (Converted/Not Converted)
    loaded_videos = ft.Container(
        files_list,
        border=ft.border.all(1, ft.Colors.SURFACE_TINT),
        border_radius=8,
        height=200,
        width=400,
        bgcolor=ft.Colors.SURFACE,
        padding=10,
    )

    # Progress Bar, Text and Container
    progress_bar = ft.ProgressBar(value=0, visible=True, width=500)
    progress_text = ft.Text("No conversion is running yet", visible=True)

    progress_container = ft.Container(
        content=ft.Column(
            [ft.Text("Status:", size = 16), progress_text, progress_bar],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        border=ft.border.all(1, ft.Colors.SURFACE_TINT),
        border_radius=8,
        width=400,
        padding=10,
    )

    # File/Folder Pickers
    file_pick, folder_pick = sf.create_file_pickers(page, on_picked_file_callback=on_picked_file, folder_callback=on_new_output)

    # BUTTONS
    menu_button = ft.PopupMenuButton(
        tooltip="Main Menu",
        icon=ft.Icons.MENU,
        icon_color=ft.Colors.ON_SURFACE,
        items=[
            ft.PopupMenuItem(
                content=ft.Text(
                    "Codeberg Repo",
                    theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                    text_align=ft.TextAlign.CENTER,
                ),
                on_click=lambda e: open_url(),
            )
        ],
    )

    clear_files_button = ft.FilledButton(
        "Clear Files",
        icon=ft.Icons.DELETE,
        on_click = lambda e: file_clear(),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        scale = 1.25,
        tooltip="Clear all uploaded files",
        bgcolor=ft.Colors.ERROR,
    )

    file_selection_button = ft.FilledButton(
        "Upload Files",
        icon=ft.Icons.FILE_UPLOAD_SHARP,
        on_click=lambda _: file_pick.pick_files(
            allowed_extensions=["mp4","mov","avi","mkv","flv","webm","wmv","m4v"],
            allow_multiple=True,
            dialog_title="Select Video Files",
        ),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        scale = 1.25,
        tooltip="Select video files to convert",
    )

    start_conversions_button = ft.FilledButton(
        "Convert File",
        icon=ft.Icons.VIDEO_SETTINGS,
        on_click=lambda v: convert_video(),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        scale = 1.25
    )

    # OUTPUT DIRECTORY SELECTION
    output_selection_button = ft.IconButton(
        icon=ft.Icons.DRIVE_FOLDER_UPLOAD,
        on_click=lambda _: folder_pick.get_directory_path(
            dialog_title="Choose a folder to save the converted files"
        ),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        scale = 1,
        tooltip="Where converted videos will be saved",
    )

    output_field = ft.TextField(
        value="",
        hint_text="Select an Output Folder",
        on_change=lambda e: update_output(),
        width=350,
        border_color=ft.Colors.TRANSPARENT,
        border_radius = 0
    )

    output_container = ft.Container(
        content=ft.Row(
            [
                output_field,
                ft.VerticalDivider(width=1),
                output_selection_button,
            ],
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        border=ft.border.all(1, ft.Colors.SURFACE_TINT),
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=8),
        height=48,
        width=400,
    )

    # Suffix field
    suffix = ""

    suffix_field = ft.TextField(
        value="",
        label="Add a suffix to the converted file name",
        hint_text="_Example",
        on_change=lambda e: update_suffix(),
        width=400,
        border_color=ft.Colors.SURFACE_TINT,
        border_radius = 8
    )

    # LAYOUT
    page.add(
        ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    [
                        menu_button,
                        ft.Text(
                            "Convert your videos files and edit on Davinci Resolve!",
                            size=20,
                            weight="bold",  # type: ignore
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Column(
                    [
                        loaded_videos,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    [
                        output_container,
                        suffix_field,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                progress_container,
                ft.Divider(),
                ft.Container(
                    padding=10,
                    content=ft.SafeArea(
                        ft.Row(
                            [file_selection_button, start_conversions_button, clear_files_button],
                            alignment=ft.MainAxisAlignment.CENTER,
                            wrap=True,
                            spacing = 50
                        )
                    ),
                ),
            ],
        )
    )


ft.app(target=main)
