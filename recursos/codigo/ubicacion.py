
from IPython.display import HTML, display

def mostrar_ubicacion(latitud: float, longitud: float) -> None:
    """
    Abre la ubicación indicada en OpenStreetMap.

    Parameters
    ----------
    latitud : float
        Latitud de la ubicación.

    longitud : float
        Longitud de la ubicación.
    """

    if not isinstance(latitud, (int, float)) or not -90 <= latitud <= 90:
        print("Latitud inválida.")
        return

    if not isinstance(longitud, (int, float)) or not -180 <= longitud <= 180:
        print("Longitud inválida.")
        return

    url = (
        f"https://www.openstreetmap.org/"
        f"?mlat={latitud}&mlon={longitud}"
        f"#map=10/{latitud}/{longitud}"
    )

    display(HTML(f'<a href="{url}" target="_blank">🗺️ Abrir mapa</a>'))