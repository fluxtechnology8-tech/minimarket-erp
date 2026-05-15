"""
Minimarket ERP v3 — Estilo Papelería Pro
Con módulo Asistente IA integrado (Claude via Anthropic API)
"""

import flet as ft

import threading
from datetime import datetime


# ─────────────────────────────────────────────
# PALETA DE COLORES (Light / Dark)
# ─────────────────────────────────────────────
class LightTheme:
    PAGE_BG          = "#F1F5F9"
    SIDEBAR_BG       = "#1E3A8A"
    SIDEBAR_HOVER    = "#2563EB"
    SIDEBAR_SELECTED = "#2563EB"
    SIDEBAR_ITEM_SEL = "#FFFFFF1A"
    SIDEBAR_TEXT     = "#BFDBFE"
    SIDEBAR_TEXT_ACT = "#FFFFFF"
    SIDEBAR_ICON     = "#93C5FD"
    SIDEBAR_ICON_ACT = "#FFFFFF"
    SIDEBAR_LOGO_BG  = "#2563EB"
    TOPBAR_BG        = "#FFFFFF"
    TOPBAR_BORDER    = "#E2E8F0"
    CARD_BG          = "#FFFFFF"
    CARD_BORDER      = "#E2E8F0"
    TEXT_H           = "#0F172A"
    TEXT_BODY        = "#334155"
    TEXT_MUTED       = "#64748B"
    TEXT_DISABLED    = "#CBD5E1"
    PRIMARY          = "#2563EB"
    PRIMARY_DARK     = "#1D4ED8"
    PRIMARY_LIGHT    = "#DBEAFE"
    PRIMARY_MID      = "#3B82F6"
    ACCENT_CYAN      = "#06B6D4"
    SUCCESS          = "#059669"
    SUCCESS_LT       = "#D1FAE5"
    WARNING          = "#D97706"
    WARNING_LT       = "#FEF3C7"
    ERROR            = "#DC2626"
    ERROR_LT         = "#FEE2E2"
    INFO             = "#0284C7"
    INFO_LT          = "#E0F2FE"
    INPUT_BG         = "#F8FAFC"
    INPUT_BORDER     = "#CBD5E1"
    INPUT_FOCUSED    = "#2563EB"
    DIVIDER          = "#E2E8F0"
    R_SM             = 6
    R_MD             = 10
    R_LG             = 14
    R_XL             = 20
    R_PILL           = 999


class DarkTheme:
    PAGE_BG          = "#0F0E17"
    SIDEBAR_BG       = "#120F24"
    SIDEBAR_HOVER    = "#3730A3"
    SIDEBAR_SELECTED = "#4F46E5"
    SIDEBAR_ITEM_SEL = "#FFFFFF15"
    SIDEBAR_TEXT     = "#A5B4FC"
    SIDEBAR_TEXT_ACT = "#FFFFFF"
    SIDEBAR_ICON     = "#818CF8"
    SIDEBAR_ICON_ACT = "#FFFFFF"
    SIDEBAR_LOGO_BG  = "#4338CA"
    TOPBAR_BG        = "#1A1730"
    TOPBAR_BORDER    = "#2D2755"
    CARD_BG          = "#1C1A2E"
    CARD_BORDER      = "#2D2755"
    TEXT_H           = "#E0E7FF"
    TEXT_BODY        = "#C7D2FE"
    TEXT_MUTED       = "#6366F1"
    TEXT_DISABLED    = "#3730A3"
    PRIMARY          = "#4F46E5"
    PRIMARY_DARK     = "#4338CA"
    PRIMARY_LIGHT    = "#1E1B4B"
    PRIMARY_MID      = "#6366F1"
    ACCENT_CYAN      = "#22D3EE"
    SUCCESS          = "#10B981"
    SUCCESS_LT       = "#064E3B"
    WARNING          = "#F59E0B"
    WARNING_LT       = "#451A03"
    ERROR            = "#EF4444"
    ERROR_LT         = "#450A0A"
    INFO             = "#38BDF8"
    INFO_LT          = "#0C2340"
    INPUT_BG         = "#14112A"
    INPUT_BORDER     = "#312E81"
    INPUT_FOCUSED    = "#4F46E5"
    DIVIDER          = "#2D2755"
    R_SM             = 6
    R_MD             = 10
    R_LG             = 14
    R_XL             = 20
    R_PILL           = 999


T = LightTheme


def shadow(color: str, blur: int = 8, y: int = 2):
    return ft.BoxShadow(
        blur_radius=blur, offset=ft.Offset(0, y),
        color=ft.Colors.with_opacity(0.10, color), spread_radius=0
    )


# ─────────────────────────────────────────────
# COMPONENTES BASE
# ─────────────────────────────────────────────

def badge(text, color, bg):
    return ft.Container(
        content=ft.Text(text, size=10, weight=ft.FontWeight.W_700, color=color),
        bgcolor=bg,
        padding=ft.padding.symmetric(horizontal=8, vertical=3),
        border_radius=T.R_PILL,
    )


def card(content, padding=16):
    return ft.Container(
        content=content,
        bgcolor=T.CARD_BG,
        border_radius=T.R_LG,
        padding=padding,
        border=ft.Border.all(0.5, T.CARD_BORDER),
        shadow=shadow(T.PRIMARY, 6, 2),
    )


def section_header(title, subtitle=""):
    controls = [ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=T.TEXT_H)]
    if subtitle:
        controls.append(ft.Text(subtitle, size=13, color=T.TEXT_MUTED))
    return ft.Column(controls=controls, spacing=3)


def primary_btn(text, icon=None, variant="filled", on_click=None, expand=False):
    if variant == "filled":
        bg, fg, border = T.PRIMARY, "#FFFFFF", "transparent"
    elif variant == "outline":
        bg, fg, border = "transparent", T.PRIMARY, T.PRIMARY
    else:  # ghost
        bg, fg, border = T.PRIMARY_LIGHT, T.PRIMARY, "transparent"
    return ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(icon, color=fg, size=15)] + [ft.Text(text, size=12, weight=ft.FontWeight.W_600, color=fg)]
            if icon else [ft.Text(text, size=12, weight=ft.FontWeight.W_600, color=fg)],
            spacing=6, tight=True,
        ),
        bgcolor=bg,
        elevation=0,
        on_click=on_click,
        expand=expand,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=T.R_PILL),
            padding=ft.padding.symmetric(horizontal=16, vertical=10),
            side=ft.BorderSide(1, border),
        ),
    )


def app_input(label, value="", hint="", prefix_icon=None, keyboard_type=None,
              expand=False, width=None, on_change=None):
    return ft.TextField(
        label=label, value=value, hint_text=hint,
        prefix_icon=prefix_icon, keyboard_type=keyboard_type,
        expand=expand, width=width, on_change=on_change,
        border_radius=T.R_MD,
        border_color=T.INPUT_BORDER,
        focused_border_color=T.INPUT_FOCUSED,
        fill_color=T.INPUT_BG,
        filled=True,
        label_style=ft.TextStyle(color=T.TEXT_MUTED, size=12),
        content_padding=ft.padding.symmetric(horizontal=14, vertical=12),
    )


def searchbar(hint="Buscar...", on_change=None, expand=True):
    return ft.TextField(
        hint_text=hint,
        hint_style=ft.TextStyle(color=T.TEXT_DISABLED, size=13),
        prefix_icon=ft.Icons.SEARCH_ROUNDED,
        border_radius=T.R_PILL,
        border_color=T.INPUT_BORDER,
        focused_border_color=T.INPUT_FOCUSED,
        fill_color=T.INPUT_BG,
        filled=True,
        content_padding=ft.padding.symmetric(horizontal=18, vertical=10),
        on_change=on_change,
        expand=expand,
    )


def app_dropdown(label, value, options, width=None, expand=False):
    return ft.Dropdown(
        label=label, value=value,
        options=[ft.dropdown.Option(o) for o in options],
        width=width, expand=expand,
        border_radius=T.R_MD,
        border_color=T.INPUT_BORDER,
        focused_border_color=T.INPUT_FOCUSED,
        fill_color=T.INPUT_BG,
        filled=True,
        label_style=ft.TextStyle(color=T.TEXT_MUTED, size=12),
    )


# ─────────────────────────────────────────────
# TOPBAR
# ─────────────────────────────────────────────
class TopBar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.STOREFRONT_ROUNDED, color=T.PRIMARY, size=20),
                        ft.Column(
                            controls=[
                                ft.Text("Papelería Pro", size=14, weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                                ft.Text("Gestión de Inventario", size=10, color=T.TEXT_MUTED),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SEARCH_ROUNDED, color=T.TEXT_DISABLED, size=16),
                            ft.Text("Buscar productos, ventas o registros...",
                                    size=13, color=T.TEXT_DISABLED),
                        ],
                        spacing=8,
                    ),
                    bgcolor=T.INPUT_BG,
                    border=ft.Border.all(0.5, T.INPUT_BORDER),
                    border_radius=T.R_PILL,
                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                    width=320,
                ),
                ft.Container(expand=True),
                ft.Row(
                    controls=[
                        ft.Stack(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED, color=T.TEXT_MUTED, size=18),
                                    width=36, height=36, bgcolor=T.INPUT_BG,
                                    border=ft.Border.all(0.5, T.CARD_BORDER),
                                    border_radius=T.R_PILL,
                                    alignment=ft.Alignment(0, 0),
                                ),
                                ft.Container(
                                    width=9, height=9, bgcolor=T.ERROR,
                                    border_radius=T.R_PILL,
                                    right=2, top=2,
                                ),
                            ],
                            width=36, height=36,
                        ),
                        ft.Container(
                            content=ft.Icon(ft.Icons.SETTINGS_OUTLINED, color=T.TEXT_MUTED, size=18),
                            width=36, height=36, bgcolor=T.INPUT_BG,
                            border=ft.Border.all(0.5, T.CARD_BORDER),
                            border_radius=T.R_PILL,
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Text("AD", size=11, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                        bgcolor=T.PRIMARY, width=28, height=28,
                                        border_radius=T.R_PILL, alignment=ft.Alignment(0, 0),
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text("Admin Papelería", size=12, weight=ft.FontWeight.W_600, color=T.TEXT_H),
                                            ft.Text("Gerente de Tienda", size=10, color=T.TEXT_MUTED),
                                        ],
                                        spacing=0,
                                    ),
                                ],
                                spacing=8,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            bgcolor=T.INPUT_BG,
                            border=ft.Border.all(0.5, T.CARD_BORDER),
                            border_radius=T.R_PILL,
                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                        ),
                    ],
                    spacing=8,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.bgcolor = T.TOPBAR_BG
        self.padding = ft.padding.symmetric(horizontal=24, vertical=10)
        self.border = ft.Border(bottom=ft.BorderSide(0.5, T.TOPBAR_BORDER))
        self.shadow = shadow(T.TEXT_H, 4, 1)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
