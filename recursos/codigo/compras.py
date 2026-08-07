import json

from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from email.message import EmailMessage
from email.policy import default

from .rutas import RUTA_SALIDA

from .utils import (
    barra,
    leer_texto,
    leer_entero,
    leer_decimal,
    leer_tarjeta,
    leer_rfc,
    leer_codigo_postal,
    leer_correo
)

def iniciar_compra():

    print("═" * 70)
    print("                 SISTEMA DE COMPRAS")
    print("═" * 70)

    numero_articulos = leer_entero("\n¿Cuántos artículos diferentes desea registrar? ", 0, 10)

    articulos = []

    print("\nArtículos registrados:\n")

    for numero in range(1, numero_articulos + 1):

        nombre = leer_texto("📦 Nombre del artículo: ", 40)
        cantidad = leer_entero("🔢 Cantidad: ", 1)
        precio_unitario = leer_decimal("💲 Precio por unidad: $")

        importe = round(cantidad * precio_unitario, 2)

        articulo = {
            "nombre": nombre,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "importe": importe
        }

        print(
            f"   ✓ {cantidad} × {nombre}"
            f"  (${importe:,.2f})\n"
        )

        articulos.append(articulo)

    barra("Procesando compra...")

    subtotal = round(sum(articulo["importe"] for articulo in articulos), 2)

    compra = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "numero_articulos": numero_articulos,
        "articulos": articulos,
        "subtotal": subtotal
    }

    compra_json = json.dumps(
        compra,
        ensure_ascii=False,
        indent=4
    )

    print("\n" + "═" * 70)
    print("                    RESUMEN DE COMPRA")
    print("═" * 70)

    for articulo in articulos:

        print(
            f"{articulo['cantidad']:>3} × "
            f"{articulo['nombre']:<35} "
            f"${articulo['importe']:>10,.2f}"
        )

    print("─" * 70)
    print(f"{'Subtotal:':>56} ${subtotal:>10,.2f}")
    print("═" * 70)

    print("\n✅ La compra fue registrada correctamente.")
    print("📦 Los datos se almacenaron en formato JSON.")

    return compra_json



def procesar_compra(compra_json):

    try:
        compra = json.loads(compra_json)

    except (json.JSONDecodeError, TypeError):
        raise ValueError(
            "❌ No fue posible leer la información de la compra."
        )

    print("=" * 70)
    print("                     PROCESAR COMPRA")
    print("=" * 70)

    print("\nSeleccione el método de pago:\n")
    print("1. Tarjeta de débito")
    print("2. Tarjeta de crédito")

    opcion_pago = leer_entero("\nSelecciona el método de pago (1-2): ", 1, 2)

    if opcion_pago == 1:
        metodo_pago = "Tarjeta de débito"
    else:
        metodo_pago = "Tarjeta de crédito"

    numero_tarjeta = leer_tarjeta("\n💳 Introduce el número de tarjeta (16 dígitos): ")

    subtotal = compra["subtotal"]
    iva = round(subtotal * 0.16, 2)
    total = round(subtotal + iva, 2)

    barra("Procesando pago...")

    lineas_ticket = [
        "=" * 70,
        "                       TICKET DE COMPRA",
        "=" * 70,
        f"Fecha: {compra['fecha']}",
        "-" * 70,
        f"{'CANT.':<8}"
        f"{'ARTÍCULO':<32}"
        f"{'P. UNIT.':>13}"
        f"{'IMPORTE':>17}",
        "-" * 70
    ]

    for articulo in compra["articulos"]:

        nombre = articulo["nombre"][:30]

        lineas_ticket.append(
            f"{articulo['cantidad']:<8}"
            f"{nombre:<32}"
            f"${articulo['precio_unitario']:>11,.2f}"
            f"${articulo['importe']:>15,.2f}"
        )

    lineas_ticket.extend([
        "-" * 70,
        f"{'Subtotal:':>52} ${subtotal:>15,.2f}",
        f"{'IVA (16%):':>52} ${iva:>15,.2f}",
        f"{'TOTAL:':>52} ${total:>15,.2f}",
        "-" * 70,
        f"Método de pago: {metodo_pago}",
        f"Tarjeta: **** **** **** {numero_tarjeta[-4:]}",
        "=" * 70,
        "                    ¡Gracias por su compra!",
        "=" * 70
    ])

    ticket = "\n".join(lineas_ticket)

    print("\n" + ticket)

    print("\n✅ La compra fue procesada correctamente.")
    print("🧾 El ticket fue almacenado como una cadena de texto.")

    return ticket





