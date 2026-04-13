from __future__ import annotations

from datetime import datetime
from pathlib import Path

import flet as ft

from views.components.ui import section_card, card, app_input, primary_btn
from views.ui.theme import AppTheme


class SyncView(ft.Column):
    def __init__(self, page: ft.Page, controller, is_mobile: bool = False):
        super().__init__(expand=True, scroll=ft.ScrollMode.AUTO, spacing=20)
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
        self.build_view()

    def build_view(self) -> None:
        if self.is_mobile:
            self.controls = [
                ft.Text(
                    "Sincronización y respaldos", size=28, weight=ft.FontWeight.BOLD
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
                ft.Text(
                    "Sincronización y Respaldos", size=28, weight=ft.FontWeight.BOLD
                ),
                self._build_sync_card(),
                self._build_history(),
            ]

    def _build_sync_card(self) -> ft.Container:
        return card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.SYNC_ROUNDED, color=AppTheme.PRIMARY, size=20
                            ),
                            ft.Text(
                                "Sincronización",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=16),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Última sincronización",
                                        size=12,
                                        color=AppTheme.TEXT_MUTED,
                                    ),
                                    ft.Text(
                                        "Hace 3 minutos",
                                        size=14,
                                        weight=ft.FontWeight.W_600,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                ],
                                spacing=2,
                            ),
                            ft.Container(expand=True),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Container(
                                            width=8,
                                            height=8,
                                            border_radius=4,
                                            bgcolor=AppTheme.SUCCESS,
                                        ),
                                        ft.Text(
                                            "Sincronizado",
                                            size=12,
                                            color=AppTheme.SUCCESS,
                                        ),
                                    ],
                                    spacing=8,
                                ),
                            ),
                        ]
                    ),
                    ft.Container(height=16),
                    ft.Divider(height=1, color=AppTheme.DIVIDER),
                    ft.Container(height=16),
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.CLOUD_DONE_ROUNDED,
                                color=AppTheme.PRIMARY,
                                size=18,
                            ),
                            ft.Text(
                                "Cloud Sync Activo",
                                size=13,
                                weight=ft.FontWeight.W_600,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                        ],
                        spacing=8,
                    ),
                ],
                spacing=0,
            ),
        )

    def _build_history(self) -> ft.Container:
        return card(
            ft.Column(
                [
                    ft.Text(
                        "Historial y Almacenamiento",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                    ft.Container(height=16),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Icon(
                                            ft.Icons.FOLDER_OPEN_ROUNDED,
                                            size=20,
                                            color=AppTheme.PRIMARY,
                                        ),
                                        ft.Text(
                                            "Exportar JSON",
                                            size=12,
                                            weight=ft.FontWeight.W_500,
                                            color=AppTheme.TEXT_PRIMARY,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                                width=80,
                                height=80,
                                bgcolor=AppTheme.INPUT_BG,
                                border_radius=AppTheme.R_MD,
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Copia de seguridad local",
                                        size=13,
                                        weight=ft.FontWeight.W_600,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        "Genera una copia completa de la base local",
                                        size=11,
                                        color=AppTheme.TEXT_MUTED,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            primary_btn(
                                "Exportar",
                                ft.Icons.UPLOAD_FILE,
                                on_click=self.export_data,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Container(height=12),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Icon(
                                            ft.Icons.DOWNLOAD_ROUNDED,
                                            size=20,
                                            color=AppTheme.INFO,
                                        ),
                                        ft.Text(
                                            "Importar",
                                            size=12,
                                            weight=ft.FontWeight.W_500,
                                            color=AppTheme.TEXT_PRIMARY,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                                width=80,
                                height=80,
                                bgcolor=AppTheme.INFO_LT,
                                border_radius=AppTheme.R_MD,
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Restaurar respaldo",
                                        size=13,
                                        weight=ft.FontWeight.W_600,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        "Importa un respaldo existente",
                                        size=11,
                                        color=AppTheme.TEXT_MUTED,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            primary_btn(
                                "Importar",
                                ft.Icons.DOWNLOAD,
                                variant="outline",
                                on_click=self.import_merge,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Container(height=12),
                    self.status_text,
                ],
                spacing=0,
            ),
        )

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
