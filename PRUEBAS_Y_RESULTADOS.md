# Cálculos, reportes y resultados de prueba

## Responsable

Nicol Gillary Saldivar Benites

## Actividades relacionadas

- US-04 Calcular tarifa, subtotal, IGV y total.
- US-05 Generar facturas_validadas.csv.
- US-06 Crear reporte consolidado y alertas.

## Objetivo

Comprobar que el sistema calcule correctamente los montos de facturación,
genere el archivo de salida y presente indicadores útiles para analizar los
pedidos de FM Industrial.

## Parámetros comerciales

- Tarifa de Banda Transportadora: S/ 65.00 por metro.
- Tarifa de Cinta de Transmisión: S/ 35.00 por metro.
- Tasa de IGV: 18 %.

## Fórmulas utilizadas

- Metros del pedido = largo × cantidad.
- Subtotal = largo × cantidad × tarifa por metro.
- IGV = subtotal × 0.18.
- Importe total = subtotal + IGV.
- Porcentaje validado = pedidos validados × 100 / pedidos procesados.
- Promedio facturado = importe total válido / pedidos validados.

## Archivo generado

El sistema genera el archivo facturas_validadas.csv con las siguientes
columnas:

- ID del pedido.
- Cliente.
- Tipo de faja.
- Ancho.
- Largo.
- Cantidad.
- Tarifa por metro.
- Subtotal.
- IGV.
- Total.
- Estado.
- Observación.

## Resultados obtenidos

Con los datos de prueba actuales se obtuvieron los siguientes resultados:

- Pedidos procesados: 10.
- Pedidos validados: 8.
- Pedidos observados: 2.
- Porcentaje de validación: 80 %.
- Subtotal válido acumulado: S/ 34 105.00.
- IGV acumulado: S/ 6 138.90.
- Importe total facturado: S/ 40 243.90.
- Promedio por pedido validado: S/ 5 030.49.
- Metros totales procesados: 710.00 metros.
- Unidades totales: 21.
- Metros de Banda Transportadora: 308.50 metros.
- Metros de Cinta de Transmisión: 401.50 metros.
- Total facturado en bandas: S/ 23 661.95.
- Total facturado en cintas: S/ 16 581.95.

## Pedido con mayor importe

- ID: FAC-005.
- Cliente: Minera Sur.
- Importe total: S/ 12 272.00.

## Pedidos observados

### FAC-007

El largo registrado es igual a cero. El sistema lo clasifica como OBSERVADO
porque el largo debe encontrarse entre 0.01 y 500 metros.

### FAC-008

El producto registrado es Rodillo Industrial. El sistema lo clasifica como
OBSERVADO porque únicamente se permiten Banda Transportadora y Cinta de
Transmisión.

## Casos comprobados

1. Pedido válido de Banda Transportadora.
2. Pedido válido de Cinta de Transmisión.
3. Cálculo de subtotal.
4. Cálculo de IGV.
5. Cálculo del importe total.
6. Generación del archivo de salida.
7. Producto no permitido.
8. Largo fuera del rango.
9. Reporte de pedidos validados y observados.
10. Identificación del pedido de mayor importe.

## Conclusión de las pruebas

El sistema procesó correctamente los diez pedidos y detectó dos registros con
errores. Los pedidos observados no fueron incorporados a la facturación válida.
Los resultados permiten analizar los montos facturados y las cantidades
necesarias para el despacho.
