
from structures.arbol_categorias import ArbolCategorias
from models.cancion import Cancion


arbol = ArbolCategorias()

# Mostrar todas las categorías.
print("Categorías del catálogo:")

for categoria in arbol.listar_categorias():
    print(categoria)

# Crear una canción de prueba.
cancion = Cancion(
    5000,
    "De música ligera",
    "Soda Stereo",
    "Canción animal",
    1990,
    218
)

# Agregar la canción a Rock Argentino.
agregada = arbol.agregar_cancion(
    "Rock Argentino",
    cancion
)

print("\n¿Canción agregada?", agregada)

# Buscar la categoría y mostrar sus canciones.
categoria = arbol.buscar_categoria("Rock Argentino")

if categoria is not None:
    print("\nCanciones de Rock Argentino:")

    for cancion in categoria.canciones:
        print(cancion)

# Probar una categoría inexistente.
categoria = arbol.buscar_categoria("Jazz")

print("\n¿Existe Jazz?", categoria is not None)
