import flet as ft

def main(page: ft.Page):
    page.padding = 20

    path_field = ft.TextField(
        hint_text="/home/lorenzo/Video/Exported_video",
        read_only=True,
        border=ft.InputBorder.NONE,
        expand=True,
    )

    container = ft.Container(
        content=ft.Row(
            [
                path_field,
                ft.VerticalDivider(width=1),
                ft.IconButton(
                    icon=ft.Icons.FOLDER_OPEN,
                    tooltip="Seleccionar carpeta",
                ),
            ],
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        border=ft.border.all(1, ft.Colors.OUTLINE),
        border_radius=6,
        padding=ft.padding.symmetric(horizontal=8),
        height=48,
    )

    page.add(container)

ft.app(target=main)