def generar_factura(ticket):

    if not isinstance(ticket, str) or not ticket.strip():
        raise ValueError(
            "❌ El ticket no contiene información válida."
        )

    print("=" * 70)
    print("                      GENERAR FACTURA")
    print("=" * 70)

    print("\nIntroduce los datos fiscales del cliente.\n")

    nombre_cliente = leer_texto("👤 Nombre o razón social: ", 80)
    rfc = leer_rfc("🪪 RFC (13 caracteres, por ejemplo: ABCD123456ABC): ")
    codigo_postal = leer_codigo_postal("📍 Código postal fiscal (5 dígitos): ")
    regimen_fiscal = leer_texto("📄 Régimen fiscal: ", 80)
    uso_cfdi = leer_texto("🧾 Uso del CFDI: ",60)

    barra("Generando factura...")

    RUTA_SALIDA.mkdir(parents=True, exist_ok=True)

    fecha = datetime.now()
    nombre_archivo = fecha.strftime("factura_%Y%m%d_%H%M%S.pdf")
    ruta_factura = RUTA_SALIDA / nombre_archivo

    documento = canvas.Canvas(str(ruta_factura), pagesize=letter)

    ancho_pagina, alto_pagina = letter

    margen = 50
    posicion_y = alto_pagina - 50

    documento.setTitle("Factura")

    # Encabezado
    documento.setFont("Helvetica-Bold", 18)

    documento.drawString(
        margen,
        posicion_y,
        "FACTURA"
    )

    documento.setFont("Helvetica", 9)

    documento.drawRightString(
        ancho_pagina - margen,
        posicion_y,
        fecha.strftime("%d/%m/%Y %H:%M:%S")
    )

    posicion_y -= 25

    documento.setFont("Helvetica", 8)

    documento.drawString(
        margen,
        posicion_y,
        "Documento generado con fines educativos."
    )

    posicion_y -= 35

    # Datos fiscales
    documento.setFont("Helvetica-Bold", 11)

    documento.drawString(
        margen,
        posicion_y,
        "DATOS DEL CLIENTE"
    )

    posicion_y -= 20

    documento.setFont("Helvetica", 10)

    datos_cliente = [
        f"Nombre o razón social: {nombre_cliente}",
        f"RFC: {rfc}",
        f"Código postal fiscal: {codigo_postal}",
        f"Régimen fiscal: {regimen_fiscal}",
        f"Uso del CFDI: {uso_cfdi}"
    ]

    for dato in datos_cliente:

        documento.drawString(
            margen,
            posicion_y,
            dato
        )

        posicion_y -= 16

    posicion_y -= 20

    # Información del ticket
    documento.setFont("Helvetica-Bold", 11)

    documento.drawString(
        margen,
        posicion_y,
        "DETALLE DE LA COMPRA"
    )

    posicion_y -= 20

    documento.setFont("Courier", 7)

    for linea in ticket.splitlines():

        if posicion_y < 50:

            documento.showPage()

            posicion_y = alto_pagina - 50

            documento.setFont(
                "Courier",
                7
            )

        documento.drawString(
            margen,
            posicion_y,
            linea[:100]
        )

        posicion_y -= 11

    documento.save()

    print("\n✅ La factura fue generada correctamente.")
    print(f"📄 Ruta del archivo: {ruta_factura.resolve()}")

    return str(ruta_factura)





def enviar_factura(ruta_factura):

    ruta_factura = Path(ruta_factura)

    if not ruta_factura.exists():
        raise FileNotFoundError(
            f"❌ No se encontró la factura:\n{ruta_factura}"
        )

    if ruta_factura.suffix.lower() != ".pdf":
        raise ValueError(
            "❌ El archivo seleccionado debe estar en formato PDF."
        )

    print("=" * 70)
    print("                      ENVIAR FACTURA")
    print("=" * 70)

    correo_destinatario = leer_correo()

    nombre_destinatario = leer_texto("👤 Nombre del destinatario: ", 80)

    asunto = leer_texto("📝 Asunto del correo: ", 100)

    barra("Preparando correo...")

    mensaje = EmailMessage()

    mensaje["From"] = "facturacion@tiendadatos.com"
    mensaje["To"] = correo_destinatario
    mensaje["Subject"] = asunto

    mensaje.set_content(
        f"Hola, {nombre_destinatario}:\n\n"
        "Gracias por realizar su compra con nosotros.\n\n"
        "Adjuntamos la factura electrónica correspondiente a su pedido en formato PDF. "
        "Le sugerimos conservar este documento para futuras consultas.\n\n"
        "Si necesita asistencia adicional, estaremos encantados de ayudarle.\n\n"
        "Este mensaje fue generado automáticamente con fines educativos y no requiere respuesta.\n\n"
        "Saludos cordiales,\n\n"
        "────────────────────────────\n"
        "Departamento de Facturación\n"
        "Tienda Datos\n"
        "facturacion@tiendadatos.com\n"
        "www.tiendadatos.com"
    )

    contenido_pdf = ruta_factura.read_bytes()

    mensaje.add_attachment(
        contenido_pdf,
        maintype="application",
        subtype="pdf",
        filename=ruta_factura.name
    )

    RUTA_SALIDA.mkdir(parents=True, exist_ok=True)

    fecha = datetime.now()
    nombre_archivo = fecha.strftime("correo_factura_%Y%m%d_%H%M%S.eml")
    ruta_correo = RUTA_SALIDA / nombre_archivo

    ruta_correo.write_bytes(mensaje.as_bytes(policy=default))

    barra("Generando archivo .eml...")

    print("\n✅ El correo fue preparado correctamente.")
    print(f"📧 Destinatario: {correo_destinatario}")
    print(f"📎 Archivo adjunto: {ruta_factura.name}")
    print(f"📁 Ruta del correo: {ruta_correo.resolve()}")

    return str(ruta_correo)