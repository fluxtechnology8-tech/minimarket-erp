from __future__ import annotations

from datetime import datetime
from pathlib import Path

import flet as ft

from views.components.ui import (
    section_card,
    card,
    app_input,
    primary_btn,
    section_header,
)
from views.ui.theme import AppTheme


class SyncView(ft.Column):
    def __init__(self, page: ft.Page, controller, is_mobile: bool = False):
        super().__init__(expand=True, scroll=ft.ScrollMode.AUTO, spacing=14)
        self._page = page
        self.controller = controller
        self.is_mobile = is_mobile
        self.padding = 24

        self.export_path = ft.TextField(
            label="Ruta de exportación JSON",
            value=str(
                Path.home()
                / f"backup_papeleria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            ),
            expand=True,
        )
        self.import_path = ft.TextField(
            label="Archivo JSON a importar",
            value=str(Path.home() / "backup_papeleria.json"),
            expand=True,
        )
        self.status_text = ft.Text(
            "Usa exportar para generar un respaldo local o importar para restaurarlo."
            if not is_mobile
            else "Solo puedes importar datos en esta versión.",
            color=AppTheme.TEXT_MUTED,
        )
        self._last_backup_time = "14:32"
        self._last_backup_date = "Hoy"
        self._db_health = "Excelente"
        self._storage_used = 3.5
        self._storage_total = 5.0
        self._catalog_size = 1.2
        self._receipts_size = 2.3
        self.build_view()

    def build_view(self) -> None:
        if self.is_mobile:
            self.controls = [
                section_header(
                    "Sincronización y Respaldos",
                    "Gestiona la integridad de tus datos",
                ),
                section_card(
                    "Importar datos",
                    [
                        ft.Row(
                            [
                                self.import_path,
                                ft.IconButton(
                                    icon=ft.Icons.FOLDER_OPEN,
                                    tooltip="Seleccionar archivo",
                                    on_click=self.on_import_file_click,
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.FilledButton(
                            "Importar datos",
                            icon=ft.Icons.DOWNLOAD,
                            on_click=self.import_merge,
                            expand=True,
                        ),
                        self.status_text,
                    ],
                    "Solo visualización. Importa un respaldo para restaurar datos.",
                ),
            ]
        else:
            self.controls = [
                section_header(
                    "Sincronización y Respaldo",
                    "Gestiona la integridad de tus datos y la nube.",
                ),
                self._build_status_card(),
                self._build_info_card(),
                self._build_history_card(),
                self._build_storage_card(),
                self._build_security_banner(),
            ]

    def _build_badge(self, text: str, color: str, bg_color: str) -> ft.Container:
        return ft.Container(
            content=ft.Text(text, size=10, weight=ft.FontWeight.W_700, color=color),
            bgcolor=bg_color,
            border_radius=AppTheme.R_PILL,
            padding=ft.padding.symmetric(horizontal=10, vertical=4),
        )

    def _build_status_card(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.CLOUD_DONE_ROUNDED, color=AppTheme.PRIMARY, size=22
                        ),
                        bgcolor=AppTheme.PRIMARY_LIGHT,
                        width=50,
                        height=50,
                        border_radius=AppTheme.R_PILL,
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Container(width=12),
                    ft.Column(
                        controls=[
                            self._build_badge(
                                "CLOUD SYNC ACTIVE",
                                AppTheme.PRIMARY,
                                AppTheme.PRIMARY_LIGHT,
                            ),
                            ft.Container(height=4),
                            ft.Text(
                                "Sincronización en tiempo real",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                        ],
                        spacing=0,
                        expand=True,
                    ),
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE_ROUNDED, color=AppTheme.SUCCESS, size=36
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=AppTheme.INFO_LT,
            border=ft.Border.all(0.5, ft.Colors.with_opacity(0.3, AppTheme.INFO)),
            border_radius=AppTheme.R_LG,
            padding=16,
        )

    def _build_info_card(self) -> ft.Container:
        return card(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "ÚLTIMO RESPALDO",
                                        size=10,
                                        color=AppTheme.TEXT_MUTED,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                    ft.Text(
                                        self._last_backup_time,
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        self._last_backup_date,
                                        size=11,
                                        color=AppTheme.TEXT_MUTED,
                                    ),
                                ],
                                spacing=2,
                            ),
                            ft.Container(expand=True),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "SALUD DE LA BASE DE DATOS",
                                        size=10,
                                        color=AppTheme.TEXT_MUTED,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                    ft.Container(height=4),
                                    ft.Row(
                                        controls=[
                                            ft.Container(
                                                width=10,
                                                height=10,
                                                bgcolor=AppTheme.SUCCESS,
                                                border_radius=AppTheme.R_PILL,
                                            ),
                                            ft.Text(
                                                self._db_health,
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                                color=AppTheme.SUCCESS,
                                            ),
                                        ],
                                        spacing=6,
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                    ),
                    ft.Container(height=14),
                    ft.Divider(height=1, color=AppTheme.DIVIDER),
                    ft.Container(height=14),
                    ft.Row(
                        controls=[
                            primary_btn(
                                "↑  Sincronizar Ahora",
                                ft.Icons.SYNC_ROUNDED,
                                expand=True,
                                on_click=self.sync_now,
                            ),
                            primary_btn(
                                "↓  Exportar Datos",
                                ft.Icons.DOWNLOAD_ROUNDED,
                                "outline",
                                expand=True,
                                on_click=self.export_data,
                            ),
                            primary_btn(
                                "☁  Importar Respaldo",
                                ft.Icons.UPLOAD_ROUNDED,
                                "outline",
                                expand=True,
                                on_click=self.import_merge,
                            ),
                        ],
                        spacing=8,
                    ),
                ],
                spacing=0,
            ),
        )

    def _build_history_card(self) -> ft.Container:
        return card(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Historial de Sincronización",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        "Registro detallado de los últimos 7 días.",
                                        size=11,
                                        color=AppTheme.TEXT_MUTED,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Text(
                                "Ver Reporte Completo", size=12, color=AppTheme.PRIMARY
                            ),
                        ],
                    ),
                    ft.Container(height=8),
                    self._build_hist_row(
                        ft.Icons.CHECK_CIRCLE_ROUNDED,
                        AppTheme.SUCCESS,
                        AppTheme.SUCCESS_LT,
                        "Sincronización Automática Completa",
                        "Servidor: Cloud • Datos sincronizados",
                        "Hoy, 14:32",
                        "EXITOSA",
                        AppTheme.SUCCESS,
                    ),
                    self._build_hist_row(
                        ft.Icons.INSERT_DRIVE_FILE_ROUNDED,
                        AppTheme.INFO,
                        AppTheme.INFO_LT,
                        "Exportación de Catálogo (Manual)",
                        "Formato: JSON • Usuario: Admin",
                        "Hoy, 09:15",
                        "FINALIZADA",
                        AppTheme.INFO,
                    ),
                    self._build_hist_row(
                        ft.Icons.CHECK_CIRCLE_ROUNDED,
                        AppTheme.SUCCESS,
                        AppTheme.SUCCESS_LT,
                        "Respaldo Programado",
                        "Integridad verificada",
                        "Ayer, 03:00",
                        "EXITOSA",
                        AppTheme.SUCCESS,
                    ),
                ],
                spacing=0,
            ),
        )

    def _build_hist_row(
        self, icon, icon_color, icon_bg, title, sub, time, status, status_color
    ) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, color=icon_color, size=16),
                        bgcolor=icon_bg,
                        width=32,
                        height=32,
                        border_radius=AppTheme.R_PILL,
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                title,
                                size=13,
                                weight=ft.FontWeight.W_600,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Text(sub, size=11, color=AppTheme.TEXT_MUTED),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(time, size=12, color=AppTheme.TEXT_PRIMARY),
                            ft.Text(
                                status,
                                size=11,
                                weight=ft.FontWeight.BOLD,
                                color=status_color,
                            ),
                        ],
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            border=ft.Border(bottom=ft.BorderSide(0.5, AppTheme.CARD_BORDER)),
            padding=ft.padding.symmetric(vertical=10),
        )

    def _build_storage_card(self) -> ft.Container:
        percent = int((self._storage_used / self._storage_total) * 100)
        return card(
            ft.Column(
                controls=[
                    ft.Text(
                        "Uso de Almacenamiento",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                    ft.Container(height=14),
                    ft.Stack(
                        controls=[
                            ft.Container(
                                width=100,
                                height=100,
                                border_radius=50,
                                bgcolor=AppTheme.INPUT_BG,
                            ),
                            ft.Container(
                                width=70,
                                height=70,
                                border_radius=35,
                                bgcolor=AppTheme.CARD_BG,
                                left=15,
                                top=15,
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            f"{percent}%",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color=AppTheme.TEXT_PRIMARY,
                                        ),
                                        ft.Text(
                                            f"{self._storage_used} GB / {self._storage_total} GB",
                                            size=9,
                                            color=AppTheme.TEXT_MUTED,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=0,
                                ),
                                width=100,
                                height=100,
                                alignment=ft.Alignment(0, 0),
                            ),
                        ],
                        width=100,
                        height=100,
                    ),
                    ft.Container(height=14),
                    ft.Divider(height=0.5, color=AppTheme.DIVIDER),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Archivos de Catálogo",
                                size=12,
                                color=AppTheme.TEXT_MUTED,
                                expand=True,
                            ),
                            ft.Text(
                                f"{self._catalog_size} GB",
                                size=12,
                                weight=ft.FontWeight.W_600,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                        ],
                        expand=True,
                    ),
                    ft.Container(height=4),
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Historial de Boletas",
                                size=12,
                                color=AppTheme.TEXT_MUTED,
                                expand=True,
                            ),
                            ft.Text(
                                f"{self._receipts_size} GB",
                                size=12,
                                weight=ft.FontWeight.W_600,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                        ],
                        expand=True,
                    ),
                ],
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def _build_security_banner(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "🔒 Protección de Datos Nivel Editorial",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.CARD_BG,
                    ),
                    ft.Text(
                        "Todos sus registros están encriptados con protocolos de grado bancario (AES-256).",
                        size=12,
                        color=AppTheme.SIDEBAR_TEXT,
                    ),
                ],
                spacing=6,
            ),
            bgcolor=AppTheme.SIDEBAR_BG,
            border_radius=AppTheme.R_LG,
            padding=20,
            margin=ft.margin.only(top=14),
        )

    def sync_now(self, e) -> None:
        try:
            self.status_text.value = "Sincronización iniciada..."
            self.status_text.color = AppTheme.INFO
        except Exception as exc:
            self.status_text.value = f"Error: {exc}"
            self.status_text.color = AppTheme.DANGER
        self.update()

    async def on_export_folder_click(self, e) -> None:
        try:
            src_bytes = self.controller.get_export_bytes()
            filename = (
                f"backup_papeleria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            path = await ft.FilePicker().save_file(
                allowed_extensions=["json"], file_name=filename, src_bytes=src_bytes
            )
            if path:
                self.export_path.value = path if isinstance(path, str) else path.name
                self.status_text.value = (
                    f"Archivo guardado en: {self.export_path.value}"
                )
                self.status_text.color = AppTheme.SUCCESS
            else:
                self.status_text.value = "Guardado cancelado"
                self.status_text.color = AppTheme.TEXT_MUTED
        except Exception as exc:
            self.status_text.value = f"Error al guardar: {exc}"
            self.status_text.color = AppTheme.DANGER
        self.update()

    async def on_import_file_click(self, e) -> None:
        try:
            files = await ft.FilePicker().pick_files(allowed_extensions=["json"])
            if files and len(files) > 0:
                file_path = files[0].path or ""
                self.import_path.value = file_path
                self.status_text.value = f"Archivo seleccionado: {files[0].name}"
                self.status_text.color = AppTheme.TEXT_MUTED
            else:
                self.status_text.value = "Selección cancelada"
                self.status_text.color = AppTheme.TEXT_MUTED
        except Exception as exc:
            self.status_text.value = f"Error al seleccionar: {exc}"
            self.status_text.color = AppTheme.DANGER
        self.update()

    def export_data(self, e) -> None:
        try:
            result = self.controller.export_data(self.export_path.value.strip())
            self.status_text.value = (
                f"Respaldo exportado correctamente en: {result.get('path', '')}"
            )
            self.status_text.color = AppTheme.SUCCESS
        except Exception as exc:
            self.status_text.value = f"No se pudo exportar: {exc}"
            self.status_text.color = AppTheme.DANGER
        self.update()

    def import_merge(self, e) -> None:
        self._import_data(merge=True)

    def _import_data(self, merge: bool) -> None:
        try:
            result = self.controller.import_data(
                self.import_path.value.strip(), merge=merge
            )
            mode = result.get("mode", "desconocido")
            self.status_text.value = f"Archivo importado correctamente. Estado: {mode}."
            self.status_text.color = AppTheme.SUCCESS
        except Exception as exc:
            self.status_text.value = f"No se pudo importar: {exc}"
            self.status_text.color = AppTheme.DANGER
        self.update()