NAV_ITEMS = [
    ("Dashboard",      ft.Icons.DASHBOARD_OUTLINED,              "dashboard"),
    ("Catálogo",       ft.Icons.INVENTORY_2_OUTLINED,            "catalogo"),
    ("Kardex",         ft.Icons.SWAP_HORIZ_ROUNDED,              "kardex"),
    ("Gastos",         ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, "gastos"),
    ("Boletas",        ft.Icons.RECEIPT_LONG_OUTLINED,           "boletas"),
    ("Reportes",       ft.Icons.BAR_CHART_ROUNDED,               "reportes"),
    ("Asistente IA",   ft.Icons.SMART_TOY_OUTLINED,              "asistente"),
    ("Sincronización", ft.Icons.SYNC_ROUNDED,                    "sync"),
]


class Sidebar(ft.Container):
    def __init__(self, page, current_view, on_navigate, on_theme_toggle):
        super().__init__()
        self._page = page
        self._current = current_view
        self._navigate = on_navigate
        self._theme_toggle = on_theme_toggle
        self._expanded = True
        self._build()

    def _build(self):
        w = 210 if self._expanded else 64

        logo = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.STOREFRONT_ROUNDED, color="#FFFFFF", size=18),
                        bgcolor=T.SIDEBAR_LOGO_BG, width=36, height=36,
                        border_radius=T.R_MD, alignment=ft.Alignment(0, 0),
                    ),
                    *(
                        [ft.Column(
                            controls=[
                                ft.Text("Papelería Pro", color="#FFFFFF", size=13, weight=ft.FontWeight.BOLD),
                                ft.Text("GESTIÓN DE INVENTARIO", color=T.SIDEBAR_TEXT, size=9,
                                        weight=ft.FontWeight.W_600),
                            ],
                            spacing=0,
                        )]
                        if self._expanded else []
                    ),
                ],
                spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=14, vertical=14),
            border=ft.Border(bottom=ft.BorderSide(0.5, ft.Colors.with_opacity(0.1, "#FFFFFF"))),
        )

        items = []
        for label, icon, key in NAV_ITEMS:
            active = key == self._current
            icon_color = T.SIDEBAR_ICON_ACT if active else T.SIDEBAR_ICON
            text_color = T.SIDEBAR_TEXT_ACT if active else T.SIDEBAR_TEXT
            bg = ft.Colors.with_opacity(0.15, "#FFFFFF") if active else "transparent"

            # Special AI badge
            extra = []
            if key == "asistente" and self._expanded:
                extra = [
                    ft.Container(
                        content=ft.Text("IA", size=8, weight=ft.FontWeight.W_700, color="#FFFFFF"),
                        bgcolor=T.ACCENT_CYAN,
                        padding=ft.padding.symmetric(horizontal=5, vertical=1),
                        border_radius=T.R_PILL,
                    )
                ]

            row_ctrl = [
                ft.Container(
                    content=ft.Icon(icon, color=icon_color, size=18),
                    width=36, height=36,
                    border_radius=T.R_MD,
                    alignment=ft.Alignment(0, 0),
                ),
            ]
            if self._expanded:
                row_ctrl.append(
                    ft.Text(label, color=text_color, size=13,
                            weight=ft.FontWeight.W_700 if active else ft.FontWeight.W_400,
                            expand=True)
                )
                row_ctrl.extend(extra)

            left_accent = ft.Container(
                width=3, height=28,
                bgcolor=T.SIDEBAR_ICON_ACT if active else "transparent",
                border_radius=ft.BorderRadius(top_right=3, bottom_right=3,
                                              top_left=0, bottom_left=0),
            )

            item = ft.Container(
                content=ft.Row(
                    controls=[
                        left_accent,
                        ft.Container(
                            content=ft.Row(row_ctrl, spacing=10,
                                           vertical_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=bg,
                            border_radius=T.R_MD,
                            padding=ft.padding.symmetric(horizontal=8, vertical=6),
                            expand=True,
                            ink=True,
                            on_click=lambda e, k=key: self._navigate(k),
                        ),
                    ],
                    spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                margin=ft.margin.symmetric(vertical=1),
                animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            )
            items.append(item)

        user_row = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text("AP", size=11, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        bgcolor=T.SIDEBAR_LOGO_BG,
                        width=32, height=32,
                        border_radius=T.R_PILL,
                        alignment=ft.Alignment(0, 0),
                    ),
                    *(
                        [ft.Column(
                            controls=[
                                ft.Text("Admin Papelería", color="#FFFFFF", size=12,
                                        weight=ft.FontWeight.W_600),
                                ft.Text("Control Total", color=T.SIDEBAR_TEXT, size=10),
                            ],
                            spacing=0,
                        )]
                        if self._expanded else []
                    ),
                ],
                spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=10, vertical=10),
        )

        bottom_controls = [
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.DARK_MODE_ROUNDED if T == LightTheme else ft.Icons.LIGHT_MODE_ROUNDED,
                            color=T.SIDEBAR_TEXT, size=16,
                        ),
                        *(
                            [ft.Text(
                                "Modo oscuro" if T == LightTheme else "Modo claro",
                                color=T.SIDEBAR_TEXT, size=11,
                            )]
                            if self._expanded else []
                        ),
                    ],
                    spacing=8,
                ),
                padding=ft.padding.symmetric(horizontal=14, vertical=7),
                border_radius=T.R_MD,
                ink=True,
                on_click=lambda e: self._theme_toggle(),
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.MENU_OPEN_ROUNDED if self._expanded else ft.Icons.MENU_ROUNDED,
                            color=T.SIDEBAR_TEXT, size=16,
                        ),
                        *(
                            [ft.Text("Colapsar", color=T.SIDEBAR_TEXT, size=11)]
                            if self._expanded else []
                        ),
                    ],
                    spacing=8,
                ),
                padding=ft.padding.symmetric(horizontal=14, vertical=7),
                border_radius=T.R_MD,
                ink=True,
                on_click=self._toggle,
            ),
        ]

        self.content = ft.Column(
            controls=[
                logo,
                ft.Container(
                    content=ft.Column(controls=items, spacing=0),
                    padding=ft.padding.symmetric(horizontal=4, vertical=8),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Divider(height=0.5, color=ft.Colors.with_opacity(0.1, "#FFFFFF")),
                            user_row,
                            ft.Divider(height=0.5, color=ft.Colors.with_opacity(0.1, "#FFFFFF")),
                            ft.Container(
                                content=ft.Column(controls=bottom_controls, spacing=2),
                                padding=ft.padding.symmetric(horizontal=4, vertical=6),
                            ),
                        ],
                        spacing=0,
                    ),
                ),
            ],
            spacing=0, expand=True,
        )
        self.width = w
        self.bgcolor = T.SIDEBAR_BG
        self.animate = ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT)

    def _toggle(self, _=None):
        self._expanded = not self._expanded
        self._build()
        if self._page:
            self._page.update()

    def update_view(self, view):
        self._current = view
        self._build()
        if self._page:
            self._page.update()


# ─────────────────────────────────────────────
# VISTA: ASISTENTE IA  (nueva)
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """Eres el Asistente de Inteligencia Artificial de Papelería Pro, un ERP moderno para gestión de minimarkets y papelerías.

Tu rol es ayudar al administrador con:
- Consultas sobre inventario y stock de productos (cuadernos, bolígrafos, papel, tinta, etc.)
- Análisis de ventas y reportes del negocio
- Registro y seguimiento de gastos
- Gestión de proveedores y pedidos
- Consejos de optimización para la papelería
- Explicar cómo usar las funciones del sistema (Kardex, Boletas, Catálogo, etc.)

Contexto del negocio:
- Nombre: Papelería Pro
- Productos principales: útiles escolares, artículos de oficina, papelería fina, materiales de arte
- Moneda local: Soles peruanos (S/)
- El sistema tiene módulos de: Dashboard, Catálogo, Kardex, Gastos, Boletas, Reportes y Sincronización

Responde siempre en español, de forma amigable, concisa y profesional. 
Cuando des cifras o ejemplos, usa el contexto de una papelería peruana.
Si te preguntan sobre stock específico que no conoces, indícalo honestamente y sugiere revisar el módulo de Catálogo o Kardex."""


