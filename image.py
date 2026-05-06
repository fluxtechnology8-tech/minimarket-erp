import flet as ft
import base64


async def main(page: ft.Page):
    page.title = "Cargar Imagen en Card"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    imagen_seleccionada = {"src": None, "name": None}

    cards_container = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    imagen_preview = ft.Image(
        src="https://placehold.co/1x1/transparent/transparent",
        width=200,
        height=200,
        fit=ft.BoxFit.CONTAIN,
        visible=False,
    )

    texto_imagen = ft.Text("No se ha seleccionado ninguna imagen")

    def _bytes_to_src(data: bytes, filename: str) -> str:
        ext = filename.rsplit(".", 1)[-1].lower()
        mime = {
            "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "png": "image/png", "gif": "image/gif",
            "webp": "image/webp", "bmp": "image/bmp",
        }.get(ext, "image/png")
        b64 = base64.b64encode(data).decode("utf-8")
        return f"data:{mime};base64,{b64}"

    async def seleccionar_imagen(e):
        # ✅ Nuevo patrón Flet 0.84: instanciar FilePicker directamente en el await
        files = await ft.FilePicker().pick_files(
            file_type=ft.FilePickerFileType.IMAGE,
            allow_multiple=False,
            with_data=True,
        )

        if not files:
            return

        archivo = files[0]
        data_uri = None

        if archivo.bytes:
            data_uri = _bytes_to_src(archivo.bytes, archivo.name)
        elif archivo.path:
            with open(archivo.path, "rb") as f:
                data_uri = _bytes_to_src(f.read(), archivo.name)

        if data_uri:
            imagen_seleccionada["src"] = data_uri
            imagen_seleccionada["name"] = archivo.name
            imagen_preview.src = data_uri
            imagen_preview.visible = True
            texto_imagen.value = f"Imagen: {archivo.name}"
        else:
            texto_imagen.value = "No se pudo cargar la imagen"

        page.update()

    def cerrar_dialogo(e):
        imagen_seleccionada["src"] = None
        imagen_seleccionada["name"] = None
        imagen_preview.src = "https://placehold.co/1x1/transparent/transparent"
        imagen_preview.visible = False
        texto_imagen.value = "No se ha seleccionado ninguna imagen"
        page.pop_dialog()
        page.update()

    async def guardar_imagen(e):
        if imagen_seleccionada["src"]:
            nuevo_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Image(
                                src=imagen_seleccionada["src"],
                                width=300,
                                height=300,
                                fit=ft.BoxFit.COVER,
                                border_radius=ft.BorderRadius(10, 10, 0, 0),
                            ),
                            ft.Container(
                                content=ft.Text(
                                    imagen_seleccionada["name"],
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                padding=10,
                            ),
                        ],
                        spacing=0,
                    ),
                    width=300,
                ),
                elevation=5,
            )
            cards_container.controls.append(nuevo_card)
            cerrar_dialogo(e)
        else:
            texto_imagen.value = "Por favor selecciona una imagen primero"
            page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Cargar Nueva Imagen"),
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Button(
                        "Seleccionar Imagen",
                        icon=ft.Icons.UPLOAD_FILE,
                        on_click=seleccionar_imagen,
                    ),
                    texto_imagen,
                    imagen_preview,
                ],
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=400,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.Button("Guardar", on_click=guardar_imagen),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def abrir_dialogo(e):
        page.show_dialog(dialog)

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=ft.Button(
                            "Agregar Imagen",
                            icon=ft.Icons.ADD_PHOTO_ALTERNATE,
                            on_click=abrir_dialogo,
                        ),
                        padding=20,
                    ),
                    ft.Divider(),
                    ft.Text("Imágenes Cargadas:", size=20, weight=ft.FontWeight.BOLD),
                    cards_container,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)