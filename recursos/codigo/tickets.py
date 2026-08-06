from datetime import datetime


def generar_ticket(productos):
    """
    Genera un ticket de compra.

    Parameters
    ----------
    productos : list[tuple]
        Lista de tuplas con el formato:
        (nombre_producto, cantidad, precio_unitario)
    """

    if not isinstance(productos, list):
        return "La lista de productos es inválida."

    for producto in productos:

        if not isinstance(producto, tuple):
            return "La lista de productos es inválida."

        if len(producto) != 3:
            return "La lista de productos es inválida."

        nombre, cantidad, precio = producto

        if not isinstance(nombre, str):
            return "El nombre del producto debe ser texto."
        
        if not nombre.strip():
            return "El nombre del producto no puede estar vacío."

        if not isinstance(cantidad, int) or cantidad <= 0:
            return "La cantidad debe ser un número entero mayor que cero."

        if not isinstance(precio, (int, float)) or precio <= 0:
            return "El precio debe ser un número mayor que cero."

    subtotal = sum(cantidad * precio for _, cantidad, precio in productos)
    iva = subtotal * 0.16
    total = subtotal + iva

    ancho = 65

    encabezado = f"""
{'=' * ancho}
{'NOVA RETAIL MÉXICO':^{ancho}}
{'Sucursal: Ciudad Juárez Centro':^{ancho}}
{'Av. Tecnológico #1450':^{ancho}}
{'Tel. (656) 123-4567':^{ancho}}
{'=' * ancho}
Fecha : {datetime.now():%d/%m/%Y %H:%M:%S}
Caja  : 03
Cajero: Ana Martínez
Ticket: NR-2026000185
{'-' * ancho}
{'Producto':<28}{'Cant.':>7}{'P.U.':>13}{'Importe':>15}
{'-' * ancho}
"""

    detalle = ""

    for nombre, cantidad, precio in productos:
        importe = cantidad * precio
        detalle += (
            f"{nombre:<28}"
            f"{cantidad:>7}"
            f"{f'$ {precio:,.2f}':>13}"
            f"{f'$ {importe:,.2f}':>15}\n"
        )

    pie = f"""
{'-' * ancho}
{'Subtotal':>49}{f'$ {subtotal:,.2f}':>15}
{'IVA (16%)':>49}{f'$ {iva:,.2f}':>15}
{'=' * ancho}
{'TOTAL':>49}{f'$ {total:,.2f}':>15}
{'=' * ancho}
Forma de pago : Tarjeta de crédito
Cliente       : Público en general
RFC           : XAXX010101000

¡Gracias por su compra!
Conserve este comprobante.
{'=' * ancho}
"""

    ticket = encabezado + detalle + pie

    return ticket