
import sqlite3
from pathlib import Path


# Path carpeta proyecto
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

# Ubicación del archivo de la BD.
RUTA_DB = RUTA_PROYECTO / "catalogo.db"


def obtener_conexion():
    """Crear una conexión con la base de datos."""
    return sqlite3.connect(RUTA_DB)


def inicializar_db():
    """Crear la tabla de canciones si todavía no existe."""
    conexion = obtener_conexion()

    try:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS canciones (
                codigo INTEGER PRIMARY KEY,
                titulo TEXT NOT NULL,
                artista TEXT NOT NULL,
                album TEXT NOT NULL,
                anio INTEGER NOT NULL CHECK (anio > 0),
                duracion INTEGER NOT NULL CHECK (duracion > 0)
            )
        """)

        conexion.commit()

    finally:
        conexion.close()
