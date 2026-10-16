
from database.db import inicializar_db, obtener_conexion


# Crear la tabla de canciones.
inicializar_db()

print("Base de datos inicializada correctamente.")

# Consultar las tablas existentes.
conexion = obtener_conexion()

try:
    cursor = conexion.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
    """)

    tablas = cursor.fetchall()

    print("Tablas encontradas:")

    for tabla in tablas:
        print("-", tabla[0])

finally:
    conexion.close()
