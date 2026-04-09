import flet as ft
from app.views.pages.home_view import home_view

def main(page: ft.Page):
    page.title = "Minimarket ERP"
    page.window_width = 1000
    page.window_height = 700

    page.add(home_view(page))

ft.run(main)