class AsistenteIAView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._messages = []          # [{role, content}]
        self._thinking = False

        # ── Área de mensajes ──
        self._chat_list = ft.ListView(
            expand=True,
            spacing=12,
            padding=ft.padding.symmetric(horizontal=4, vertical=8),
            auto_scroll=True,
        )

        # ── Input ──
        self._input = ft.TextField(
            hint_text="Escribe tu consulta aquí (ej: 'Muestra ventas de ayer')...",
            hint_style=ft.TextStyle(color=T.TEXT_DISABLED, size=13),
            border_radius=T.R_PILL,
            border_color=T.INPUT_BORDER,
            focused_border_color=T.INPUT_FOCUSED,
            fill_color=T.CARD_BG,
            filled=True,
            expand=True,
            multiline=False,
            content_padding=ft.padding.symmetric(horizontal=20, vertical=14),
            on_submit=self._on_send,
            text_style=ft.TextStyle(color=T.TEXT_H, size=13),
        )

        send_btn = ft.Container(
            content=ft.Icon(ft.Icons.SEND_ROUNDED, color="#FFFFFF", size=18),
            bgcolor=T.PRIMARY,
            width=46, height=46,
            border_radius=T.R_PILL,
            alignment=ft.Alignment(0, 0),
            ink=True,
            on_click=self._on_send,
            shadow=shadow(T.PRIMARY, 10, 3),
        )

        # ── Chips de acceso rápido ──
        quick_chips = ft.Row(
            controls=[
                self._chip("📦 Ver stock bajo", "¿Qué productos tienen stock bajo?"),
                self._chip("💰 Resumen de caja", "Dame un resumen de las ventas del día"),
                self._chip("📊 Margen de ganancia", "¿Cuál es el margen de ganancia promedio?"),
                self._chip("🔔 Alertas activas", "¿Cuáles son las alertas activas del sistema?"),
            ],
            wrap=True,
            spacing=8,
            run_spacing=8,
        )

        # ── Header del chat ──
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Stack(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(ft.Icons.SMART_TOY_ROUNDED,
                                                    color="#FFFFFF", size=20),
                                    bgcolor=T.PRIMARY,
                                    width=44, height=44,
                                    border_radius=T.R_PILL,
                                    alignment=ft.Alignment(0, 0),
                                ),
                                ft.Container(
                                    width=12, height=12,
                                    bgcolor=T.SUCCESS,
                                    border_radius=T.R_PILL,
                                    border=ft.Border.all(2, T.CARD_BG),
                                    right=0, bottom=0,
                                ),
                            ],
                            width=44, height=44,
                        ),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Asistente de Inteligencia Artificial",
                                    size=15, weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        width=7, height=7,
                                        bgcolor=T.SUCCESS,
                                        border_radius=T.R_PILL,
                                    ),
                                    ft.Text("En línea • Papelería Pro IA",
                                            size=11, color=T.TEXT_MUTED),
                                ],
                                spacing=5,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED,
                                                    color=T.TEXT_MUTED, size=16),
                                    width=34, height=34,
                                    bgcolor=T.INPUT_BG,
                                    border=ft.Border.all(0.5, T.CARD_BORDER),
                                    border_radius=T.R_PILL,
                                    alignment=ft.Alignment(0, 0),
                                    ink=True,
                                    on_click=self._clear_chat,
                                    tooltip="Limpiar conversación",
                                ),
                            ],
                            spacing=8,
                        ),
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=T.CARD_BG,
            border=ft.Border(bottom=ft.BorderSide(0.5, T.CARD_BORDER)),
            padding=ft.padding.symmetric(horizontal=20, vertical=14),
            border_radius=ft.BorderRadius(T.R_LG, T.R_LG, 0, 0),
        )

        # Footer del input
        footer_bar = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            self._input,
                            ft.Container(width=8),
                            send_btn,
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=6),
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.LOCK_OUTLINE_ROUNDED,
                                            color=T.TEXT_DISABLED, size=12),
                                    ft.Text("Encriptación de extremo a extremo",
                                            size=10, color=T.TEXT_DISABLED),
                                ],
                                spacing=4,
                            ),
                            ft.Container(width=14),
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.HISTORY_ROUNDED,
                                            color=T.TEXT_DISABLED, size=12),
                                    ft.Text("Historial guardado",
                                            size=10, color=T.TEXT_DISABLED),
                                ],
                                spacing=4,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=0,
            ),
            bgcolor=T.CARD_BG,
            border=ft.Border(top=ft.BorderSide(0.5, T.CARD_BORDER)),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            border_radius=ft.BorderRadius(0, 0, T.R_LG, T.R_LG),
        )

        # Sidebar derecho con info y chips
        right_panel = ft.Container(
            content=ft.Column(
                controls=[
                    card(ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.BOLT_ROUNDED, color=T.WARNING, size=16),
                                    ft.Text("Accesos Rápidos", size=13,
                                            weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                                ],
                                spacing=6,
                            ),
                            ft.Container(height=10),
                            quick_chips,
                        ],
                    )),
                    ft.Container(height=12),
                    card(ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED,
                                            color=T.INFO, size=16),
                                    ft.Text("Capacidades IA", size=13,
                                            weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                                ],
                                spacing=6,
                            ),
                            ft.Container(height=10),
                            *[self._capability_row(icon, label) for icon, label in [
                                ("📦", "Consulta de inventario en tiempo real"),
                                ("📊", "Análisis de ventas y reportes"),
                                ("💸", "Seguimiento de gastos"),
                                ("🛒", "Gestión de proveedores"),
                                ("💡", "Consejos de optimización"),
                                ("🔔", "Alertas y notificaciones"),
                            ]],
                        ],
                        spacing=0,
                    )),
                    ft.Container(height=12),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Impulsado por", size=10,
                                        color=ft.Colors.with_opacity(0.6, "#FFFFFF"),
                                        weight=ft.FontWeight.W_600),
                                ft.Text("Claude AI", size=16,
                                        color="#FFFFFF",
                                        weight=ft.FontWeight.BOLD),
                                ft.Text("Anthropic", size=10,
                                        color=ft.Colors.with_opacity(0.7, "#FFFFFF")),
                            ],
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor=T.SIDEBAR_BG,
                        border_radius=T.R_LG,
                        padding=ft.padding.symmetric(horizontal=16, vertical=14),
                        alignment=ft.Alignment(0, 0),
                    ),
                ],
                spacing=0,
            ),
            width=250,
        )

        # Layout principal del chat
        chat_area = ft.Container(
            content=ft.Column(
                controls=[
                    header,
                    ft.Container(
                        content=self._chat_list,
                        expand=True,
                        bgcolor=T.PAGE_BG,
                        padding=ft.padding.symmetric(horizontal=16, vertical=8),
                    ),
                    footer_bar,
                ],
                spacing=0,
                expand=True,
            ),
            expand=True,
            border_radius=T.R_LG,
            border=ft.Border.all(0.5, T.CARD_BORDER),
            shadow=shadow(T.PRIMARY, 8, 2),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        section_header("Asistente de IA",
                                       "Consulta, analiza y gestiona tu papelería con inteligencia artificial."),
                        ft.Container(expand=True),
                        badge("CLAUDE AI", T.PRIMARY, T.PRIMARY_LIGHT),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=16),
                ft.Row(
                    controls=[
                        chat_area,
                        ft.Container(width=14),
                        right_panel,
                    ],
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            expand=True,
        )
        self.padding = 24
        self.expand = True
        self.bgcolor = T.PAGE_BG

        # Mensaje de bienvenida
        self._add_ai_bubble(
            "¡Hola! Soy tu asistente de **Papelería Pro**. Estoy aquí para ayudarte a gestionar "
            "tu negocio de forma eficiente.\n\n"
            "¿Te gustaría consultar el stock actual, revisar el reporte de ventas del día "
            "o quizás necesitas ayuda para registrar un nuevo proveedor?"
        )

    # ── helpers de UI ──

    def _chip(self, label, query):
        return ft.Container(
            content=ft.Text(label, size=11, color=T.PRIMARY, weight=ft.FontWeight.W_600),
            bgcolor=T.PRIMARY_LIGHT,
            border=ft.Border.all(0.5, ft.Colors.with_opacity(0.4, T.PRIMARY)),
            border_radius=T.R_PILL,
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            ink=True,
            on_click=lambda e, q=query: self._quick_send(q),
        )

    def _capability_row(self, icon, label):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(icon, size=14),
                    ft.Text(label, size=11, color=T.TEXT_BODY, expand=True),
                ],
                spacing=8,
            ),
            padding=ft.padding.symmetric(vertical=4),
        )

    def _add_user_bubble(self, text: str):
        now = datetime.now().strftime("%I:%M %p")
        bubble = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(expand=True),
                            ft.Container(
                                content=ft.Text(text, size=13, color="#FFFFFF",
                                                selectable=True),
                                bgcolor=T.PRIMARY,
                                border_radius=ft.BorderRadius(T.R_LG, T.R_LG, 4, T.R_LG),
                                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                                shadow=shadow(T.PRIMARY, 6, 2),
                            ),
                            ft.Container(
                                content=ft.Icon(ft.Icons.PERSON_ROUNDED,
                                                color=T.TEXT_MUTED, size=16),
                                bgcolor=T.INPUT_BG,
                                border=ft.Border.all(0.5, T.CARD_BORDER),
                                width=32, height=32,
                                border_radius=T.R_PILL,
                                alignment=ft.Alignment(0, 0),
                            ),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(expand=True),
                            ft.Text(f"Enviado a las {now}", size=10, color=T.TEXT_DISABLED),
                            ft.Container(width=42),
                        ],
                    ),
                ],
                spacing=4,
            ),
        )
        self._chat_list.controls.append(bubble)

    def _add_ai_bubble(self, text: str, thinking=False):
        if thinking:
            content_widget = ft.Row(
                controls=[
                    ft.ProgressRing(width=14, height=14, stroke_width=2, color=T.PRIMARY),
                    ft.Text("Consultando inventario en tiempo real...",
                            size=12, color=T.TEXT_MUTED, italic=True),
                ],
                spacing=10,
            )
        else:
            # Render markdown-lite: bold (**text**)
            parts = []
            segments = text.split("**")
            for i, seg in enumerate(segments):
                if seg:
                    parts.append(ft.TextSpan(
                        text=seg,
                        style=ft.TextStyle(
                            weight=ft.FontWeight.BOLD if i % 2 == 1 else ft.FontWeight.NORMAL,
                            size=13,
                            color=T.TEXT_H,
                        ),
                    ))
            content_widget = ft.Text(spans=parts, selectable=True)

        bubble = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.SMART_TOY_ROUNDED, color="#FFFFFF", size=16),
                        bgcolor=T.PRIMARY,
                        width=32, height=32,
                        border_radius=T.R_PILL,
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Container(
                        content=content_widget,
                        bgcolor=T.CARD_BG,
                        border_radius=ft.BorderRadius(4, T.R_LG, T.R_LG, T.R_LG),
                        padding=ft.padding.symmetric(horizontal=16, vertical=12),
                        border=ft.Border.all(0.5, T.CARD_BORDER),
                        shadow=shadow(T.TEXT_H, 4, 1),
                        expand=True,
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            data="thinking" if thinking else "message",
        )
        self._chat_list.controls.append(bubble)
        return bubble

    def _remove_thinking(self):
        self._chat_list.controls = [
            c for c in self._chat_list.controls
            if getattr(c, "data", None) != "thinking"
        ]

    def _quick_send(self, query: str):
        self._input.value = query
        if self._page:
            self._page.update()
        self._on_send(None)

    def _clear_chat(self, _=None):
        self._messages.clear()
        self._chat_list.controls.clear()
        self._add_ai_bubble(
            "Conversación reiniciada. ¿En qué puedo ayudarte con **Papelería Pro**?"
        )
        if self._page:
            self._page.update()

    def _on_send(self, _):
        text = (self._input.value or "").strip()
        if not text or self._thinking:
            return

        self._thinking = True
        self._input.value = ""
        self._input.disabled = True

        # Add user bubble
        self._add_user_bubble(text)
        thinking_bubble = self._add_ai_bubble("", thinking=True)

        if self._page:
            self._page.update()

        # Build messages for API
        self._messages.append({"role": "user", "content": text})

        def call_api():
            try:
                client = anthropic.Anthropic()
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    messages=self._messages,
                )
                ai_text = response.content[0].text
                self._messages.append({"role": "assistant", "content": ai_text})

                def update_ui():
                    self._remove_thinking()
                    self._add_ai_bubble(ai_text)
                    self._thinking = False
                    self._input.disabled = False
                    if self._page:
                        self._page.update()

                if self._page:
                    self._page.run_task(update_ui) if hasattr(self._page, "run_task") else update_ui()

            except Exception as exc:
                err_msg = f"⚠️ Error al conectar con la IA: {str(exc)[:120]}"

                def update_err():
                    self._remove_thinking()
                    self._add_ai_bubble(err_msg)
                    self._thinking = False
                    self._input.disabled = False
                    if self._page:
                        self._page.update()

                if self._page:
                    update_err()

        thread = threading.Thread(target=call_api, daemon=True)
        thread.start()


