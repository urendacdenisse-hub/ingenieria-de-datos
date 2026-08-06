import math
import matplotlib.pyplot as plt
import pandas as pd

from textwrap import fill
from pandas.api.types import (
    is_bool_dtype,
    is_numeric_dtype,
    is_object_dtype,
)


def visualizar_resultados(datos, max_categorias=10):

    columnas_categoricas = []
    columnas_ignoradas = []

    # Identificar las variables categóricas
    for columna in datos.columns:

        serie = datos[columna]
        numero_categorias = serie.nunique(dropna=True)

        es_categorica = (
            isinstance(serie.dtype, pd.CategoricalDtype)
            or is_object_dtype(serie)
            or is_bool_dtype(serie)
            or (
                is_numeric_dtype(serie)
                and numero_categorias <= max_categorias
            )
        )

        if es_categorica:
            columnas_categoricas.append(columna)
        else:
            columnas_ignoradas.append(columna)

    # Informar qué columnas no serán utilizadas
    if columnas_ignoradas:
        print(
            "Las siguientes variables no son categóricas y no serán graficadas:"
        )

        for columna in columnas_ignoradas:
            print(f"   • {columna}")

    # Terminar si no existen variables categóricas
    if not columnas_categoricas:
        print(
            "No se encontraron variables categóricas para visualizar."
        )
        return None

    numero_graficas = len(columnas_categoricas)

    # Organizar automáticamente las gráficas
    numero_columnas = min(2, numero_graficas)
    numero_filas = math.ceil(numero_graficas / numero_columnas)

    fig, axes = plt.subplots(
        numero_filas,
        numero_columnas,
        figsize=(8, 3 * numero_filas),
        sharey=True,
        squeeze=False,
    )

    axes = axes.ravel()

    for i, columna in enumerate(columnas_categoricas):

        serie = datos[columna].dropna()

        # Conservar todas las categorías definidas, aunque alguna no aparezca
        if isinstance(serie.dtype, pd.CategoricalDtype):
            categorias = list(serie.cat.categories)

        else:
            categorias = list(serie.unique())

            # Ordenarlas cuando los valores sean comparables
            try:
                categorias = sorted(categorias)
            except TypeError:
                categorias = sorted(categorias, key=str)

        frecuencias = (
            serie
            .value_counts()
            .reindex(categorias, fill_value=0)
        )

        frecuencia_maxima = frecuencias.max()

        colores = [
            "indianred" if frecuencia == frecuencia_maxima
            else "steelblue"
            for frecuencia in frecuencias
        ]

        frecuencias.plot.bar(
            ax=axes[i],
            color=colores,
            width=0.8,
        )

        # Mostrar el promedio únicamente en variables numéricas
        if is_numeric_dtype(serie):

            media = serie.mean()

            axes[i].set_title(
                f"Promedio: {media:.2f}",
                fontsize=9,
                color="gray",
            )

        # Pregunta o nombre de la variable
        axes[i].set_xlabel(
            fill(str(columna), width=45),
            fontsize=11,
        )

        axes[i].set_ylabel("")

        axes[i].tick_params(
            axis="x",
            rotation=0,
        )

        axes[i].tick_params(
            axis="y",
            left=False,
            labelleft=False,
        )

        axes[i].spines["left"].set_visible(False)
        axes[i].spines["right"].set_visible(False)
        axes[i].spines["top"].set_visible(False)

        # Mostrar la frecuencia sobre cada barra
        for barra in axes[i].patches:

            altura = barra.get_height()

            axes[i].text(
                barra.get_x() + barra.get_width() / 2,
                altura,
                f"{int(altura)}",
                ha="center",
                va="bottom",
                fontsize=9,
                color=barra.get_facecolor(),
            )

    # Ocultar espacios sobrantes del layout
    for eje in axes[numero_graficas:]:
        eje.axis("off")

    fig.tight_layout()

    return fig