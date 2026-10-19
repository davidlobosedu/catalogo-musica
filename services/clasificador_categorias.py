
from repositories.cancion_repository import CancionRepository
from structures.arbol_categorias import ArbolCategorias


def clasificar_cancion(cancion):
    """
    Clasificar según el género guardado en la canción.
    Si el género no corresponde a una categoría existente,
    utilizar reglas por artista como alternativa.
    """
    genero = (cancion.genero or "").strip().casefold()

    generos_validos = {
        "rock argentino": "Rock Argentino",
        "rock internacional": "Rock internacional",
        "pop": "Pop",
        "folclore": "Folclore",
    }

    if genero in generos_validos:
        return generos_validos[genero]

    # Compatibilidad con canciones antiguas o sin género reconocido.
    artista = cancion.artista.casefold()

    artistas_rock_argentino = {
        "la renga",
        "sumo",
        "divididos",
        "los enanitos verdes",
        "los abuelos de la nada",
        "andres calamaro",
        "gustavo cerati",
        "luis alberto spinetta",
        "almendra",
        "sui generis",
        "seru giran",
        "patricio rey y sus redonditos de ricota",
        "los fabulosos cadillacs",
    }

    artistas_folclore = {
        "mercedes sosa",
        "daniel toro",
    }

    artistas_pop = {
        "madonna",
        "michael jackson",
        "abba",
    }

    if artista in artistas_rock_argentino:
        return "Rock Argentino"

    if artista in artistas_folclore:
        return "Folclore"

    if artista in artistas_pop:
        return "Pop"

    return "Rock internacional"


def cargar_categorias():
    """Construir el árbol con las canciones almacenadas en SQLite."""
    repositorio = CancionRepository()
    arbol = ArbolCategorias()

    canciones = repositorio.obtener_todas()

    for cancion in canciones:
        categoria = clasificar_cancion(cancion)
        arbol.agregar_cancion(categoria, cancion)

    return arbol


if __name__ == "__main__":
    arbol = cargar_categorias()

    for categoria in arbol.listar_categorias():
        print(categoria)

    print("\nResumen de canciones por categoría:")

    for nombre in [
        "Rock Argentino",
        "Rock internacional",
        "Pop",
        "Folclore",
    ]:
        nodo = arbol.buscar_categoria(nombre)

        if nodo is not None:
            print(f"{nombre}: {len(nodo.canciones)} canciones")
