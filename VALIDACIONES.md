# Lectura y validaciones del archivo CSV

## Responsable

Bryan Carlos Velasco

## Actividades relacionadas

US-02 Implementar lectura repetitiva del archivo CSV.
US-03 Validar campos, rangos, duplicados y tipos.

## Objetivo

Documentar el proceso empleado para leer cada pedido del archivo CSV y validar que la información sea correcta antes de calcular la facturación y preparar el despacho.

## Lectura repetitiva del archivo

El sistema utiliza el módulo csv de Python para abrir y procesar el archivo pedidos_fm_industrial.csv.

Un ciclo for recorre cada fila del archivo. En cada repetición se obtiene la información correspondiente a un pedido y se aplican las validaciones necesarias.

Los campos numéricos se convierten al tipo de dato correspondiente:

Ancho_Pulgadas se convierte a entero.
Largo_Metros se convierte a decimal.
Cantidad se convierte a entero.

## Validaciones aplicadas

Antes de calcular la factura, el sistema verifica:

1. El ID del pedido no debe estar vacío.
2. El ID no debe estar repetido.
3. El nombre del cliente no debe estar vacío.
4. El tipo de producto debe estar permitido.
5. El ancho debe ser mayor que cero.
6. El largo debe ser mayor que cero.
7. La cantidad debe ser un número entero mayor que cero.
8. Los campos numéricos deben convertirse correctamente.
9. Los pedidos incorrectos deben clasificarse como OBSERVADO.
10. El sistema debe mostrar el motivo de la observación.

## Productos permitidos

Banda Transportadora.
Cinta de Transmisión.

## Estructuras de programación utilizadas

Ciclo for para recorrer las filas del archivo.
Condicionales if, elif y else para aplicar las validaciones.
Listas para almacenar los pedidos procesados.
Cadenas para comparar identificadores, clientes y productos.
Manejo de errores para controlar datos numéricos incorrectos.
Acumuladores para consolidar los resultados.

## Resultado esperado

Los pedidos que cumplan todas las validaciones continúan con el cálculo del subtotal, IGV e importe total.

Los pedidos que presenten errores se registran como OBSERVADO y no se incorporan al monto total válido facturado.
