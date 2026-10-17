
from services.json_service import JsonService

servicio = JsonService()

print("Exportando canciones...")
cantidad = servicio.exportar_canciones()
print(f"Canciones exportadas: {cantidad}")

print("\nProbando importación...")
insertadas = servicio.importar_canciones()
print(f"Canciones nuevas importadas: {insertadas}")

print("\nPrueba finalizada.")
