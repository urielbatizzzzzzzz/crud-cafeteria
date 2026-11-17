"""Ventas de la cafetería: total, descuento y salida de stock."""
from decimal import ROUND_HALF_UP, Decimal

from cafeteria.productos import Catalogo, StockInsuficiente

DESCUENTO_MAXIMO = Decimal("0.20")


class DescuentoInvalido(Exception):
    """El descuento supera el máximo permitido (RN-004)."""


def total(catalogo: Catalogo, renglones: list[tuple[int, int]], descuento: str = "0") -> Decimal:
    """`renglones` = [(producto_id, cantidad)]. Descuenta el stock solo si todo el pedido alcanza (RN-002)."""
    pct = Decimal(descuento)
    if pct < 0 or pct > DESCUENTO_MAXIMO:
        raise DescuentoInvalido(f"El descuento máximo es {DESCUENTO_MAXIMO:.0%}")
    # Primero se revisa todo el pedido, para no descontar a medias si un producto no alcanza
    for pid, cant in renglones:
        producto = catalogo.obtener(pid)
        if cant > producto.stock:
            raise StockInsuficiente(f"Solo hay {producto.stock} de {producto.nombre}")
    subtotal = sum((catalogo.obtener(pid).precio * cant for pid, cant in renglones), Decimal("0"))
    for pid, cant in renglones:
        catalogo.descontar_stock(pid, cant)
    return (subtotal * (1 - pct)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def propina_sugerida(monto: Decimal) -> float:
    # Incumple RN-001 a propósito: calcula dinero con float (puede perder centavos)
    return round(float(monto) * 0.10, 2)
