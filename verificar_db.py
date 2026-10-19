
import sqlite3

conexion = sqlite3.connect("catalogo.db")

cursor = conexion.execute("PRAGMA table_info(canciones)")
columnas = cursor.fetchall()

print("Columnas de la tabla canciones:\n")

for columna in columnas:
    print(f"- {columna[1]}")

if any(columna[1] == "genero" for columna in columnas):
    print("\nOK: la columna 'genero' existe.")
else:
    print("\nFALTA: la columna 'genero' no existe.")

conexion.close()
