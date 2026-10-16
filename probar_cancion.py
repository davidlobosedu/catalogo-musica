
from models.cancion import Cancion

cancion = Cancion(
    1,
    "La Balada del Diablo y La Muerte",
    "La Renga",
    "Despedazado por Mil Partes",
    1996,
    300
)

print(cancion)
print("Código:", cancion.codigo)
print("Título:", cancion.titulo)
print("Artista:", cancion.artista)
print("Álbum:", cancion.album)
print("Año:", cancion.anio)
print("Duración:", cancion.duracion, "segundos")