# ─────────────────────────────────────────────
# VISTA: DASHBOARD
# ─────────────────────────────────────────────
class DashboardView(ft.Container):
    def __init__(self, page):
        super().__init__()

        def metric(icon, icon_color, icon_bg, tag_text, tag_color, tag_bg,
                   label, value):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(icon, color=icon_color, size=20),
                                    bgcolor=icon_bg, width=40, height=40,
                                    border_radius=T.R_MD, alignment=ft.Alignment(0, 0),
                                ),
                                ft.Container(expand=True),
                                badge(tag_text, tag_color, tag_bg),
                            ],
                        ),
                        ft.Container(height=8),
                        ft.Text(label, size=12, color=T.TEXT_MUTED),
                        ft.Text(value, size=22, weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                    ],
                    spacing=3,
                ),
                bgcolor=T.CARD_BG,
                border_radius=T.R_LG,
                padding=16,
                border=ft.Border.all(0.5, T.CARD_BORDER),
                shadow=shadow(T.PRIMARY, 6, 2),
                expand=1,
            )

        metrics = ft.Row(
            controls=[
                metric(ft.Icons.CREDIT_CARD_OUTLINED, T.PRIMARY, T.PRIMARY_LIGHT,
                       "+12.5%", T.PRIMARY, T.PRIMARY_LIGHT,
                       "Total de Ventas", "S/ 45,280.00"),
                metric(ft.Icons.INVENTORY_2_OUTLINED, T.PRIMARY, T.PRIMARY_LIGHT,
                       "842 SKU", T.TEXT_MUTED, T.INPUT_BG,
                       "Productos Activos", "1,248"),
                metric(ft.Icons.WARNING_AMBER_ROUNDED, T.ERROR, T.ERROR_LT,
                       "Urgente", T.ERROR, T.ERROR_LT,
                       "Stock Bajo", "14 Items"),
                metric(ft.Icons.SHOPPING_CART_OUTLINED, T.WARNING, T.WARNING_LT,
                       "-2% vs mes ant.", T.WARNING, T.WARNING_LT,
                       "Gastos Mensuales", "S/ 8,420.50"),
            ],
            spacing=14,
        )

        days = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        actuals = [42, 65, 38, 88, 72, 34, 20]
        projections = [55, 70, 50, 80, 75, 45, 35]
        max_h = max(actuals + projections)

        def bar_col(day, actual, proj):
            bar_h = 110
            return ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            ft.Container(
                                width=28, height=int((proj / max_h) * bar_h),
                                bgcolor=T.PRIMARY_LIGHT, border_radius=ft.BorderRadius(3, 3, 0, 0),
                            ),
                            ft.Container(
                                width=28, height=int((actual / max_h) * bar_h),
                                bgcolor=T.PRIMARY, border_radius=ft.BorderRadius(3, 3, 0, 0),
                            ),
                        ],
                        height=bar_h,
                    ),
                    ft.Text(day, size=10, color=T.TEXT_MUTED),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            )

        chart_legend = ft.Row(
            controls=[
                ft.Row(controls=[
                    ft.Container(width=10, height=10, bgcolor=T.PRIMARY, border_radius=2),
                    ft.Text("Ventas", size=11, color=T.TEXT_MUTED),
                ], spacing=4),
                ft.Row(controls=[
                    ft.Container(width=10, height=10, bgcolor=T.PRIMARY_LIGHT, border_radius=2),
                    ft.Text("Proyectado", size=11, color=T.TEXT_MUTED),
                ], spacing=4),
            ],
            spacing=14,
        )

        chart_card = card(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("Rendimiento Semanal", size=14,
                                            weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                                    ft.Text("Ventas brutas vs Proyecciones", size=11, color=T.TEXT_MUTED),
                                ],
                                spacing=2, expand=True,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Text("Semanas", size=11, color=T.TEXT_MUTED),
                                        padding=ft.padding.symmetric(horizontal=12, vertical=5),
                                        border=ft.Border.all(0.5, T.CARD_BORDER),
                                        border_radius=T.R_PILL,
                                    ),
                                    ft.Container(
                                        content=ft.Text("Meses", size=11, color="#FFFFFF"),
                                        bgcolor=T.PRIMARY,
                                        padding=ft.padding.symmetric(horizontal=12, vertical=5),
                                        border_radius=T.R_PILL,
                                    ),
                                ],
                                spacing=6,
                            ),
                        ],
                    ),
                    ft.Container(height=8),
                    chart_legend,
                    ft.Container(height=8),
                    ft.Row(
                        controls=[bar_col(d, a, p) for d, a, p in zip(days, actuals, projections)],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
        )

        def prod_row(emoji, name, cat, amount, vtas):
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(emoji, size=20),
                            width=40, height=40,
                            bgcolor=T.INPUT_BG,
                            border_radius=T.R_MD,
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(name, size=13, weight=ft.FontWeight.W_600, color=T.TEXT_H),
                                ft.Text(cat, size=11, color=T.TEXT_MUTED),
                            ],
                            spacing=1, expand=True,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(amount, size=13, weight=ft.FontWeight.BOLD, color=T.PRIMARY),
                                ft.Text(vtas, size=10, color=T.TEXT_MUTED),
                            ],
                            spacing=1,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                border=ft.Border(bottom=ft.BorderSide(0.5, T.CARD_BORDER)),
                padding=ft.padding.symmetric(vertical=8),
            )

        top_prod_card = card(
            ft.Column(
                controls=[
                    ft.Text("Productos más Vendidos", size=14,
                            weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                    ft.Container(height=6),
                    prod_row("✒️", "Pluma Estilográfica", "Escritura de lujo", "S/ 2,450", "124 VTAS"),
                    prod_row("📄", "Papel Canson", "Artístico / Acuarela", "S/ 1,820", "98 VTAS"),
                    prod_row("🖊️", "Marcadores", "Tinta pigmentada", "S/ 1,140", "82 VTAS"),
                    prod_row("📓", "Cuaderno Premium", "Hojas de 90g", "S/ 940", "65 VTAS"),
                    ft.Container(height=6),
                    ft.Container(
                        content=ft.Text("Ver Catálogo Completo", size=12,
                                        color=T.PRIMARY, weight=ft.FontWeight.W_600),
                        alignment=ft.Alignment(0, 0),
                        bgcolor=T.PRIMARY_LIGHT,
                        border_radius=T.R_MD,
                        padding=ft.padding.symmetric(vertical=9),
                        ink=True,
                    ),
                ],
                spacing=0,
            ),
        )

        def crit_item(name, amount, pct, color):
            return ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(name, size=12, color=T.TEXT_BODY, expand=True),
                            ft.Text(amount, size=12, weight=ft.FontWeight.W_600, color=color),
                        ],
                    ),
                    ft.Container(
                        content=ft.Container(
                            bgcolor=color, border_radius=T.R_PILL,
                            width=pct, height=6,
                        ),
                        bgcolor=T.INPUT_BG,
                        border_radius=T.R_PILL,
                        height=6,
                    ),
                ],
                spacing=4,
            )

        critical_card = card(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                                    color=T.PRIMARY, size=16),
                            ft.Text("Estado de Existencias Críticas", size=14,
                                    weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=12),
                    crit_item("Resmas Papel Bond A4 (80g)", "12 unidades restantes", 50, T.ERROR),
                    ft.Container(height=10),
                    crit_item("Tinta Epson Cyan 544", "8 unidades restantes", 80, T.WARNING),
                ],
            ),
        )

        self.content = ft.Column(
            controls=[
                section_header("Panel de Control",
                               "Bienvenido de nuevo, Administrador. Aquí está el resumen de hoy."),
                ft.Container(height=16),
                metrics,
                ft.Container(height=16),
                ft.Row(
                    controls=[
                        ft.Container(chart_card, expand=2),
                        ft.Container(top_prod_card, expand=1),
                    ],
                    spacing=14,
                ),
                ft.Container(height=14),
                critical_card,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        self.padding = 24
        self.expand = True
        self.bgcolor = T.PAGE_BG


# ─────────────────────────────────────────────
# VISTA: CATÁLOGO
# ─────────────────────────────────────────────
class CatalogoView(ft.Container):
    def __init__(self, page):
        super().__init__()

        products = [
            ("Cuaderno Justus", "SKU: 123", "S/ 2.50", 30, T.PRIMARY, T.PRIMARY_LIGHT, "📓"),
            ("Cuaderno Standford", "SKU: 456", "Sin precio", 0, T.ACCENT_CYAN, "#ECFEFF", "📒"),
            ("Papel Bond A4", "SKU: 789", "S/ 12.00", 150, T.SUCCESS, T.SUCCESS_LT, "📄"),
            ("Bolígrafo Gel", "SKU: 012", "S/ 1.50", 8, T.WARNING, T.WARNING_LT, "🖊️"),
        ]

        def prod_card(name, sku, price, stock, accent, accent_lt, emoji):
            if stock > 10:
                sc, sb, st = T.SUCCESS, T.SUCCESS_LT, f"{stock} en stock"
            elif stock > 0:
                sc, sb, st = T.WARNING, T.WARNING_LT, f"{stock} en stock"
            else:
                sc, sb, st = T.ERROR, T.ERROR_LT, "Agotado"

            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Stack(
                                controls=[
                                    ft.Container(bgcolor=accent_lt, height=90),
                                    ft.Container(
                                        content=ft.Text(emoji, size=40),
                                        alignment=ft.Alignment(0, 0),
                                        height=90,
                                    ),
                                ],
                            ),
                            height=90,
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(name, size=13, weight=ft.FontWeight.BOLD,
                                            color=T.TEXT_H),
                                    ft.Text(sku, size=11, color=T.TEXT_MUTED),
                                    ft.Container(height=4),
                                    ft.Row(
                                        controls=[
                                            ft.Text(price, size=18, weight=ft.FontWeight.BOLD,
                                                    color=T.PRIMARY if price != "Sin precio" else T.TEXT_MUTED),
                                            ft.Container(expand=True),
                                            badge(st, sc, sb),
                                        ],
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    ft.Container(height=8),
                                    ft.Row(
                                        controls=[
                                            primary_btn("Editar", ft.Icons.EDIT_ROUNDED, "ghost"),
                                            ft.Container(
                                                content=ft.Icon(ft.Icons.MORE_VERT_ROUNDED,
                                                                color=T.TEXT_MUTED, size=16),
                                                width=32, height=32,
                                                bgcolor=T.INPUT_BG,
                                                border=ft.Border.all(0.5, T.CARD_BORDER),
                                                border_radius=T.R_MD,
                                                alignment=ft.Alignment(0, 0),
                                            ),
                                        ],
                                    ),
                                ],
                                spacing=3,
                            ),
                            padding=12,
                        ),
                    ],
                    spacing=0,
                ),
                bgcolor=T.CARD_BG,
                border_radius=T.R_LG,
                border=ft.Border.all(0.5, T.CARD_BORDER),
                shadow=shadow(T.PRIMARY, 6, 2),
                expand=1,
                ink=True,
            )

        grid_row1 = ft.Row(controls=[prod_card(*p) for p in products[:2]], spacing=14)
        grid_row2 = ft.Row(controls=[prod_card(*p) for p in products[2:]], spacing=14)

        stats = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("4", size=20, weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                            ft.Text("Total", size=11, color=T.TEXT_MUTED),
                        ],
                        spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=T.INPUT_BG, border=ft.Border.all(0.5, T.CARD_BORDER),
                    border_radius=T.R_MD,
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("2", size=20, weight=ft.FontWeight.BOLD, color=T.SUCCESS),
                            ft.Text("Con stock", size=11, color=T.TEXT_MUTED),
                        ],
                        spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=T.SUCCESS_LT, border=ft.Border.all(0.5, T.CARD_BORDER),
                    border_radius=T.R_MD,
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("1", size=20, weight=ft.FontWeight.BOLD, color=T.ERROR),
                            ft.Text("Agotados", size=11, color=T.TEXT_MUTED),
                        ],
                        spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=T.ERROR_LT, border=ft.Border.all(0.5, T.CARD_BORDER),
                    border_radius=T.R_MD,
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                ),
            ],
            spacing=10,
        )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        section_header("Catálogo de Productos", "Gestión de inventario y precios"),
                        ft.Container(expand=True),
                        primary_btn("Nuevo Producto", ft.Icons.ADD_ROUNDED),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
                ft.Container(height=14),
                stats,
                ft.Container(height=14),
                searchbar("Buscar por nombre, SKU o categoría..."),
                ft.Container(height=14),
                card(
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("Todos los productos", size=14,
                                            weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                                    ft.Container(expand=True),
                                    app_dropdown("Ordenar", "Más recientes",
                                                 ["Más recientes", "Nombre A-Z", "Precio menor"],
                                                 width=160),
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Container(height=14),
                            grid_row1,
                            ft.Container(height=12),
                            grid_row2,
                        ],
                    ),
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        self.padding = 24
        self.expand = True
        self.bgcolor = T.PAGE_BG


