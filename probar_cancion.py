
from models.cancion import Cancion

cancion = Cancion(
    1,
    "De música ligera",
    "Soda Stereo",
    "Canción animal",
    1990,
    218
)

print("Canción original:")
print(cancion)

print("\nModificando el título...")
cancion.titulo = "Persiana americana"
print(cancion)

print("\nProbando una validación...")

try:
    cancion.titulo = ""
except ValueError as error:
    print("Error controlado:", error)

print("\nTítulo actual:", cancion.titulo)
