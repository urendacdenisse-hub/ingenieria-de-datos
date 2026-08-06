from datetime import datetime


def generar_correo_promocional(nombre: str, correo: str, ciudad: str) -> None:
    sucursales = {
        "Ciudad Juárez": "Sucursal Ciudad Juárez Centro",
        "Chihuahua": "Sucursal Chihuahua Norte",
        "Monterrey": "Sucursal Monterrey Galerías",
        "Torreón": "Sucursal Torreón Oriente",
        "Hermosillo": "Sucursal Hermosillo Centro",
        "Culiacán": "Sucursal Culiacán Tres Ríos",
        "Mérida": "Sucursal Mérida Altabrisa",
        "Puebla": "Sucursal Puebla Angelópolis",
    }

    if correo.count("@") != 1:
        return "Correo electrónico inválido."

    usuario, dominio = correo.split("@")

    if not usuario or not dominio or "." not in dominio:
        return "Correo electrónico inválido."

    sucursal = sucursales.get(ciudad, "Sucursal más cercana")

    mensaje = f"""
=================================================================
                        NOVA RETAIL MÉXICO
=================================================================

De      : promociones@novaretail.com
Para    : {correo}
Asunto  : ¡Tenemos promociones para ti! 🎉

-----------------------------------------------------------------

Hola, {nombre}.

Queremos agradecer tu preferencia.

Este fin de semana podrás disfrutar de promociones
exclusivas en:

📍 {sucursal}

Ciudad  : {ciudad}
Fecha   : {datetime.now():%d/%m/%Y}
Horario : 09:00 - 21:00

Presenta este correo en caja y obtén un
20% de descuento en productos seleccionados.

¡Te esperamos!

-----------------------------------------------------------------

NOVA RETAIL MÉXICO
Siempre cerca de ti.
www.novaretail.com

=================================================================
"""

    return mensaje