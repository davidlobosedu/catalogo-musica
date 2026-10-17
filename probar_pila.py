
from structures.pila import Pila

pila = Pila()

print("¿Está vacía?", pila.esta_vacia())

pila.apilar("Agregar canción")
pila.apilar("Modificar canción")
pila.apilar("Eliminar canción")

print("Cantidad de operaciones:", pila.tamanio())
print("Última operación:", pila.ver_tope())

print("Deshacer:", pila.desapilar())
print("Nueva operación en el tope:", pila.ver_tope())
print("Cantidad restante:", pila.tamanio())
