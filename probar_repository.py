
from database.db import inicializar_db
from models.cancion import Cancion
from repositories.cancion_repository import CancionRepository


# Preparar la tabla.
inicializar_db()

# Crear el repositorio.
repositorio = CancionRepository()

# Insertar una canción de prueba si todavía no existe.
cancion = repositorio.obtener_por_codigo(1)

if cancion is None:
    cancion = Cancion(
        1,
        "De música ligera",
        "Soda Stereo",
        "Canción animal",
        1990,
        218
    )

    repositorio.insertar(cancion)
    print("Canción insertada correctamente.")
else:
    print("La canción de prueba ya existe.")

# Consultar todas las canciones.
print("\nListado de canciones:")

for cancion in repositorio.obtener_todas():
    print(cancion)

# Buscar una canción por código.
print("\nBúsqueda por código:")

cancion = repositorio.obtener_por_codigo(1)

if cancion is not None:
    print(cancion)
else:
    print("No se encontró la canción.")
