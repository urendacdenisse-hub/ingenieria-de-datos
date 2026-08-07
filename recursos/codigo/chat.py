
import json
from datetime import datetime

from .rutas import RUTA_ENTRADA

def buscar_chat(fecha: str) -> str:
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        return "Formato de fecha inválido. Utilice el formato AAAA-MM-DD."
    
    with open(RUTA_ENTRADA /"chats.json", "r", encoding="utf-8") as archivo:
        historial = json.load(archivo)

    conversaciones = [
        mensaje
        for mensaje in historial
        if mensaje["fecha"] == fecha
    ]

    if not conversaciones:
        return (
            "============================================================\n"
            "                 HISTORIAL DE CONVERSACIONES\n"
            "============================================================\n\n"
            f"Fecha buscada : {fecha}\n\n"
            "No se encontraron conversaciones para esa fecha."
        )

    resultado = (
        "============================================================\n"
        "                 HISTORIAL DE CONVERSACIONES\n"
        "============================================================\n\n"
        f"Fecha : {fecha}\n\n"
    )

    for mensaje in conversaciones:
        resultado += (
            f"[{mensaje['hora']}] {mensaje['usuario']}\n"
            f"{mensaje['mensaje']}\n\n"
        )

    resultado += "=" * 60

    return resultado