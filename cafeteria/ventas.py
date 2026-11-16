"""Ventas de la cafetería: total, descuento y salida de stock."""
from decimal import ROUND_HALF_UP, Decimal

from cafeteria.productos import Catalogo

DESCUENTO_MAXIMO = Decimal("0.20")


class DescuentoInvalido(Exception):
    """El descuento supera el máximo permitido (RN-004)."""


def total(catalogo: Catalogo, renglones: list[tuple[int, int]], descuento: str = "0") -> Decimal:
    """`renglones` = [(producto_id, cantidad)]. Descuenta el stock solo si la venta es válida."""
    pct = Decimal(descuento)
    if pct < 0 or pct > DESCUENTO_MAXIMO:
        raise DescuentoInvalido(f"El descuento máximo es {DESCUENTO_MAXIMO:%}")
    subtotal = sum((catalogo.obtener(pid).precio * cant for pid, cant in renglones), Decimal("0"))
    # Primero se revisa todo el stock, para no descontar a medias si un producto no alcanza
    for pid, cant in renglones:
        if cant > catalogo.obtener(pid).stock:
            catalogo.descontar_stock(pid, cant)  # lanza StockInsuficiente
    for pid, cant in renglones:
        catalogo.descontar_stock(pid, cant)
    return (subtotal * (1 - pct)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def propina_sugerida(monto: Decimal) -> float:
    # Incumple RN-001 a propósito: calcula dinero con float
    return round(float(monto) * 0.10, 2)
