import random

from datetime import datetime
from .utils import (
    barra, leer_texto, leer_fecha, leer_correo, 
    leer_url, leer_si_no, leer_entero
)

def capturar_datos():

    print("=" * 70)
    print("      SISTEMA INTELIGENTE DE CAPTURA DE INFORMACIÓN")
    print("                     SICAI v1.0")
    print("=" * 70)

    barra("Conectando con el sistema...")

    print("Complete la siguiente información.\n")

    nombre = leer_texto("👤 Nombre completo: ", 45)

    nacimiento = leer_fecha()

    hoy = datetime.today()

    edad = hoy.year - nacimiento.year

    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        edad -= 1

    ciudad = leer_texto("📍 Ciudad: ", 45)

    correo = leer_correo()

    pagina = leer_url()

    estudiante = leer_si_no("🎓 ¿Actualmente estudias?")

    if estudiante:

        carrera = leer_texto("📚 Carrera: ", 45)
        semestre = leer_entero("📖 Semestre: ")

    else:

        carrera = "No aplica"
        semestre = "-"

    trabaja = leer_si_no("💼 ¿Actualmente trabajas?")

    if trabaja:

        empresa = leer_texto("🏢 Empresa: ", 45)
        puesto = leer_texto("💻 Puesto: ", 45)
        experiencia = leer_entero("📅 Años de experiencia: ")

    else:

        empresa = "No aplica"
        puesto = "No aplica"
        experiencia = "-"

    color = leer_texto("🎨 Color favorito: ", 45)
    comida = leer_texto("🍕 Comida favorita: ", 45)
    pasatiempo = leer_texto("🎯 Pasatiempo favorito: ", 45)

    descripcion = leer_texto("💬 Cuéntanos algo sobre ti: ", 200)

    # ------------------------------------------------------

    barra("Generando reporte...")

    # ------------------------------------------------------

    if estudiante and trabaja:
        resumen = "Actualmente combina sus estudios con una actividad laboral."

    elif estudiante:
        resumen = "Actualmente se dedica principalmente a sus estudios."

    elif trabaja:
        resumen = "Actualmente participa en el mercado laboral."

    else:
        resumen = "Actualmente no reportó estudios ni actividad laboral."

    folio = f"SICAI-{random.randint(100000,999999)}"

    reporte = f"""
╔════════════════════════════════════════════════════════════════════╗
║                  REPORTE DE INFORMACIÓN PERSONAL                   ║
╚════════════════════════════════════════════════════════════════════╝

Folio del reporte : {folio}
Fecha de emisión  : {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

══════════════════════════════════════════════════════════════════════

👤 DATOS PERSONALES

Nombre completo : {nombre}
Edad aproximada : {edad} años
Ciudad          : {ciudad}
Correo          : {correo}
Página web      : {pagina}

══════════════════════════════════════════════════════════════════════

🎓 INFORMACIÓN ACADÉMICA

¿Estudia?       : {"Sí" if estudiante else "No"}
Carrera         : {carrera}
Semestre        : {semestre}

══════════════════════════════════════════════════════════════════════

💼 INFORMACIÓN LABORAL

¿Trabaja?       : {"Sí" if trabaja else "No"}
Empresa         : {empresa}
Puesto          : {puesto}
Experiencia     : {experiencia}

══════════════════════════════════════════════════════════════════════

🎨 PREFERENCIAS

Color favorito  : {color}
Comida favorita : {comida}
Pasatiempo      : {pasatiempo}

══════════════════════════════════════════════════════════════════════

📝 DESCRIPCIÓN

{descripcion}

══════════════════════════════════════════════════════════════════════

🤖 RESUMEN AUTOMÁTICO

{resumen}

El sistema verificó correctamente la información
proporcionada y generó este reporte automáticamente.

Campos procesados : 13

Estado del registro : ✔ COMPLETADO

══════════════════════════════════════════════════════════════════════
"""

    print("✅ Reporte generado correctamente.\n")

    return reporte