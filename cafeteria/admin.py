"""Operaciones que solo puede hacer un administrador."""
from decimal import Decimal
from functools import wraps

from cafeteria.productos import Catalogo


class SinPermiso(Exception):
    """El usuario no tiene rol de administrador (RN-003)."""


def requiere_admin(funcion):
    @wraps(funcion)
    def envoltura(usuario: dict, *args, **kwargs):
        if usuario.get("rol") != "admin":
            raise SinPermiso(f"{usuario.get('nombre', 'usuario')} no es administrador")
        return funcion(usuario, *args, **kwargs)
    return envoltura


@requiere_admin
def cambiar_precio(usuario: dict, catalogo: Catalogo, producto_id: int, precio: str) -> None:
    catalogo.obtener(producto_id).precio = Decimal(precio)


@requiere_admin
def eliminar_producto(usuario: dict, catalogo: Catalogo, producto_id: int) -> None:
    catalogo.borrar(producto_id)
