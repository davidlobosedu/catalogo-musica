
from database.db import inicializar_db
from models.cancion import Cancion
from repositories.cancion_repository import CancionRepository


inicializar_db()
repositorio = CancionRepository()

# 1. Insertar una canción de prueba.
codigo_prueba = 9999

cancion = repositorio.obtener_por_codigo(codigo_prueba)

if cancion is None:
    cancion = Cancion(
        codigo_prueba,
        "Cancion de prueba",
        "Artista de prueba",
        "Album de prueba",
        2020,
        180,
        genero="Desconocido"
    )

    repositorio.insertar(cancion)
    print("1. Canción insertada.")
else:
    print("1. La canción de prueba ya existía.")

# 2. Consultar la canción.
cancion = repositorio.obtener_por_codigo(codigo_prueba)

if cancion is not None:
    print("2. Canción encontrada:", cancion)

# 3. Modificar la canción.
cancion.titulo = "Cancion modificada"
cancion.artista = "Artista actualizado"

if repositorio.modificar(cancion):
    print("3. Canción modificada.")

# Verificar la modificación.
cancion = repositorio.obtener_por_codigo(codigo_prueba)
print("Título actualizado:", cancion.titulo)

# 4. Eliminar la canción de prueba.
if repositorio.eliminar(codigo_prueba):
    print("4. Canción eliminada.")

# Verificar la eliminación.
cancion = repositorio.obtener_por_codigo(codigo_prueba)

if cancion is None:
    print("5. Confirmado: la canción ya no existe.")
