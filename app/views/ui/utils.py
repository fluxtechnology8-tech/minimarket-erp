from __future__ import annotations

from datetime import datetime


def parse_float(value, default: float = 0.0) -> float:
    if value is None:
        return default
    text = str(value).strip().replace(",", ".")
    if not text:
        return default
    return float(text)


def parse_int(value, default: int = 0) -> int:
    if value is None:
        return default
    text = str(value).strip()
    if not text:
        return default
    return int(float(text))


def money(value: float) -> str:
    return f"S/ {value:,.2f}"


def short_datetime(value: str | datetime | None) -> str:
    if not value:
        return "-"
    
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y %H:%M")
    
    if isinstance(value, str):
        normalized = value.replace("T", " ")
        for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(normalized, fmt).strftime("%d/%m/%Y %H:%M")
            except ValueError:
                continue
        return normalized
    
    return str(value)