# ─────────────────────────────────────────────
# VISTA: KARDEX
# ─────────────────────────────────────────────
class KardexView(ft.Container):
    def __init__(self, page):
        super().__init__()

        def kmetric(value, label, primary=False):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(value, size=24, weight=ft.FontWeight.BOLD,
                                color="#FFFFFF" if primary else T.TEXT_H),
                        ft.Text(label, size=10, color="#FFFFFF99" if primary else T.TEXT_MUTED,
                                weight=ft.FontWeight.W_600),
                    ],
                    spacing=3,
                ),
                bgcolor=T.PRIMARY if primary else T.CARD_BG,
                border_radius=T.R_LG,
                padding=16,
                border=ft.Border.all(0.5, T.CARD_BORDER if not primary else "transparent"),
                expand=1,
            )

        kmetrics = ft.Row(
            controls=[
                kmetric("2.4k", "ENTRADAS MES", primary=True),
                kmetric("842", "SALIDAS MES"),
                kmetric("15.2k", "STOCK TOTAL"),
            ],
            spacing=12,
        )

        entry_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ADD_CIRCLE_ROUNDED, color=T.SUCCESS, size=14),
                    ft.Text("ENTRADA", size=12, weight=ft.FontWeight.W_700, color=T.SUCCESS),
                ],
                spacing=4, tight=True,
            ),
            bgcolor=T.SUCCESS_LT,
            border=ft.Border.all(1, T.SUCCESS),
            border_radius=T.R_MD,
            padding=ft.padding.symmetric(horizontal=14, vertical=7),
            expand=1,
            alignment=ft.Alignment(0, 0),
            ink=True,
        )
        exit_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.REMOVE_CIRCLE_OUTLINED, color=T.TEXT_MUTED, size=14),
                    ft.Text("SALIDA", size=12, weight=ft.FontWeight.W_600, color=T.TEXT_MUTED),
                ],
                spacing=4, tight=True,
            ),
            bgcolor=T.INPUT_BG,
            border=ft.Border.all(0.5, T.CARD_BORDER),
            border_radius=T.R_MD,
            padding=ft.padding.symmetric(horizontal=14, vertical=7),
            expand=1,
            alignment=ft.Alignment(0, 0),
            ink=True,
        )

        reg_form = card(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.EDIT_NOTE_ROUNDED, color=T.PRIMARY, size=18),
                            ft.Text("Registrar Movimiento", size=14,
                                    weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=12),
                    ft.Text("PRODUCTO", size=10, color=T.TEXT_MUTED, weight=ft.FontWeight.W_600),
                    ft.Container(height=4),
                    app_dropdown("", "Papel Bond A4 80g",
                                 ["Papel Bond A4 80g", "Cuaderno Justus",
                                  "Bolígrafo Gel Negro", "Cuaderno Espiral A5"]),
                    ft.Container(height=10),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("TIPO", size=10, color=T.TEXT_MUTED,
                                            weight=ft.FontWeight.W_600),
                                    ft.Container(height=4),
                                    ft.Row(controls=[entry_btn, exit_btn], spacing=6),
                                ],
                                expand=True,
                            ),
                            ft.Container(
                                content=app_input("CANTIDAD", value="0",
                                                  keyboard_type=ft.KeyboardType.NUMBER,
                                                  width=90),
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=10),
                    ft.Text("MOTIVO / DOCUMENTO", size=10, color=T.TEXT_MUTED,
                            weight=ft.FontWeight.W_600),
                    ft.Container(height=4),
                    ft.TextField(
                        hint_text="Ej: Compra según factura F-001...",
                        multiline=True, min_lines=2, max_lines=3,
                        border_radius=T.R_MD, border_color=T.INPUT_BORDER,
                        focused_border_color=T.INPUT_FOCUSED,
                        fill_color=T.INPUT_BG, filled=True,
                        content_padding=ft.padding.all(12),
                    ),
                    ft.Container(height=12),
                    primary_btn("Confirmar Registro",
                                ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                                expand=True),
                ],
                spacing=0,
            ),
        )

        def row_data(fecha, producto, tipo, cant, razon):
            tipo_badge = badge("ENTRADA", T.SUCCESS, T.SUCCESS_LT) if tipo == "E" \
                else badge("SALIDA", T.ERROR, T.ERROR_LT)
            cant_color = T.SUCCESS if tipo == "E" else T.ERROR
            cant_prefix = "+" if tipo == "E" else "-"
            return ft.DataRow(
                cells=[
                    ft.DataCell(ft.Column(
                        controls=[ft.Text(fecha[0], size=12, color=T.TEXT_MUTED),
                                  ft.Text(fecha[1], size=11, color=T.TEXT_DISABLED)],
                        spacing=0,
                    )),
                    ft.DataCell(ft.Text(producto, size=13, color=T.TEXT_H)),
                    ft.DataCell(tipo_badge),
                    ft.DataCell(ft.Text(f"{cant_prefix}{cant}", size=13,
                                        weight=ft.FontWeight.BOLD, color=cant_color)),
                    ft.DataCell(ft.Text(razon, size=12, color=T.TEXT_MUTED,
                                        max_lines=1, overflow=ft.TextOverflow.ELLIPSIS)),
                ],
            )

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Fecha y Hora", size=11, color=T.TEXT_MUTED, weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Producto", size=11, color=T.TEXT_MUTED, weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Tipo", size=11, color=T.TEXT_MUTED, weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Cant.", size=11, color=T.TEXT_MUTED, weight=ft.FontWeight.W_600)),
                ft.DataColumn(ft.Text("Razón / Ref.", size=11, color=T.TEXT_MUTED, weight=ft.FontWeight.W_600)),
            ],
            rows=[
                row_data(("24 May 2024", "09:15 AM"), "Papel Bond A4 80g", "E", "500", 'Compra Proveedor'),
                row_data(("24 May 2024", "10:42 AM"), "Bolígrafo Gel Negro", "S", "120", "Venta Directa - Ticket 8829"),
                row_data(("23 May 2024", "04:30 PM"), "Cuaderno Espiral A5", "E", "50", "Ajuste de inventario físico"),
                row_data(("23 May 2024", "11:00 AM"), "Marcador Permanente", "S", "15", "Baja por daño en empaque"),
                row_data(("10 Abr 2026", "19:38"), "Cuaderno Justus", "E", "30", "—"),
            ],
            border=ft.Border.all(0, "transparent"),
            border_radius=T.R_MD,
            heading_row_color=T.INPUT_BG,
            data_row_color={"hovered": T.PRIMARY_LIGHT},
            column_spacing=16,
        )

        historial_card = card(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Historial de Movimientos", size=14,
                                    weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                            ft.Container(expand=True),
                            ft.Row(
                                controls=[
                                    primary_btn("Todos", variant="filled"),
                                    primary_btn("Entrada", variant="outline"),
                                    primary_btn("Salida", variant="outline"),
                                ],
                                spacing=6,
                            ),
                        ],
                    ),
                    ft.Container(height=10),
                    searchbar("Buscar por producto..."),
                    ft.Container(height=10),
                    ft.Container(
                        content=table,
                        bgcolor=T.INPUT_BG,
                        border_radius=T.R_MD,
                        border=ft.Border.all(0.5, T.CARD_BORDER),
                    ),
                    ft.Container(height=10),
                    ft.Row(
                        controls=[
                            ft.Text("Mostrando 5 de 1,240 registros",
                                    size=12, color=T.TEXT_MUTED, expand=True),
                            primary_btn("Anterior", variant="outline"),
                            primary_btn("Siguiente"),
                        ],
                        spacing=8,
                    ),
                ],
            ),
        )

        def low_stock_row(name, current, total, color):
            pct = max(4, int((current / total) * 100))
            return ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(name, size=12, weight=ft.FontWeight.W_600,
                                    color=T.TEXT_BODY, expand=True),
                            ft.Text(f"{current} / {total}", size=12,
                                    weight=ft.FontWeight.W_600, color=color),
                        ],
                    ),
                    ft.Container(
                        content=ft.Container(
                            bgcolor=color, border_radius=T.R_PILL,
                            width=pct * 2, height=6,
                        ),
                        bgcolor=T.INPUT_BG, border_radius=T.R_PILL, height=6,
                    ),
                ],
                spacing=4,
            )

        alert_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=T.ERROR, size=16),
                                    ft.Text("Productos con bajo stock (Alertas de Reposición)",
                                            size=13, weight=ft.FontWeight.BOLD, color=T.ERROR),
                                ],
                                spacing=6,
                            ),
                            ft.Container(expand=True),
                            badge("ACCIÓN REQUERIDA", T.ERROR, T.ERROR_LT),
                        ],
                    ),
                    ft.Container(height=12),
                    low_stock_row("PAPEL BOND A4 80G", 150, 1000, T.ERROR),
                    ft.Container(height=8),
                    low_stock_row("TONER LASER HP 85A", 2, 20, T.ERROR),
                ],
                spacing=0,
            ),
            bgcolor=T.CARD_BG,
            border_radius=T.R_LG,
            padding=16,
            border=ft.Border.all(0.5, ft.Colors.with_opacity(0.4, T.ERROR)),
        )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        section_header("Kardex de Movimientos",
                                       "Registro histórico detallado de entradas y salidas de almacén."),
                        ft.Container(expand=True),
                        ft.Row(
                            controls=[
                                primary_btn("Exportar PDF", ft.Icons.PICTURE_AS_PDF_ROUNDED, "outline"),
                                primary_btn("Nuevo Registro", ft.Icons.ADD_ROUNDED),
                            ],
                            spacing=8,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
                ft.Container(height=14),
                kmetrics,
                ft.Container(height=14),
                ft.Row(
                    controls=[
                        ft.Container(reg_form, width=280),
                        ft.Container(historial_card, expand=True),
                    ],
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(height=14),
                alert_card,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        self.padding = 24
        self.expand = True
        self.bgcolor = T.PAGE_BG


# ─────────────────────────────────────────────
# VISTA: GASTOS
# ─────────────────────────────────────────────
class GastosView(ft.Container):
    def __init__(self, page):
        super().__init__()

        def gmetric(label, tag, value, sub_text, sub_color, pct):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(label, size=12, color=T.TEXT_MUTED),
                                ft.Container(width=6),
                                badge(tag, T.PRIMARY, T.PRIMARY_LIGHT),
                            ],
                        ),
                        ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                        ft.Container(
                            content=ft.Container(
                                bgcolor=T.PRIMARY, border_radius=T.R_PILL,
                                width=pct * 2, height=5,
                            ),
                            bgcolor=T.INPUT_BG, border_radius=T.R_PILL, height=5,
                        ),
                        ft.Text(sub_text, size=11, color=sub_color),
                    ],
                    spacing=6,
                ),
                bgcolor=T.CARD_BG,
                border_radius=T.R_LG,
                padding=16,
                border=ft.Border.all(0.5, T.CARD_BORDER),
                expand=1,
            )

        metrics_row = ft.Row(
            controls=[
                gmetric("Gasto Diario", "HOY", "S/ 1,420.50",
                        "15% más que ayer", T.SUCCESS, 65),
                gmetric("Presupuesto Restante", "MENSUAL", "S/ 8,579.50",
                        "75% utilizado", T.TEXT_MUTED, 75),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Resumen de Categorías", size=13,
                                    weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                            ft.Text("Mayor gasto en Suministros de Oficina",
                                    size=11, color=ft.Colors.with_opacity(0.7, "#FFFFFF")),
                            ft.Container(height=8),
                            ft.Row(
                                controls=[
                                    ft.Container(bgcolor=ft.Colors.with_opacity(0.6, "#FFFFFF"),
                                                 border_radius=T.R_SM, height=40, width=30),
                                    ft.Container(bgcolor=ft.Colors.with_opacity(0.5, "#FFFFFF"),
                                                 border_radius=T.R_SM, height=55, width=30),
                                    ft.Container(bgcolor=ft.Colors.with_opacity(0.4, "#FFFFFF"),
                                                 border_radius=T.R_SM, height=35, width=30),
                                    ft.Container(bgcolor=ft.Colors.with_opacity(0.9, "#FFFFFF"),
                                                 border_radius=T.R_SM, height=70, width=30),
                                    ft.Container(bgcolor=ft.Colors.with_opacity(0.35, "#FFFFFF"),
                                                 border_radius=T.R_SM, height=28, width=30),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                                vertical_alignment=ft.CrossAxisAlignment.END,
                                spacing=4,
                            ),
                        ],
                        spacing=3,
                    ),
                    bgcolor=T.SIDEBAR_BG,
                    border_radius=T.R_LG,
                    padding=16,
                    expand=1,
                ),
            ],
            spacing=12,
        )

        form_card = card(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ADD_CIRCLE_ROUNDED, color=T.PRIMARY, size=18),
                            ft.Text("Nuevo Gasto", size=14,
                                    weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=12),
                    ft.Text("CONCEPTO O PRODUCTO", size=10, color=T.TEXT_MUTED,
                            weight=ft.FontWeight.W_600),
                    ft.Container(height=4),
                    app_input("", hint="Ej: Resmas de papel A4"),
                    ft.Container(height=10),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("CATEGORÍA", size=10, color=T.TEXT_MUTED,
                                            weight=ft.FontWeight.W_600),
                                    ft.Container(height=4),
                                    app_dropdown("", "Suministros",
                                                 ["Suministros", "Logística", "Servicios",
                                                  "Mantenimiento"]),
                                ],
                                expand=True,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("MONTO (S/)", size=10, color=T.TEXT_MUTED,
                                            weight=ft.FontWeight.W_600),
                                    ft.Container(height=4),
                                    app_input("", value="0.00",
                                              keyboard_type=ft.KeyboardType.NUMBER,
                                              width=100),
                                ],
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=10),
                    ft.Text("FECHA", size=10, color=T.TEXT_MUTED, weight=ft.FontWeight.W_600),
                    ft.Container(height=4),
                    app_input("", hint="mm/dd/yyyy",
                              prefix_icon=ft.Icons.CALENDAR_TODAY_ROUNDED),
                    ft.Container(height=14),
                    primary_btn("Registrar Gasto", ft.Icons.ADD_ROUNDED, expand=True),
                ],
                spacing=0,
            ),
        )

        def gasto_row(emoji, nombre, ref, cat, cat_color, cat_bg, fecha, monto):
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(emoji, size=20),
                            width=40, height=40, bgcolor=T.INPUT_BG,
                            border_radius=T.R_MD, alignment=ft.Alignment(0, 0),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(nombre, size=13, weight=ft.FontWeight.W_600, color=T.TEXT_H),
                                ft.Text(ref, size=11, color=T.TEXT_MUTED),
                            ],
                            spacing=2, expand=True,
                        ),
                        ft.Column(
                            controls=[badge(cat, cat_color, cat_bg)],
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                        ),
                        ft.Container(width=10),
                        ft.Column(
                            controls=[
                                ft.Text(monto, size=13, weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                                ft.Text(fecha, size=11, color=T.TEXT_MUTED),
                            ],
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                border=ft.Border(bottom=ft.BorderSide(0.5, T.CARD_BORDER)),
                padding=ft.padding.symmetric(vertical=10),
            )

        list_card = card(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Gastos Recientes", size=14,
                                    weight=ft.FontWeight.BOLD, color=T.TEXT_H, expand=True),
                            ft.Text("Ver todo el historial", size=12, color=T.PRIMARY),
                        ],
                    ),
                    ft.Container(height=10),
                    gasto_row("🚚", "Envío Proveedor FABER", "Referencia #9021",
                              "LOGÍSTICA", T.PRIMARY, T.PRIMARY_LIGHT, "Hoy, 10:45", "S/ 45.00"),
                    gasto_row("🖨️", "Cartuchos de Tinta Pro", "Insumos de impresión",
                              "SUMINISTROS", T.TEXT_MUTED, T.INPUT_BG, "Ayer", "S/ 320.00"),
                    gasto_row("⚡", "Recibo de Luz - Local A", "Pago de servicios",
                              "SERVICIOS", T.WARNING, T.WARNING_LT, "22 Oct", "S/ 1,055.50"),
                    gasto_row("🧹", "Materiales de Limpieza", "Mantenimiento mensual",
                              "SUMINISTROS", T.TEXT_MUTED, T.INPUT_BG, "20 Oct", "S/ 85.00"),
                ],
                spacing=0,
            ),
        )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        section_header("Libro de Gastos",
                                       "Control de egresos y presupuesto de suministros."),
                        ft.Container(expand=True),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
                ft.Container(height=14),
                metrics_row,
                ft.Container(height=14),
                ft.Row(
                    controls=[
                        ft.Container(form_card, width=290),
                        ft.Container(list_card, expand=True),
                    ],
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        self.padding = 24
        self.expand = True
        self.bgcolor = T.PAGE_BG


# ─────────────────────────────────────────────
# VISTA: VENTAS / BOLETAS
# ─────────────────────────────────────────────
class VentasView(ft.Container):
    def __init__(self, page):
        super().__init__()
        self._page = page
        self._cart = {}
        self._cart_col = ft.Column(spacing=0, expand=True)
        self._cart_total_col = ft.Column(spacing=0)
        self._build()

    def _build(self):
        products = [
            ("Pluma Estilográfica Premium", "✒️", 12.50, 34, "Tinta negra, punta fina"),
            ("Cuaderno de Cuero A5",        "📔", 24.00,  5, "Hojas punteadas, 120g"),
            ("Set Cintas Washi Pastel",     "🎀",  8.20, 120, "Paquete de 6 unidades"),
            ("Pack Resaltadores Neon",      "🖊️",  5.90,  45, "4 colores de alta visibilidad"),
            ("Agenda Ejecutiva 2024",       "📅", 18.00,   1, "Diseño minimalista gris"),
            ("Marcadores Caligráficos",     "🎨", 14.30,  28, "Set de 12 gradientes azules"),
        ]

        def prod_tile(name, emoji, price, stock, desc):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Stack(
                            controls=[
                                ft.Container(
                                    content=ft.Text(emoji, size=36),
                                    bgcolor=T.INPUT_BG,
                                    height=80,
                                    alignment=ft.Alignment(0, 0),
                                    border_radius=ft.BorderRadius(T.R_LG, T.R_LG, 0, 0),
                                ),
                                ft.Container(
                                    content=ft.Text(f"{stock} unid.", size=9,
                                                    weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                    bgcolor=T.PRIMARY,
                                    border_radius=T.R_PILL,
                                    padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                    top=6, right=6,
                                ),
                            ],
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(name, size=12, weight=ft.FontWeight.BOLD,
                                            color=T.TEXT_H, max_lines=2),
                                    ft.Text(desc, size=10, color=T.TEXT_MUTED),
                                    ft.Container(height=4),
                                    ft.Row(
                                        controls=[
                                            ft.Text(f"S/{price:.2f}", size=16,
                                                    weight=ft.FontWeight.BOLD, color=T.PRIMARY),
                                            ft.Container(expand=True),
                                            ft.Container(
                                                content=ft.Icon(ft.Icons.ADD_SHOPPING_CART_ROUNDED,
                                                                color=T.PRIMARY, size=16),
                                                width=30, height=30,
                                                bgcolor=T.PRIMARY_LIGHT,
                                                border_radius=T.R_MD,
                                                alignment=ft.Alignment(0, 0),
                                            ),
                                        ],
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ],
                                spacing=3,
                            ),
                            padding=10,
                        ),
                    ],
                    spacing=0,
                ),
                bgcolor=T.CARD_BG,
                border_radius=T.R_LG,
                border=ft.Border.all(0.5, T.CARD_BORDER),
                shadow=shadow(T.PRIMARY, 4, 1),
                on_click=lambda e, n=name, em=emoji, pr=price: self._add(n, em, pr),
                ink=True,
                expand=1,
            )

        grid_rows = []
        for i in range(0, len(products), 3):
            grid_rows.append(
                ft.Row(controls=[prod_tile(*p) for p in products[i:i+3]], spacing=10)
            )

        left = ft.Column(controls=[*grid_rows], spacing=10, expand=True)

        cart_count = ft.Container(
            content=ft.Text("0 Items", size=10, weight=ft.FontWeight.W_600, color=T.PRIMARY),
            bgcolor=T.PRIMARY_LIGHT,
            padding=ft.padding.symmetric(horizontal=8, vertical=3),
            border_radius=T.R_PILL,
        )
        self._cart_count_badge = cart_count

        right = card(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Carrito de Venta", size=14,
                                    weight=ft.FontWeight.BOLD, color=T.TEXT_H, expand=True),
                            cart_count,
                        ],
                    ),
                    ft.Container(height=10),
                    self._cart_col,
                    ft.Container(height=4),
                    self._cart_total_col,
                    ft.Container(height=10),
                    primary_btn("🧾  Generar Boleta", icon=None, expand=True),
                    ft.Container(height=6),
                    primary_btn("Cancelar", variant="outline", expand=True),
                ],
                spacing=0,
            ),
        )

        self._render_cart()

        self.content = ft.Column(
            controls=[
                section_header("Venta en Curso", "Seleccione productos para la boleta actual"),
                ft.Container(height=14),
                ft.Row(
                    controls=[
                        ft.Container(left, expand=True),
                        ft.Container(right, width=290),
                    ],
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        self.padding = 24
        self.expand = True
        self.bgcolor = T.PAGE_BG

    def _add(self, name, emoji, price):
        if name in self._cart:
            self._cart[name]["qty"] += 1
        else:
            self._cart[name] = {"emoji": emoji, "price": price, "qty": 1}
        self._render_cart()
        if self._page:
            self._page.update()

    def _remove(self, name):
        if name in self._cart:
            del self._cart[name]
        self._render_cart()
        if self._page:
            self._page.update()

    def _change_qty(self, name, delta):
        if name in self._cart:
            self._cart[name]["qty"] += delta
            if self._cart[name]["qty"] <= 0:
                del self._cart[name]
        self._render_cart()
        if self._page:
            self._page.update()

    def _render_cart(self):
        self._cart_col.controls.clear()
        self._cart_total_col.controls.clear()

        if not self._cart:
            self._cart_col.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED, size=40, color=T.TEXT_DISABLED),
                            ft.Text("Haz clic en un producto\npara agregarlo",
                                    size=12, color=T.TEXT_MUTED, text_align=ft.TextAlign.CENTER),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    height=120,
                    alignment=ft.Alignment(0, 0),
                    bgcolor=T.INPUT_BG,
                    border_radius=T.R_MD,
                    border=ft.Border.all(0.5, T.CARD_BORDER),
                )
            )
            self._cart_count_badge.content = ft.Text(
                "0 Items", size=10, weight=ft.FontWeight.W_600, color=T.PRIMARY)
            return

        total = 0.0
        for name, v in self._cart.items():
            subtotal = v["price"] * v["qty"]
            total += subtotal
            self._cart_col.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(v["emoji"], size=22),
                            ft.Column(
                                controls=[
                                    ft.Text(name, size=12, weight=ft.FontWeight.W_600,
                                            color=T.TEXT_H, max_lines=1),
                                    ft.Text(f"S/{v['price']:.2f} c/u", size=11, color=T.TEXT_MUTED),
                                ],
                                spacing=1, expand=True,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Text("−", size=14, color=T.TEXT_MUTED),
                                        width=24, height=24, bgcolor=T.INPUT_BG,
                                        border=ft.Border.all(0.5, T.CARD_BORDER),
                                        border_radius=6, alignment=ft.Alignment(0, 0),
                                        ink=True,
                                        on_click=lambda e, n=name: self._change_qty(n, -1),
                                    ),
                                    ft.Text(str(v["qty"]), size=12, width=20,
                                            text_align=ft.TextAlign.CENTER),
                                    ft.Container(
                                        content=ft.Text("+", size=14, color=T.TEXT_MUTED),
                                        width=24, height=24, bgcolor=T.INPUT_BG,
                                        border=ft.Border.all(0.5, T.CARD_BORDER),
                                        border_radius=6, alignment=ft.Alignment(0, 0),
                                        ink=True,
                                        on_click=lambda e, n=name: self._change_qty(n, 1),
                                    ),
                                ],
                                spacing=4,
                            ),
                            ft.Container(
                                content=ft.Text("✕", size=12, color=T.TEXT_MUTED),
                                ink=True,
                                on_click=lambda e, n=name: self._remove(n),
                                padding=4,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    border=ft.Border(bottom=ft.BorderSide(0.5, T.CARD_BORDER)),
                    padding=ft.padding.symmetric(vertical=8),
                )
            )

        igv = total * 0.18
        self._cart_total_col.controls += [
            ft.Row(controls=[
                ft.Text("Subtotal", size=13, color=T.TEXT_MUTED, expand=True),
                ft.Text(f"S/{total:.2f}", size=13, color=T.TEXT_BODY),
            ]),
            ft.Row(controls=[
                ft.Text("IGV (18%)", size=13, color=T.TEXT_MUTED, expand=True),
                ft.Text(f"S/{igv:.2f}", size=13, color=T.TEXT_BODY),
            ]),
            ft.Divider(height=0.5, color=T.DIVIDER),
            ft.Row(controls=[
                ft.Text("Total", size=15, weight=ft.FontWeight.BOLD,
                        color=T.TEXT_H, expand=True),
                ft.Text(f"S/{total + igv:.2f}", size=16,
                        weight=ft.FontWeight.BOLD, color=T.PRIMARY),
            ]),
        ]

        count = sum(v["qty"] for v in self._cart.values())
        self._cart_count_badge.content = ft.Text(
            f"{count} Items", size=10, weight=ft.FontWeight.W_600, color=T.PRIMARY)


