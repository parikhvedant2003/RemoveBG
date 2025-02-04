import base64
import flet as ft
from flet import *
from flet.core.snack_bar import SnackBar
import shutil
from rembg import remove
import os


def main(page: Page):
    page.title = "Remove Background"
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 500
    page.window.height = 500
    # page.window_resizable = True
    page.padding = 10
    page.expand = True

    original_image = Image(visible=True, fit=ft.ImageFit.CONTAIN)
    processed_image = Image(visible=True, fit=ft.ImageFit.CONTAIN)
    image_container = Container(
        Row(
            [
                Container(
                    original_image, expand=1, border=ft.border.all(1, ft.Colors.BLACK)
                ),
                Container(
                    processed_image, expand=1, border=ft.border.all(1, ft.Colors.BLACK)
                ),
            ],
            expand=True,
        ),
        visible=False,
    )
    processed_data = None

    def after_upload(e: FilePickerResultEvent):
        nonlocal processed_data
        if not e.files:
            return
        file = e.files[0]
        with open(file.path, "rb") as f:
            img_data = f.read()
            original_image.src_base64 = base64.b64encode(img_data).decode("utf-8")
            # original_image.visible = True
            image_container.visible = True
            page.update()
            with open(
                "G:\\Projects\\Flet_Projects\\RemoveBG\\ComingSoon.png", "rb"
            ) as tf:
                img = tf.read()
                processed_image.src_base64 = base64.b64encode(img).decode("utf-8")
                # processed_image.visible = True
                image_container.visible = True
                page.update()

            processed_data = remove(img_data)
            processed_image.src_base64 = base64.b64encode(processed_data).decode(
                "utf-8"
            )
            # processed_image.visible = True
            image_container.visible = True
            download_button.visible = True

            page.update()
        shutil.copy(file.path, f"samples/{file.name}")

    def download_processed_image(e):
        if processed_data:
            with open("processed_image.png", "wb") as f:
                f.write(processed_data)
            page.snack_bar = SnackBar(Text("Processed image downloaded!"))
            page.snack_bar.open = True
            page.update()

    file_picker = ft.FilePicker(on_result=after_upload)
    page.overlay.append(file_picker)
    page.update()

    upload_button = ElevatedButton(
        text="Upload a file",
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False, file_type=FilePickerFileType.IMAGE
        ),
    )
    download_button = ElevatedButton(
        text="Download Processed Image",
        on_click=download_processed_image,
        visible=False,
    )

    button_row = Row(
        [upload_button, download_button], alignment=MainAxisAlignment.CENTER
    )

    page.add(button_row, image_container)


if __name__ == "__main__":
    ft.app(target=main)
