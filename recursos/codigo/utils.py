
import re
import sys
import time
from textwrap import fill

from datetime import datetime

def barra(mensaje, tiempo=2):
    print(f"\n{mensaje}")

    pasos = 30

    for i in range(pasos + 1):
        porcentaje = int(i / pasos * 100)
        progreso = "█" * i + "░" * (pasos - i)

        sys.stdout.write(f"\r[{progreso}] {porcentaje}%")
        sys.stdout.flush()
        time.sleep(tiempo / pasos)

    print("\n")


def leer_texto(mensaje, max_caracteres, ancho=60):

    ancho = min(max_caracteres, ancho)

    while True:

        dato = input(mensaje)
        dato = " ".join(dato.split())

        if len(dato) == 0:
            print("❌ Este campo no puede quedar vacío.\n")
            continue

        if len(dato) > max_caracteres:
            print(
                f"⚠ El texto supera los {max_caracteres} caracteres.\n"
                f"   Se conservarán únicamente los primeros {max_caracteres}.\n"
            )
            dato = dato[:max_caracteres]

        return fill(dato, width=ancho)


def leer_entero(mensaje, minimo=None, maximo=None):

    while True:

        try:
            numero = int(input(mensaje))

            if minimo is not None and numero < minimo:
                print(f"❌ El número debe ser mayor o igual a {minimo}.\n")
                continue

            if maximo is not None and numero > maximo:
                print(f"❌ El número debe ser menor o igual a {maximo}.\n")
                continue

            return numero

        except ValueError:
            print("❌ Debes escribir un número entero.\n")


def leer_fecha():

    while True:

        dato = input("📅 Fecha de nacimiento (DD/MM/AAAA): ")

        try:
            return datetime.strptime(dato, "%d/%m/%Y")
        except:
            print("❌ Formato incorrecto.\n")


def leer_si_no(mensaje):

    while True:

        dato = input(mensaje + " (Sí/No): ").strip().lower()

        if dato in ["si", "sí", "s", "yes", "y"]:
            return True

        if dato in ["no", "n"]:
            return False

        print("❌ Escribe únicamente Sí o No.\n")


def leer_correo():

    patron = r"^[^@]+@[^@]+\.[^@]+$"

    while True:

        correo = input("📧 Correo electrónico: ").strip()

        if re.match(patron, correo):
            return correo

        print("❌ Correo inválido.\n")


def leer_url():

    while True:

        url = input("🌐 Página web o red social: ").strip()

        if url.startswith("http://") or url.startswith("https://"):
            return url

        print("❌ Debe comenzar con http:// o https://\n")


def leer_decimal(mensaje, minimo=0.01):

    while True:

        dato = input(mensaje).strip().replace("$", "").replace(",", "")

        try:
            numero = float(dato)

            if numero < minimo:
                print(
                    f"❌ El valor debe ser mayor o igual a {minimo}.\n"
                )
                continue

            return round(numero, 2)

        except ValueError:
            print("❌ Introduce un número válido.\n")


def leer_rfc(mensaje):

    patron = r"^[A-ZÑ&]{4}\d{6}[A-Z0-9]{3}$"

    while True:

        rfc = input(mensaje).strip().upper().replace(" ", "")

        if re.fullmatch(patron, rfc):
            return rfc

        print(
            "❌ El RFC no tiene un formato válido.\n"
            "   Ejemplo: UECJ940204ABC\n"
        )


def leer_codigo_postal(mensaje):

    while True:

        codigo_postal = input(mensaje).strip()

        if codigo_postal.isdigit() and len(codigo_postal) == 5:
            return codigo_postal

        print("❌ El código postal debe contener exactamente 5 números.\n")


def leer_tarjeta(mensaje):

    while True:

        tarjeta = input(mensaje)

        tarjeta = tarjeta.replace(" ", "").replace("-", "")

        if tarjeta.isdigit() and len(tarjeta) == 16:
            return tarjeta

        print("❌ La tarjeta debe contener exactamente 16 dígitos.\n")