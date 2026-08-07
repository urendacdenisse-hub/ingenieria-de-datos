from pathlib import Path
from urllib.request import Request, urlopen

from IPython.display import Image as DisplayImage
from IPython.display import display
from PIL import Image as PILImage
from PIL import ImageFilter

from rutas import RUTA_ENTRADA, RUTA_SALIDA

EXTENSIONES_IMAGEN = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
)

def cargar_imagen(ruta: str) -> PILImage.Image | None:
    """
    Carga una imagen desde disco.

    Parameters
    ----------
    ruta : str
        Nombre del archivo o ruta completa de la imagen.

    Returns
    -------
    PILImage.Image | None
        Objeto Image o None si ocurrió un error.
    """

    ruta = Path(ruta)

    # Si solo recibió un nombre de archivo, buscar en Datos/Entrada.
    if ruta.parent == Path("."):
        ruta = RUTA_ENTRADA / ruta

    if not ruta.exists():
        print("No se encontró la imagen.")
        return None

    try:
        return PILImage.open(ruta)

    except Exception:
        print("No fue posible abrir la imagen.")
        return None




def descargar_imagen(
    url: str,
    nombre_archivo: str,
) -> str | None:
    """
    Descarga una imagen desde Internet.

    Parameters
    ----------
    url : str
        Dirección web de la imagen.

    nombre_archivo : str
        Nombre con el que se guardará la imagen.

    Returns
    -------
    str | None
        Ruta donde se guardó la imagen o None si ocurrió un error.
    """

    if not url.startswith("https://"):
        print("La dirección debe utilizar el protocolo HTTPS.")
        return None

    if not nombre_archivo.lower().endswith(EXTENSIONES_IMAGEN):
        print("El nombre del archivo debe tener una extensión de imagen.")
        return None

    RUTA_SALIDA.mkdir(parents=True, exist_ok=True)
    ruta = RUTA_SALIDA / nombre_archivo

    try:
        request = Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        with urlopen(request) as respuesta:
            tipo_contenido = respuesta.headers.get_content_type()

            if not tipo_contenido.startswith("image/"):
                print(
                    "La dirección proporcionada no corresponde a una imagen."
                )
                return None

            with open(ruta, "wb") as archivo:
                archivo.write(respuesta.read())

        return str(ruta)

    except Exception:
        if ruta.exists():
            ruta.unlink()

        print(
            "No fue posible descargar la imagen.\n"
            "Verifique la conexión a Internet "
            "o la dirección proporcionada."
        )
        return None




def mostrar_imagen(origen: str) -> None:
    """
    Muestra una imagen desde una ruta local o una URL.

    Parameters
    ----------
    origen : str
        Ruta local o dirección web de la imagen.
    """

    if origen.startswith(("http://", "https://")):
        display(DisplayImage(url=origen))
        return

    imagen = cargar_imagen(origen)

    if imagen is None:
        return

    try:
        display(imagen)

    finally:
        imagen.close()



def aplicar_filtro(
    ruta_imagen: str,
    filtro: str,
    nombre_salida: str,
) -> str | None:
    """
    Aplica un filtro a una imagen y guarda el resultado.

    Parameters
    ----------
    ruta_imagen : str
        Ruta de la imagen original.

    filtro : str
        Nombre del filtro que se aplicará.

    Filtros disponibles:
    - "contorno"
    - "bordes"
    - "relieve"
    - "nitidez"

    nombre_salida : str
        Nombre de la imagen modificada.

    Returns
    -------
    str | None
        Ruta de la imagen modificada o None si ocurrió un error.
    """

    if not nombre_salida.lower().endswith(EXTENSIONES_IMAGEN):
        print("El nombre de salida debe tener una extensión de imagen.")
        return None

    RUTA_SALIDA.mkdir(parents=True, exist_ok=True)
    ruta_salida = RUTA_SALIDA / nombre_salida

    filtros = {
        "bordes": ImageFilter.FIND_EDGES,
        "contorno": ImageFilter.CONTOUR,
        "relieve": ImageFilter.EMBOSS,
        "nitidez": ImageFilter.SHARPEN,
    }

    if filtro not in filtros:
        opciones = ", ".join(filtros)
        print(f"Filtro inválido. Opciones disponibles: {opciones}.")
        return None

    imagen = cargar_imagen(ruta_imagen)

    if imagen is None:
        return None

    try:
        imagen_modificada = imagen.filter(filtros[filtro])
        imagen_modificada.save(ruta_salida)

        return str(ruta_salida)

    except Exception:
        print("No fue posible modificar la imagen.")
        return None

    finally:
        imagen.close()


def redimensionar_imagen(
    ruta_imagen: str,
    ancho: int,
    alto: int,
    nombre_salida: str,

) -> str | None:
    imagen = cargar_imagen(ruta_imagen)

    if imagen is None:
        return None

    if not nombre_salida.lower().endswith(EXTENSIONES_IMAGEN):
        print("El nombre de salida debe tener una extensión de imagen.")
        return None

    RUTA_SALIDA.mkdir(parents=True, exist_ok=True)
    ruta_salida = RUTA_SALIDA / nombre_salida

    try:
        imagen_modificada = imagen.resize((ancho, alto))
        imagen_modificada.save(ruta_salida)

        return str(ruta_salida)

    except Exception:
        print("No fue posible redimensionar la imagen.")
        return None

    finally:
        imagen.close()


def rotar_imagen(
    ruta_imagen: str,
    grados: float,
    nombre_salida: str,
) -> str | None:
    """
    Rota una imagen y guarda el resultado.

    Parameters
    ----------
    ruta_imagen : str
        Ruta de la imagen original.

    grados : float
        Ángulo de rotación en grados.

    nombre_salida : str
        Nombre de la imagen rotada.

    Returns
    -------
    str | None
        Ruta de la imagen rotada o None si ocurrió un error.
    """

    if not nombre_salida.lower().endswith(EXTENSIONES_IMAGEN):
        print("El nombre de salida debe tener una extensión de imagen.")
        return None

    RUTA_SALIDA.mkdir(parents=True, exist_ok=True)
    ruta_salida = RUTA_SALIDA / nombre_salida

    imagen = cargar_imagen(ruta_imagen)

    if imagen is None:
        return None

    try:
        imagen_rotada = imagen.rotate(
            grados,
            expand=True,
        )

        imagen_rotada.save(ruta_salida)

        return str(ruta_salida)

    except Exception:
        print("No fue posible rotar la imagen.")
        return None

    finally:
        imagen.close()