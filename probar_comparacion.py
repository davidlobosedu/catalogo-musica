
from repositories.cancion_repository import CancionRepository
from structures.arbol_busqueda import ArbolBusqueda

repositorio = CancionRepository()
canciones = repositorio.obtener_todas()

arbol = ArbolBusqueda()

for cancion in canciones:
    arbol.insertar(cancion)

# Buscamos un código que exista en la base de datos.
codigo_buscado = 20

# Búsqueda secuencial en la lista.
comparaciones_lista = 0
resultado_lista = None

for cancion in canciones:
    comparaciones_lista += 1

    if cancion.codigo == codigo_buscado:
        resultado_lista = cancion
        break

# Búsqueda en el árbol binario.
resultado_arbol, comparaciones_arbol = arbol.buscar(codigo_buscado)

print("=== COMPARACIÓN DE BÚSQUEDAS ===")
print(f"Canciones cargadas: {len(canciones)}")
print(f"Código buscado: {codigo_buscado}")

print("\nBúsqueda secuencial:")
print("Resultado:", resultado_lista)
print("Comparaciones:", comparaciones_lista)

print("\nBúsqueda en árbol binario:")
print("Resultado:", resultado_arbol)
print("Comparaciones:", comparaciones_arbol)

print("\n¿Ambos métodos encontraron la canción?")
print(resultado_lista is not None and resultado_arbol is not None)
