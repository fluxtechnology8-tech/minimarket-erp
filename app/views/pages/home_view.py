import flet as ft
from controllers.product_controller import create_product

def home_view(page: ft.Page):

    input_name = ft.TextField(label="Nombre del producto")
    input_price = ft.TextField(label="Precio del producto")
    input_stock = ft.TextField(label="Stock del producto")

    def on_click(e):
        try:
            product = create_product(
                input_name.value,
                input_price.value,
                input_stock.value
            )

            # limpiar inputs
            input_name.value = ""
            input_price.value = ""
            input_stock.value = ""

            # feedback visual
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Producto '{product.name}' guardado")
            )
            page.snack_bar.open = True

        except Exception as err:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error: {str(err)}")
            )
            page.snack_bar.open = True

        page.update()

    return ft.Column([
        ft.Text("Mini ERP", size=24),
        input_name,
        input_price,
        input_stock,
        ft.ElevatedButton("Crear", on_click=on_click)
    ])