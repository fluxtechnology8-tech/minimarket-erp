from __future__ import annotations

from datetime import datetime
from pathlib import Path

import flet as ft

from app.components.ui import section_card
from app.ui.theme import AppTheme


class SyncView(ft.Column):
    def __init__(self, page: ft.Page, db, is_mobile: bool = False):
        super().__init__(expand=True, scroll=ft.ScrollMode.AUTO, spacing=20)
        self._page = page
        self.db = db
        self.is_mobile = is_mobile
        self.padding = 20

        self.export_path = ft.TextField(
            label="Ruta de exportacion JSON",
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
            color=AppTheme.TEXT_SECONDARY,
        )

        self.build_view()

    def build_view(self) -> None:
        if self.is_mobile:
            self.controls = [
                ft.Text(
                    "Sincronizacion y respaldos", size=28, weight=ft.FontWeight.BOLD
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
                    "Sincronizacion y respaldos", size=28, weight=ft.FontWeight.BOLD
                ),
                section_card(
                    "Exportar datos",
                    [
                        ft.Row(
                            [
                                self.export_path,
                                ft.IconButton(
                                    icon=ft.Icons.FOLDER_OPEN,
                                    tooltip="Seleccionar ruta",
                                    on_click=self.on_export_folder_click,
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.FilledButton(
                            "Exportar JSON",
                            icon=ft.Icons.UPLOAD_FILE,
                            on_click=self.export_data,
                            expand=True,
                        ),
                    ],
                    "Genera una copia completa de la base local.",
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
                        ft.Row(
                            [
                                ft.FilledButton(
                                    "Importar y fusionar",
                                    icon=ft.Icons.DOWNLOAD,
                                    on_click=self.import_merge,
                                    expand=True,
                                ),
                                ft.OutlinedButton(
                                    "Reemplazar todo",
                                    icon=ft.Icons.WARNING_AMBER_ROUNDED,
                                    on_click=self.import_replace,
                                    expand=True,
                                ),
                            ],
                            spacing=8,
                        ),
                        self.status_text,
                    ],
                    "Importa un respaldo existente. Reemplazar sobrescribe los registros actuales.",
                ),
            ]

    async def on_export_folder_click(self, e) -> None:
        try:
            src_bytes = self.db.get_export_bytes()

            filename = (
                f"backup_papeleria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

            path = await ft.FilePicker().save_file(
                allowed_extensions=["json"],
                file_name=filename,
                src_bytes=src_bytes,
            )

            if path:
                self.export_path.value = path if isinstance(path, str) else path.name
                self.status_text.value = (
                    f"Archivo guardado en: {self.export_path.value}"
                )
                self.status_text.color = AppTheme.SUCCESS
            else:
                self.status_text.value = "Guardado cancelado"
                self.status_text.color = AppTheme.TEXT_SECONDARY
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
                self.status_text.color = AppTheme.TEXT_SECONDARY
            else:
                self.status_text.value = "Selección cancelada"
                self.status_text.color = AppTheme.TEXT_SECONDARY
        except Exception as exc:
            self.status_text.value = f"Error al seleccionar: {exc}"
            self.status_text.color = AppTheme.DANGER
        self.update()

    def export_data(self, e) -> None:
        try:
            path = self.db.export_data(self.export_path.value.strip())
            self.status_text.value = f"Respaldo exportado correctamente en: {path}"
            self.status_text.color = AppTheme.SUCCESS
        except Exception as exc:
            self.status_text.value = f"No se pudo exportar: {exc}"
            self.status_text.color = AppTheme.DANGER
        self.update()

    def import_merge(self, e) -> None:
        self._import_data(merge=True)

    def import_replace(self, e) -> None:
        self._import_data(merge=False)

    def _import_data(self, merge: bool) -> None:
        try:
            self.db.import_data(self.import_path.value.strip(), merge=merge)
            mode = "fusionado" if merge else "reemplazado"
            self.status_text.value = f"Archivo importado correctamente. Estado: {mode}."
            self.status_text.color = AppTheme.SUCCESS
        except Exception as exc:
            self.status_text.value = f"No se pudo importar: {exc}"
            self.status_text.color = AppTheme.DANGER
        self.update()
