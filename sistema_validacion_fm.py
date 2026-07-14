"""
Sistema de validación automatizado para facturación y despacho de FM Industrial.

El programa procesa un archivo CSV de pedidos, valida sus campos, calcula
subtotal, IGV y total, genera un archivo de auditoría y muestra indicadores.
Utiliza únicamente módulos de la biblioteca estándar de Python.
"""

import csv
import os
import unicodedata

COSTO_METRO_BANDA = 65.0
COSTO_METRO_CINTA = 35.0
TASA_IGV = 0.18
LIMITE_ALERTA_TRANSPORTE = 10000.0

ARCHIVO_ENTRADA = "pedidos_fm_industrial.csv"
ARCHIVO_SALIDA = "facturas_validadas.csv"


def quitar_tildes(texto):
    """Devuelve un texto sin tildes para facilitar comparaciones."""
    texto_normalizado = unicodedata.normalize("NFD", texto)
    return "".join(caracter for caracter in texto_normalizado
                   if unicodedata.category(caracter) != "Mn")


def normalizar_tipo(tipo):
    """Normaliza el nombre del producto y devuelve su forma oficial."""
    tipo_limpio = quitar_tildes(tipo.strip().lower())
    if tipo_limpio == "banda transportadora":
        return "Banda Transportadora"
    if tipo_limpio == "cinta de transmision":
        return "Cinta de Transmisión"
    return ""


def tarifa_segun_tipo(tipo_normalizado):
    """Obtiene la tarifa por metro lineal según el tipo de producto."""
    if tipo_normalizado == "Banda Transportadora":
        return COSTO_METRO_BANDA
    return COSTO_METRO_CINTA


def convertir_entero(valor, nombre_campo, minimo, maximo, errores):
    """Convierte y valida un entero; agrega el error a la lista si falla."""
    try:
        numero = int(valor)
        if numero < minimo or numero > maximo:
            errores.append(
                f"{nombre_campo} debe estar entre {minimo} y {maximo}"
            )
            return 0
        return numero
    except ValueError:
        errores.append(f"{nombre_campo} debe ser un número entero")
        return 0


def convertir_real(valor, nombre_campo, minimo, maximo, errores):
    """Convierte y valida un decimal; agrega el error a la lista si falla."""
    try:
        numero = float(valor)
        if numero < minimo or numero > maximo:
            errores.append(
                f"{nombre_campo} debe estar entre {minimo} y {maximo}"
            )
            return 0.0
        return numero
    except ValueError:
        errores.append(f"{nombre_campo} debe ser un número")
        return 0.0


def crear_listas_resultado():
    """Crea y devuelve todas las listas paralelas utilizadas por el sistema."""
    return {
        "ids": [],
        "clientes": [],
        "tipos": [],
        "anchos": [],
        "largos": [],
        "cantidades": [],
        "tarifas": [],
        "subtotales": [],
        "igvs": [],
        "totales": [],
        "estados": [],
        "observaciones": [],
    }


def registrar_resultado(datos, pedido_id, cliente, tipo, ancho, largo,
                         cantidad, tarifa, subtotal, igv, total, estado,
                         observacion):
    """Agrega un pedido a las listas paralelas conservando la misma posición."""
    datos["ids"].append(pedido_id)
    datos["clientes"].append(cliente)
    datos["tipos"].append(tipo)
    datos["anchos"].append(ancho)
    datos["largos"].append(largo)
    datos["cantidades"].append(cantidad)
    datos["tarifas"].append(tarifa)
    datos["subtotales"].append(subtotal)
    datos["igvs"].append(igv)
    datos["totales"].append(total)
    datos["estados"].append(estado)
    datos["observaciones"].append(observacion)


