
from services.historial import HistorialOperaciones

historial = HistorialOperaciones()

cancion = {
    "codigo": 31,
    "titulo": "Hablando de la Libertad",
    "artista": "La Renga"
}

print("¿Historial vacío?", historial.esta_vacio())

historial.registrar("agregar", cancion)
historial.registrar(
    "modificar",
    {"codigo": 31, "titulo_anterior": "Hablando de la Libertad"}
)
historial.registrar(
    "eliminar",
    {"codigo": 31, "titulo": "Hablando de la Libertad"}
)

print("Cantidad de operaciones:", historial.cantidad())
print("Última operación:", historial.obtener_ultima())

print("Operación retirada:", historial.deshacer_ultima())
print("Cantidad restante:", historial.cantidad())
print("Nueva última operación:", historial.obtener_ultima())

