from decimal import Decimal

import pytest

from cafeteria import admin, ventas
from cafeteria.productos import Catalogo, StockInsuficiente

ADMIN = {"nombre": "Lupita", "rol": "admin"}
CAJERO = {"nombre": "Pepe", "rol": "cajero"}


@pytest.fixture
def catalogo():
    c = Catalogo()
    c.crear("Café americano", "25.50", stock=10)
    c.crear("Torta", "40.00", stock=2)
    return c


@pytest.mark.regla("RN-001")
def test_total_exacto_con_decimal(catalogo):
    assert ventas.total(catalogo, [(1, 3)]) == Decimal("76.50")


@pytest.mark.regla("RN-002")
def test_stock_no_queda_negativo(catalogo):
    with pytest.raises(StockInsuficiente):
        ventas.total(catalogo, [(1, 1), (2, 3)])
    assert catalogo.obtener(1).stock == 10  # no se descontó a medias


@pytest.mark.regla("RN-003")
def test_solo_admin_cambia_precio(catalogo):
    with pytest.raises(admin.SinPermiso):
        admin.cambiar_precio(CAJERO, catalogo, 1, "1.00")
    admin.cambiar_precio(ADMIN, catalogo, 1, "27.00")
    assert catalogo.obtener(1).precio == Decimal("27.00")


@pytest.mark.regla("RN-004")
def test_descuento_maximo_20(catalogo):
    with pytest.raises(ventas.DescuentoInvalido):
        ventas.total(catalogo, [(1, 1)], descuento="0.25")
    assert ventas.total(catalogo, [(2, 1)], descuento="0.20") == Decimal("32.00")


def test_crud_de_productos(catalogo):
    p = catalogo.crear("Jugo", "18.00", stock=5)
    catalogo.surtir(p.id, 5)
    assert catalogo.obtener(p.id).stock == 10
    admin.eliminar_producto(ADMIN, catalogo, p.id)
    assert catalogo.obtener(p.id) is None