# ─────────────────────────────────────────────
# VISTA: REPORTES
# ─────────────────────────────────────────────
class ReportesView(ft.Container):
    def __init__(self, page):
        super().__init__()

        def report_stat(tag, tag_color, tag_bg, label, value, diff, diff_color):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        badge(tag, tag_color, tag_bg),
                        ft.Container(height=6),
                        ft.Text(label, size=12, color=T.TEXT_MUTED),
                        ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                        ft.Text(diff, size=11, color=diff_color),
                    ],
                    spacing=3,
                ),
                bgcolor=T.CARD_BG, border_radius=T.R_LG, padding=16,
                border=ft.Border.all(0.5, T.CARD_BORDER),
                shadow=shadow(T.PRIMARY, 4, 1),
            )

        stats_col = ft.Column(
            controls=[
                report_stat("EXISTENCIAS", T.PRIMARY, T.PRIMARY_LIGHT,
                            "Ventas Totales", "S/ 45,280.00",
                            "↑ +12.5% vs mes anterior", T.SUCCESS),
                ft.Container(height=10),
                report_stat("MARGEN", T.SUCCESS, T.SUCCESS_LT,
                            "Utilidad Neta", "S/ 12,840.50",
                            "↑ +5.2% vs mes anterior", T.SUCCESS),
            ],
            spacing=0,
            width=230,
        )

        weeks = [[40, 45, 60, 50], [70, 80, 95, 75], [55, 65, 88, 92], [60, 72, 65, 45]]
        proj  = [[50, 55, 65, 60], [75, 85, 90, 80], [60, 70, 85, 88], [65, 75, 70, 50]]
        max_v = max(v for row in weeks + proj for v in row)

        bar_cols = []
        for wi, (wvals, pvals) in enumerate(zip(weeks, proj)):
            week_bars = ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Container(bgcolor=T.PRIMARY_LIGHT,
                                         border_radius=ft.BorderRadius(3, 3, 0, 0),
                                         width=12, height=int((pvals[di] / max_v) * 160)),
                            ft.Container(bgcolor=T.PRIMARY,
                                         border_radius=ft.BorderRadius(3, 3, 0, 0),
                                         width=12, height=int((wvals[di] / max_v) * 160)),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2,
                    ) for di in range(4)
                ],
                spacing=3,
                vertical_alignment=ft.CrossAxisAlignment.END,
            )
            bar_cols.append(ft.Column(
                controls=[week_bars, ft.Text(f"SEMANA 0{wi+1}", size=9, color=T.TEXT_MUTED)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4,
            ))

        trend_card = card(ft.Column(controls=[
            ft.Text("Tendencias de Venta Diaria", size=14,
                    weight=ft.FontWeight.BOLD, color=T.TEXT_H),
            ft.Container(height=12),
            ft.Row(controls=bar_cols, alignment=ft.MainAxisAlignment.SPACE_AROUND,
                   vertical_alignment=ft.CrossAxisAlignment.END),
        ]))

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        section_header("Reportes y Analítica",
                                       "Visualiza el rendimiento de tu papelería con datos precisos."),
                        ft.Container(expand=True),
                        ft.Row(controls=[
                            primary_btn("Este Mes"),
                            primary_btn("Trimestre", variant="outline"),
                            primary_btn("Año 2024", variant="outline"),
                        ], spacing=6),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
                ft.Container(height=14),
                ft.Row(
                    controls=[
                        stats_col,
                        ft.Container(content=trend_card, expand=True),
                    ],
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        self.padding = 24
        self.expand = True
        self.bgcolor = T.PAGE_BG


# ─────────────────────────────────────────────
# VISTA: SINCRONIZACIÓN
# ─────────────────────────────────────────────
class SyncView(ft.Container):
    def __init__(self, page):
        super().__init__()

        status_card = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.CLOUD_DONE_ROUNDED, color=T.PRIMARY, size=22),
                        bgcolor=T.PRIMARY_LIGHT, width=50, height=50,
                        border_radius=T.R_PILL, alignment=ft.Alignment(0, 0),
                    ),
                    ft.Container(width=12),
                    ft.Column(
                        controls=[
                            badge("CLOUD SYNC ACTIVE", T.PRIMARY, T.PRIMARY_LIGHT),
                            ft.Container(height=4),
                            ft.Text("Sincronización en tiempo real", size=15,
                                    weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                        ],
                        spacing=0, expand=True,
                    ),
                    ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=T.SUCCESS, size=36),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=T.INFO_LT,
            border=ft.Border.all(0.5, ft.Colors.with_opacity(0.3, T.INFO)),
            border_radius=T.R_LG,
            padding=16,
        )

        action_btns = ft.Row(
            controls=[
                primary_btn("↑  Sincronizar Ahora", ft.Icons.SYNC_ROUNDED, expand=True),
                primary_btn("↓  Exportar Datos", ft.Icons.DOWNLOAD_ROUNDED, "outline", expand=True),
                primary_btn("☁  Importar Respaldo", ft.Icons.UPLOAD_ROUNDED, "outline", expand=True),
            ],
            spacing=8,
        )

        security_banner = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("🔒 Protección de Datos Nivel Editorial",
                            size=14, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ft.Text(
                        "Todos sus registros de inventario están encriptados "
                        "con protocolos de grado bancario (AES-256) antes de subir a la nube.",
                        size=12, color=ft.Colors.with_opacity(0.75, "#FFFFFF"),
                    ),
                ],
                spacing=6,
            ),
            bgcolor=T.SIDEBAR_BG,
            border_radius=T.R_LG,
            padding=20,
            margin=ft.margin.only(top=14),
        )

        self.content = ft.Column(
            controls=[
                section_header("Sincronización y Respaldo",
                               "Gestiona la integridad de tus datos y la nube de Papelería Pro."),
                ft.Container(height=14),
                status_card,
                ft.Container(height=12),
                card(ft.Column(controls=[action_btns], spacing=0)),
                security_banner,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        self.padding = 24
        self.expand = True
        self.bgcolor = T.PAGE_BG


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main(page: ft.Page):
    global T

    page.title = "Papelería Pro — Gestión de Inventario"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.bgcolor = T.PAGE_BG
    page.window.min_width = 900
    page.window.min_height = 600

    state = {"view": "dashboard", "dark": False}
    content_area = ft.Container(expand=True, bgcolor=T.PAGE_BG)
    sidebar_ref = [None]

    VIEW_MAP = {
        "dashboard": DashboardView,
        "catalogo":  CatalogoView,
        "kardex":    KardexView,
        "gastos":    GastosView,
        "boletas":   VentasView,
        "reportes":  ReportesView,
        "asistente": AsistenteIAView,
        "sync":      SyncView,
    }

    def get_view(name):
        cls = VIEW_MAP.get(name, DashboardView)
        return cls(page)

    def navigate(view_name: str):
        state["view"] = view_name
        content_area.content = get_view(view_name)
        content_area.bgcolor = T.PAGE_BG
        if sidebar_ref[0]:
            sidebar_ref[0].update_view(view_name)
        page.update()

    def toggle_theme():
        global T
        state["dark"] = not state["dark"]
        T = DarkTheme if state["dark"] else LightTheme
        page.theme_mode = ft.ThemeMode.DARK if state["dark"] else ft.ThemeMode.LIGHT
        page.bgcolor = T.PAGE_BG
        build_layout()
        page.update()

    def build_layout():
        nonlocal content_area
        sidebar = Sidebar(page, state["view"], navigate, toggle_theme)
        sidebar_ref[0] = sidebar
        content_area = ft.Container(
            content=get_view(state["view"]),
            expand=True,
            bgcolor=T.PAGE_BG,
        )
        topbar = TopBar(page)
        page.controls.clear()
        page.add(
            ft.Column(
                controls=[
                    topbar,
                    ft.Row(
                        controls=[
                            sidebar,
                            ft.Container(width=0.5, bgcolor=T.DIVIDER),
                            content_area,
                        ],
                        spacing=0,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        )

    build_layout()
    page.update()


if __name__ == "__main__":
    ft.run(main)