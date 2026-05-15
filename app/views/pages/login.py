from __future__ import annotations

import flet as ft
from views.ui.theme import AppTheme, LightPalette
from controllers.auth_controller import AuthController


class LoginView(ft.Container):
    def __init__(self, on_login_success, auth_controller: AuthController = None):
        super().__init__(expand=True, padding=0)
        self.on_login_success = on_login_success
        self.auth_controller = auth_controller or AuthController()
        self.username_field = ft.TextField(
            label="Usuario",
            prefix_icon=ft.Icons.PERSON,
            border_color=LightPalette.INPUT_BORDER,
            focused_border_color=LightPalette.PRIMARY,
            bgcolor=LightPalette.INPUT_BG,
            text_style=ft.TextStyle(size=14, color=LightPalette.TEXT_BODY),
            label_style=ft.TextStyle(color=LightPalette.TEXT_MUTED),
            width=320,
        )
        self.password_field = ft.TextField(
            label="Contraseña",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            border_color=LightPalette.INPUT_BORDER,
            focused_border_color=LightPalette.PRIMARY,
            bgcolor=LightPalette.INPUT_BG,
            text_style=ft.TextStyle(size=14, color=LightPalette.TEXT_BODY),
            label_style=ft.TextStyle(color=LightPalette.TEXT_MUTED),
            width=320,
            on_submit=self._handle_login,
        )
        self.error_text = ft.Text(
            "",
            size=12,
            color=LightPalette.ERROR,
            text_align=ft.TextAlign.CENTER,
            visible=False,
        )
        self.build_view()

    def build_view(self) -> None:
        self.bgcolor = LightPalette.PAGE_BG
        self.content = ft.Column(
            [
                ft.Container(
                    expand=True,
                    content=ft.Row(
                        [
                            ft.Container(
                                expand=1,
                                bgcolor=LightPalette.SIDEBAR_BG,
                                content=ft.Column(
                                    [
                                        ft.Container(height=80),
                                        ft.Icon(
                                            ft.Icons.STORE,
                                            size=80,
                                            color=ft.Colors.WHITE,
                                        ),
                                        ft.Container(height=20),
                                        ft.Text(
                                            "MINIMARKET ERP",
                                            size=28,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.WHITE,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        ft.Text(
                                            "Sistema de Gestión",
                                            size=14,
                                            color=LightPalette.SIDEBAR_TEXT,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ),
                            ft.Container(
                                expand=1,
                                content=ft.Column(
                                    [
                                        ft.Container(height=100),
                                        ft.Container(
                                            width=400,
                                            padding=40,
                                            bgcolor=LightPalette.CARD_BG,
                                            border_radius=ft.BorderRadius(
                                                top_left=20,
                                                top_right=20,
                                                bottom_left=20,
                                                bottom_right=20,
                                            ),
                                            shadow=[
                                                ft.BoxShadow(
                                                    blur_radius=20,
                                                    offset=ft.Offset(0, 4),
                                                    color=ft.Colors.with_opacity(
                                                        0.1, "#000000"
                                                    ),
                                                )
                                            ],
                                            content=ft.Column(
                                                [
                                                    ft.Container(
                                                        alignment=ft.Alignment(0, 0),
                                                        content=ft.Icon(
                                                            ft.Icons.ACCOUNT_CIRCLE,
                                                            size=60,
                                                            color=LightPalette.PRIMARY,
                                                        ),
                                                    ),
                                                    ft.Container(height=20),
                                                    ft.Text(
                                                        "Iniciar Sesión",
                                                        size=24,
                                                        weight=ft.FontWeight.BOLD,
                                                        color=LightPalette.TEXT_H,
                                                        text_align=ft.TextAlign.CENTER,
                                                    ),
                                                    ft.Text(
                                                        "Ingrese sus credenciales para continuar",
                                                        size=12,
                                                        color=LightPalette.TEXT_MUTED,
                                                        text_align=ft.TextAlign.CENTER,
                                                    ),
                                                    ft.Container(height=30),
                                                    self.username_field,
                                                    ft.Container(height=16),
                                                    self.password_field,
                                                    ft.Container(height=24),
                                                    self.error_text,
                                                    ft.Container(height=8),
                                                    ft.ElevatedButton(
                                                        content=ft.Text(
                                                            "INGRESAR",
                                                            size=14,
                                                            weight=ft.FontWeight.BOLD,
                                                            color=ft.Colors.WHITE,
                                                        ),
                                                        style=ft.ButtonStyle(
                                                            bgcolor=LightPalette.PRIMARY,
                                                            padding=15,
                                                        ),
                                                        width=320,
                                                        on_click=self._handle_login,
                                                    ),
                                                    ft.Container(height=30),
                                                    ft.Container(
                                                        padding=20,
                                                        bgcolor=LightPalette.PRIMARY_LIGHT,
                                                        border_radius=10,
                                                        content=ft.Column(
                                                            [
                                                                ft.Text(
                                                                    "Credenciales de prueba",
                                                                    size=11,
                                                                    weight=ft.FontWeight.BOLD,
                                                                    color=LightPalette.PRIMARY_DARK,
                                                                ),
                                                                ft.Text(
                                                                    "Admin: admin / admin123",
                                                                    size=10,
                                                                    color=LightPalette.PRIMARY_DARK,
                                                                ),
                                                                ft.Text(
                                                                    "Empleado: empleado / emp123",
                                                                    size=10,
                                                                    color=LightPalette.PRIMARY_DARK,
                                                                ),
                                                            ],
                                                            tight=True,
                                                            spacing=4,
                                                        ),
                                                    ),
                                                ],
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                spacing=0,
                                            ),
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ),
                        ],
                        expand=True,
                        spacing=0,
                    ),
                ),
            ],
            spacing=0,
            expand=True,
        )

    def _handle_login(self, e) -> None:
        username = self.username_field.value.strip()
        password = self.password_field.value.strip()

        if not username or not password:
            self.error_text.value = "Por favor ingrese usuario y contraseña"
            self.error_text.visible = True
            self.update()
            return

        try:
            usuario = self.auth_controller.login(username, password)

            if usuario:
                self.error_text.visible = False
                self.on_login_success(usuario)
            else:
                self.error_text.value = "Usuario o contraseña incorrectos"
                self.error_text.visible = True
                self.update()
        except ValueError as e:
            self.error_text.value = str(e)
            self.error_text.visible = True
            self.update()

    def update(self) -> None:
        if self.page:
            self.page.update()
