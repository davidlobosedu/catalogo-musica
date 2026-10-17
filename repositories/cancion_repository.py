
from database.db import obtener_conexion
from models.cancion import Cancion


class CancionRepository:

    def insertar(self, cancion):
        """Guardar una canción en la base de datos."""
        conexion = obtener_conexion()

        try:
            conexion.execute(
                """
                INSERT INTO canciones
                (codigo, titulo, artista, album, anio, duracion)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    cancion.codigo,
                    cancion.titulo,
                    cancion.artista,
                    cancion.album,
                    cancion.anio,
                    cancion.duracion
                )
            )

            conexion.commit()

        finally:
            conexion.close()

    def obtener_todas(self):
        """Consultar todas las canciones."""
        conexion = obtener_conexion()

        try:
            cursor = conexion.execute(
                """
                SELECT codigo, titulo, artista, album, anio, duracion
                FROM canciones
                ORDER BY codigo
                """
            )

            filas = cursor.fetchall()

            canciones = []

            for fila in filas:
                cancion = Cancion(
                    fila[0],
                    fila[1],
                    fila[2],
                    fila[3],
                    fila[4],
                    fila[5]
                )

                canciones.append(cancion)

            return canciones

        finally:
            conexion.close()

    def obtener_por_codigo(self, codigo):
        """Buscar una canción mediante su código."""
        conexion = obtener_conexion()

        try:
            cursor = conexion.execute(
                """
                SELECT codigo, titulo, artista, album, anio, duracion
                FROM canciones
                WHERE codigo = ?
                """,
                (codigo,)
            )

            fila = cursor.fetchone()

            if fila is None:
                return None

            return Cancion(
                fila[0],
                fila[1],
                fila[2],
                fila[3],
                fila[4],
                fila[5]
            )

        finally:
            conexion.close()
