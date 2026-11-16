"""CRUD de productos de la cafetería (en memoria)."""
from dataclasses import dataclass
from decimal import Decimal


class StockInsuficiente(Exception):
    """La venta dejaría el stock en negativo (RN-002)."""


@dataclass
class Producto:
    id: int
    nombre: str
    precio: Decimal
    stock: int


class Catalogo:
    def __init__(self) -> None:
        self._productos: dict[int, Producto] = {}
        self._siguiente = 1

    def crear(self, nombre: str, precio: str, stock: int = 0) -> Producto:
        producto = Producto(self._siguiente, nombre, Decimal(precio), stock)
        self._productos[producto.id] = producto
        self._siguiente += 1
        return producto

    def obtener(self, producto_id: int) -> Producto | None:
        return self._productos.get(producto_id)

    def listar(self) -> list[Producto]:
        return sorted(self._productos.values(), key=lambda p: p.nombre)

    def surtir(self, producto_id: int, cantidad: int) -> None:
        self._productos[producto_id].stock += cantidad

    def descontar_stock(self, producto_id: int, cantidad: int) -> None:
        producto = self._productos[producto_id]
        if cantidad > producto.stock:
            raise StockInsuficiente(f"Solo hay {producto.stock} de {producto.nombre}")
        producto.stock -= cantidad

    def borrar(self, producto_id: int) -> None:
        del self._productos[producto_id]
