# CRUD Cafetería escolar

Repositorio de prueba para IA VOY: CRUD de productos y ventas de una cafetería, con sus reglas de negocio en
`reglas_negocio.toml`. Son reglas distintas a las de la biblioteca, para comprobar que cada proyecto se
califica con las suyas.

## Reglas de negocio

| Regla | En palabras simples | Ejemplo | Cómo la revisa IA VOY | Resultado esperado |
|---|---|---|---|---|
| RN-001 | Los cobros salen exactos al centavo | 3 cafés de $25.50 = $76.50 exactos | Patrón: no debe aparecer `float(` en `cafeteria/`, y la prueba `test_total_exacto_al_centavo` | **No cumple**, a propósito |
| RN-002 | No se vende lo que no hay | Quedan 2 tortas y piden 3: se rechaza el pedido entero y no se descuenta nada | Prueba `test_no_se_vende_lo_que_no_hay` | Cumple |
| RN-003 | Solo el administrador cambia precios o borra productos | Pepe (cajero) no puede bajar el café a $1.00; Lupita (administradora) sí puede cambiarlo | Patrón: `@requiere_admin` debe estar en `cafeteria/admin.py`, y la prueba `test_solo_admin_cambia_precio` | Cumple |
| RN-004 | El descuento máximo es de 20 % | Torta de $40.00 con 20 % = $32.00; un 25 % se rechaza | Prueba `test_descuento_maximo_20` | Cumple |

**Resultado esperado del análisis:** 4 reglas · 3 cumplen · 1 no cumple (RN-001).

- **Las pruebas solo corren con el sandbox** (`SANDBOX=wsl` o `docker`). Sin él, RN-002 y RN-004 quedan
  "sin verificar". RN-003 también queda "sin verificar", aunque su patrón cumple, porque su prueba no corrió.
  RN-001 sigue en "no cumple".
- **RN-001 falla a propósito**, en `propina_sugerida` de `cafeteria/ventas.py`, para comprobar que IA VOY señala
  el archivo y la línea. Su prueba sí pasa: la regla no cumple porque basta que falle el patrón o una prueba.

## Uso

```bash
pip install -r requirements.txt
pytest
```
