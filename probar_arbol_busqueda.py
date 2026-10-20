
from models.cancion import Cancion
from structures.arbol_busqueda import ArbolBusqueda

arbol = ArbolBusqueda()

canciones = [
    Cancion(30, "Persiana americana", "Soda Stereo", "Signos", 1986, 270, "Rock Argentino"),
    Cancion(10, "De música ligera", "Soda Stereo", "Canción animal", 1990, 218, "Rock Argentino"),
    Cancion(20, "Lamento boliviano", "Los Enanitos Verdes", "Big Bang", 1994, 210, "Rock Argentino"),
    Cancion(40, "Flaca", "Andrés Calamaro", "Alta suciedad", 1997, 240, "Rock Argentino"),
]

print("Insertando canciones:")
for cancion in canciones:
    agregada = arbol.insertar(cancion)
    print(cancion.codigo, "Agregada:", agregada)

print("\nIntentando insertar un código duplicado:")
print(arbol.insertar(canciones[0]))

print("\nCanciones ordenadas por código:")
for cancion in arbol.listar_inorden():
    print(cancion.codigo, "-", cancion)

print("\nBuscando el código 20:")
cancion, comparaciones = arbol.buscar(20)
print("Resultado:", cancion)
print("Comparaciones:", comparaciones)

print("\nBuscando el código 99:")
cancion, comparaciones = arbol.buscar(99)
print("Resultado:", cancion)
print("Comparaciones:", comparaciones)
