# Estructura del archivo CSV y datos de prueba

## Responsable

Jorge Erqueaga Rivera

## Actividad relacionada

US-01 Definir estructura del CSV y datos de prueba.

## Objetivo

Definir la estructura de los pedidos utilizados por el sistema de validación de FM Industrial y preparar casos que permitan comprobar el funcionamiento del programa.

## Estructura del archivo pedidos_fm_industrial.csv

El archivo contiene las siguientes columnas:

- ID_Pedido: código único que identifica cada pedido.
- Cliente: nombre o razón social del cliente.
- Tipo_Faja: producto solicitado por el cliente.
- Ancho_Pulgadas: ancho de la faja expresado en pulgadas.
- Largo_Metros: longitud solicitada expresada en metros.
- Cantidad: número de unidades solicitadas.

## Tipos de productos permitidos

- Banda Transportadora.
- Cinta de Transmisión.

## Casos de prueba válidos

Los pedidos válidos deben cumplir con las siguientes condiciones:

- Tener un ID único.
- Contener el nombre del cliente.
- Utilizar uno de los productos permitidos.
- Tener ancho mayor que cero.
- Tener largo mayor que cero.
- Tener cantidad mayor que cero.

## Casos de prueba observados

Se incluyeron registros con errores intencionales para comprobar las validaciones:

- Producto no permitido.
- Largo igual o menor que cero.
- Cantidad inválida.
- Campos vacíos.
- Identificadores repetidos.

## Resultado esperado

Los pedidos correctos deben clasificarse como VALIDADO.

Los pedidos incorrectos deben clasificarse como OBSERVADO y mostrar el motivo de la observación.
