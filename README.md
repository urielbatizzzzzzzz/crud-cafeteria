# CRUD Cafetería escolar

Repositorio de prueba para IA VOY: CRUD de productos y ventas de una cafetería, con sus reglas de negocio en
`reglas_negocio.toml`. Son reglas distintas a las de la biblioteca, para comprobar que cada proyecto se
califica con las suyas.

## Reglas de negocio

| Regla | Qué dice | Cómo se verifica | Resultado esperado en IA VOY |
|---|---|---|---|
| RN-001 | Dinero con Decimal, nunca float | Patrón `prohibido` en `cafeteria/` | **No cumple**: `propina_sugerida` usa `float(` (a propósito) |
| RN-002 | El stock nunca queda negativo | Prueba `@pytest.mark.regla("RN-002")` | Cumple (con sandbox; sin él, sin verificar) |
| RN-003 | Cambios de precio y bajas solo por admin | Patrón `obligatorio` en `cafeteria/admin.py` | **Cumple** |
| RN-004 | Descuento máximo de 20 % | Prueba `@pytest.mark.regla("RN-004")` | Cumple (con sandbox; sin él, sin verificar) |

El incumplimiento de RN-001 está puesto a propósito, para comprobar que IA VOY lo detecta y señala el archivo
y la línea.

## Uso

```bash
pip install -r requirements.txt
pytest
```
