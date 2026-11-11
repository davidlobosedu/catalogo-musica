
from database.db import inicializar_db
from models.cancion import Cancion
from repositories.cancion_repository import CancionRepository
from services.catalogo import Catalogo


inicializar_db()

repositorio = CancionRepository()
catalogo = Catalogo()

print("=== PRUEBA DE FUNCIONALIDAD: SEGUNDOS TOTALES DE LA LISTA ===")

# 1. Prueba con la lista completa de canciones
canciones_todas = catalogo.listar_canciones()
total_segundos = catalogo.calcular_segundos_totales(canciones_todas)
tiempo_formateado = Catalogo.formatear_duracion(total_segundos)

print(f"Cantidad de canciones en catálogo: {len(canciones_todas)}")
print(f"Segundos totales calculados: {total_segundos} segundos")
print(f"Tiempo formateado: {tiempo_formateado}")

# Verificación manual de la suma
suma_manual = sum(c.duracion for c in canciones_todas)
assert total_segundos == suma_manual, "Error: la suma de segundos no coincide"
print("✓ Verificación de suma total: CORRECTO")

# 2. Prueba llamando al método sin argumentos (por defecto usa todas las canciones)
total_defecto = catalogo.calcular_segundos_totales()
assert total_defecto == total_segundos, "Error: el valor por defecto no coincide"
print("✓ Verificación con argumento por defecto: CORRECTO")

# 3. Prueba con una lista filtrada (por ejemplo una búsqueda)
if canciones_todas:
    canciones_subconjunto = canciones_todas[:3]
    total_subconjunto = catalogo.calcular_segundos_totales(canciones_subconjunto)
    suma_esperada = sum(c.duracion for c in canciones_subconjunto)
    assert total_subconjunto == suma_esperada
    print(f"✓ Subconjunto de {len(canciones_subconjunto)} canciones: {total_subconjunto} s ({Catalogo.formatear_duracion(total_subconjunto)}) - CORRECTO")

# 4. Prueba con lista vacía
assert catalogo.calcular_segundos_totales([]) == 0
assert Catalogo.formatear_duracion(0) == "0 s"
print("✓ Verificación con lista vacía: CORRECTO")

print("\n¡Todas las pruebas de segundos totales pasaron exitosamente!")