def procesar_archivo(ruta_entrada):
    """Lee el CSV, valida cada fila mediante un ciclo y calcula los importes."""
    datos = crear_listas_resultado()
    ids_leidos = []

    with open(ruta_entrada, "r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.reader(archivo)
        encabezado = next(lector, None)
        encabezado_esperado = [
            "ID_Pedido", "Cliente", "Tipo_Faja", "Ancho_Pulgadas",
            "Largo_Metros", "Cantidad"
        ]

        if encabezado != encabezado_esperado:
            raise ValueError(
                "El archivo no contiene el encabezado esperado: "
                + ", ".join(encabezado_esperado)
            )

        for numero_fila, fila in enumerate(lector, start=2):
            errores = []

            if len(fila) != 6:
                registrar_resultado(
                    datos, f"FILA-{numero_fila}", "", "", 0, 0.0, 0,
                    0.0, 0.0, 0.0, 0.0, "OBSERVADO",
                    "La fila no contiene exactamente 6 columnas"
                )
                continue

            pedido_id = fila[0].strip().upper()
            cliente = fila[1].strip().title()
            tipo_original = fila[2].strip()
            tipo_normalizado = normalizar_tipo(tipo_original)

            if pedido_id == "":
                errores.append("ID_Pedido está vacío")
            elif pedido_id in ids_leidos:
                errores.append("ID_Pedido duplicado")
            else:
                ids_leidos.append(pedido_id)

            if cliente == "":
                errores.append("Cliente está vacío")

            if tipo_normalizado == "":
                errores.append(
                    "Tipo_Faja debe ser Banda Transportadora o Cinta de Transmisión"
                )

            ancho = convertir_entero(
                fila[3].strip(), "Ancho_Pulgadas", 1, 120, errores
            )
            largo = convertir_real(
                fila[4].strip(), "Largo_Metros", 0.01, 500.0, errores
            )
            cantidad = convertir_entero(
                fila[5].strip(), "Cantidad", 1, 100, errores
            )

            if len(errores) == 0:
                tarifa = tarifa_segun_tipo(tipo_normalizado)
                subtotal = round(largo * cantidad * tarifa, 2)
                igv = round(subtotal * TASA_IGV, 2)
                total = round(subtotal + igv, 2)
                estado = "VALIDADO"
                observacion = "Sin observaciones"
                tipo_salida = tipo_normalizado
            else:
                tarifa = 0.0
                subtotal = 0.0
                igv = 0.0
                total = 0.0
                estado = "OBSERVADO"
                observacion = "; ".join(errores)
                tipo_salida = tipo_original

            registrar_resultado(
                datos, pedido_id, cliente, tipo_salida, ancho, largo,
                cantidad, tarifa, subtotal, igv, total, estado, observacion
            )

    return datos


def guardar_archivo_salida(datos, ruta_salida):
    """Genera el archivo de auditoría para facturación y despacho."""
    encabezado = [
        "ID_Pedido", "Cliente", "Tipo_Faja", "Ancho_Pulgadas",
        "Largo_Metros", "Cantidad", "Tarifa_Metro", "Subtotal",
        "IGV", "Total", "Estado", "Observacion"
    ]

    with open(ruta_salida, "w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezado)

        for i in range(len(datos["ids"])):
            escritor.writerow([
                datos["ids"][i],
                datos["clientes"][i],
                datos["tipos"][i],
                datos["anchos"][i],
                datos["largos"][i],
                datos["cantidades"][i],
                f"{datos['tarifas'][i]:.2f}",
                f"{datos['subtotales'][i]:.2f}",
                f"{datos['igvs'][i]:.2f}",
                f"{datos['totales'][i]:.2f}",
                datos["estados"][i],
                datos["observaciones"][i],
            ])


def calcular_indicadores(datos):
    """Recorre las listas y calcula los indicadores para el análisis."""
    cantidad_procesados = len(datos["ids"])
    cantidad_validados = 0
    cantidad_observados = 0
    total_subtotal = 0.0
    total_igv = 0.0
    total_facturado = 0.0
    metros_totales = 0.0
    unidades_totales = 0
    total_bandas = 0.0
    total_cintas = 0.0
    metros_bandas = 0.0
    metros_cintas = 0.0
    posicion_mayor = -1

    for i in range(cantidad_procesados):
        if datos["estados"][i] == "VALIDADO":
            cantidad_validados += 1
            total_subtotal += datos["subtotales"][i]
            total_igv += datos["igvs"][i]
            total_facturado += datos["totales"][i]
            metros_pedido = datos["largos"][i] * datos["cantidades"][i]
            metros_totales += metros_pedido
            unidades_totales += datos["cantidades"][i]

            if datos["tipos"][i] == "Banda Transportadora":
                total_bandas += datos["totales"][i]
                metros_bandas += metros_pedido
            else:
                total_cintas += datos["totales"][i]
                metros_cintas += metros_pedido

            if posicion_mayor == -1 or (
                    datos["totales"][i] > datos["totales"][posicion_mayor]):
                posicion_mayor = i
        else:
            cantidad_observados += 1

    promedio_factura = 0.0
    if cantidad_validados > 0:
        promedio_factura = total_facturado / cantidad_validados

    porcentaje_validados = 0.0
    if cantidad_procesados > 0:
        porcentaje_validados = cantidad_validados * 100 / cantidad_procesados

    return {
        "procesados": cantidad_procesados,
        "validados": cantidad_validados,
        "observados": cantidad_observados,
        "porcentaje_validados": round(porcentaje_validados, 2),
        "subtotal": round(total_subtotal, 2),
        "igv": round(total_igv, 2),
        "facturado": round(total_facturado, 2),
        "promedio_factura": round(promedio_factura, 2),
        "metros": round(metros_totales, 2),
        "unidades": unidades_totales,
        "total_bandas": round(total_bandas, 2),
        "total_cintas": round(total_cintas, 2),
        "metros_bandas": round(metros_bandas, 2),
        "metros_cintas": round(metros_cintas, 2),
        "posicion_mayor": posicion_mayor,
    }


def mostrar_reporte(datos):
    """Muestra el análisis consolidado y una conclusión automática."""
    indicadores = calcular_indicadores(datos)

    print("\n" + "=" * 68)
    print("REPORTE CONSOLIDADO - FM INDUSTRIAL")
    print("=" * 68)
    print(f"Pedidos procesados       : {indicadores['procesados']}")
    print(f"Pedidos validados        : {indicadores['validados']}")
    print(f"Pedidos observados       : {indicadores['observados']}")
    print(f"Porcentaje de validación : {indicadores['porcentaje_validados']:.2f}%")
    print(f"Subtotal acumulado       : S/ {indicadores['subtotal']:.2f}")
    print(f"IGV acumulado            : S/ {indicadores['igv']:.2f}")
    print(f"Total facturado          : S/ {indicadores['facturado']:.2f}")
    print(f"Promedio por factura     : S/ {indicadores['promedio_factura']:.2f}")
    print(f"Metros lineales          : {indicadores['metros']:.2f}")
    print(f"Unidades solicitadas     : {indicadores['unidades']}")
    print("-" * 68)
    print(
        f"Bandas: {indicadores['metros_bandas']:.2f} m | "
        f"S/ {indicadores['total_bandas']:.2f}"
    )
    print(
        f"Cintas: {indicadores['metros_cintas']:.2f} m | "
        f"S/ {indicadores['total_cintas']:.2f}"
    )

    posicion_mayor = indicadores["posicion_mayor"]
    if posicion_mayor != -1:
        print("-" * 68)
        print(
            "Pedido de mayor importe: "
            f"{datos['ids'][posicion_mayor]} - "
            f"{datos['clientes'][posicion_mayor]} - "
            f"S/ {datos['totales'][posicion_mayor]:.2f}"
        )

    print("-" * 68)
    if indicadores["facturado"] > LIMITE_ALERTA_TRANSPORTE:
        print(
            "ALERTA: El total facturado supera S/ 10 000. "
            "Se recomienda revisar la capacidad y prioridad de despacho."
        )
    else:
        print(
            "El volumen económico se encuentra dentro del umbral regular "
            "de despacho."
        )

    if indicadores["observados"] > 0:
        print(
            "CONCLUSIÓN: Existen pedidos observados. Deben corregirse antes "
            "de facturar o preparar el despacho."
        )
    else:
        print(
            "CONCLUSIÓN: Todos los pedidos fueron validados y pueden continuar "
            "al proceso de facturación y despacho."
        )


def mostrar_observados(datos):
    """Lista únicamente los pedidos que requieren corrección."""
    contador = 0
    print("\nPEDIDOS OBSERVADOS")
    print("-" * 68)
    for i in range(len(datos["ids"])):
        if datos["estados"][i] == "OBSERVADO":
            contador += 1
            print(
                f"{datos['ids'][i]:<12} | {datos['clientes'][i]:<22} | "
                f"{datos['observaciones'][i]}"
            )
    if contador == 0:
        print("No existen pedidos observados.")


def buscar_pedido(datos):
    """Busca un pedido por ID utilizando un recorrido repetitivo."""
    codigo = input("Ingrese el ID del pedido: ").strip().upper()
    encontrado = False

    for i in range(len(datos["ids"])):
        if datos["ids"][i] == codigo:
            encontrado = True
            print("\nRESULTADO DE LA BÚSQUEDA")
            print("-" * 68)
            print(f"ID          : {datos['ids'][i]}")
            print(f"Cliente     : {datos['clientes'][i]}")
            print(f"Producto    : {datos['tipos'][i]}")
            print(f"Dimensiones : {datos['anchos'][i]} pulg. x {datos['largos'][i]} m")
            print(f"Cantidad    : {datos['cantidades'][i]}")
            print(f"Total       : S/ {datos['totales'][i]:.2f}")
            print(f"Estado      : {datos['estados'][i]}")
            print(f"Observación : {datos['observaciones'][i]}")
            break

    if not encontrado:
        print(f"El pedido {codigo} no se encuentra registrado.")


def mostrar_menu():
    print("\nSISTEMA DE VALIDACIÓN - FM INDUSTRIAL")
    print("1. Procesar archivo CSV")
    print("2. Mostrar reporte consolidado")
    print("3. Mostrar pedidos observados")
    print("4. Buscar pedido por ID")
    print("0. Salir")


def leer_opcion():
    """Solicita una opción válida mediante un ciclo while."""
    while True:
        try:
            opcion = int(input("Seleccione una opción: "))
            if 0 <= opcion <= 4:
                return opcion
            print("*** Ingrese una opción entre 0 y 4.")
        except ValueError:
            print("*** Debe ingresar un número entero.")


def main():
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta_entrada = os.path.join(carpeta, ARCHIVO_ENTRADA)
    ruta_salida = os.path.join(carpeta, ARCHIVO_SALIDA)
    datos = None

    while True:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == 1:
            try:
                datos = procesar_archivo(ruta_entrada)
                guardar_archivo_salida(datos, ruta_salida)
                print(f"\nArchivo procesado correctamente: {ruta_entrada}")
                print(f"Archivo de salida generado: {ruta_salida}")
                mostrar_reporte(datos)
            except FileNotFoundError:
                print(f"*** No se encontró el archivo: {ruta_entrada}")
            except (ValueError, OSError) as error:
                print(f"*** No se pudo procesar el archivo: {error}")

        elif opcion == 2:
            if datos is None:
                print("*** Primero debe procesar el archivo con la opción 1.")
            else:
                mostrar_reporte(datos)

        elif opcion == 3:
            if datos is None:
                print("*** Primero debe procesar el archivo con la opción 1.")
            else:
                mostrar_observados(datos)

        elif opcion == 4:
            if datos is None:
                print("*** Primero debe procesar el archivo con la opción 1.")
            else:
                buscar_pedido(datos)

        else:
            print("Programa finalizado.")
            break


if __name__ == "__main__":
    main()
