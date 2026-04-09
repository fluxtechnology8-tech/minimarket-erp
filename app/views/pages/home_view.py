import flet as ft
from app.controllers.product_controller import create_product

def home_view(page: ft.Page):

    input_name = ft.TextField(label="Nombre del producto")
    output_text = ft.Text("")

    def on_click(e):
        product = create_product(input_name.value)
        output_text.value = f"Producto creado: {product.name}"
        page.update()

    return ft.Column([
        ft.Text("Mini ERP", size=24),
        input_name,
        ft.ElevatedButton("Crear", on_click=on_click),
        output_text
    ])