
from database.db import inicializar_db
from models.cancion import Cancion
from repositories.cancion_repository import CancionRepository
from services.catalogo import Catalogo


inicializar_db()

repositorio = CancionRepository()
catalogo = Catalogo()

codigo_prueba = 9998

try:
    # Preparar una canción conocida para la prueba.
    if repositorio.obtener_por_codigo(codigo_prueba) is not None:
        repositorio.eliminar(codigo_prueba)

    cancion = Cancion(
        codigo_prueba,
        "Persiana americana",
        "Soda Stereo",
        "Signos",
        1986,
        270,
        "Rock Argentino"
    )

    repositorio.insertar(cancion)

    # Probar la búsqueda por título.
    resultados, comparaciones = catalogo.buscar_por_titulo(
        "Persiana americana"
    )

    print("Búsqueda por título:")
    print("Resultados encontrados:", len(resultados))
    print("Comparaciones:", comparaciones)

    for cancion in resultados:
        print(cancion)

    # Probar la búsqueda por artista.
    resultados, comparaciones = catalogo.buscar_por_artista(
        "Soda Stereo"
    )

    print("\nBúsqueda por artista:")
    print("Resultados encontrados:", len(resultados))
    print("Comparaciones:", comparaciones)

    # Probar la búsqueda por álbum.
    resultados, comparaciones = catalogo.buscar_por_album(
        "Signos"
    )

    print("\nBúsqueda por álbum:")
    print("Resultados encontrados:", len(resultados))
    print("Comparaciones:", comparaciones)

finally:
    # Eliminar la canción temporal.
    repositorio.eliminar(codigo_prueba)
