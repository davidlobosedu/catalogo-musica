
import sqlite3
from pathlib import Path


# Ruta absoluta a la base de datos del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_DB = BASE_DIR / "catalogo.db"


def obtener_conexion():
    """Abrir una conexión con la base de datos SQLite."""
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row
    return conexion


def inicializar_db():
    """Crear la tabla si no existe y agregar género si falta."""
    conexion = obtener_conexion()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS canciones (
                codigo INTEGER PRIMARY KEY,
                titulo TEXT NOT NULL,
                artista TEXT NOT NULL,
                album TEXT NOT NULL,
                anio INTEGER NOT NULL CHECK (anio > 0),
                duracion INTEGER NOT NULL CHECK (duracion > 0)
            )
        """)

        cursor.execute("PRAGMA table_info(canciones)")
        columnas = [fila["name"] for fila in cursor.fetchall()]

        if "genero" not in columnas:
            cursor.execute("""
                ALTER TABLE canciones
                ADD COLUMN genero TEXT NOT NULL
                DEFAULT 'Sin especificar'
            """)

        conexion.commit()

    finally:
        conexion.close()
