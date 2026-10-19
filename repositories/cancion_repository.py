
from database.db import obtener_conexion
from models.cancion import Cancion


class CancionRepository:

    def insertar(self, cancion):
        conexion = obtener_conexion()

        try:
            conexion.execute("""
                INSERT INTO canciones
                (codigo, titulo, artista, album, anio, duracion, genero)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                cancion.codigo,
                cancion.titulo,
                cancion.artista,
                cancion.album,
                cancion.anio,
                cancion.duracion,
                cancion.genero
            ))

            conexion.commit()

        finally:
            conexion.close()

    def obtener_todas(self):
        conexion = obtener_conexion()

        try:
            cursor = conexion.execute("""
                SELECT codigo, titulo, artista, album, anio, duracion, genero
                FROM canciones
                ORDER BY codigo
            """)

            return [
                Cancion(
                    fila[0], fila[1], fila[2], fila[3],
                    fila[4], fila[5], fila[6]
                )
                for fila in cursor.fetchall()
            ]

        finally:
            conexion.close()

    def obtener_por_codigo(self, codigo):
        conexion = obtener_conexion()

        try:
            cursor = conexion.execute("""
                SELECT codigo, titulo, artista, album, anio, duracion, genero
                FROM canciones
                WHERE codigo = ?
            """, (codigo,))

            fila = cursor.fetchone()

            if fila is None:
                return None

            return Cancion(
                fila[0], fila[1], fila[2], fila[3],
                fila[4], fila[5], fila[6]
            )

        finally:
            conexion.close()

    def modificar(self, cancion):
        conexion = obtener_conexion()

        try:
            cursor = conexion.execute("""
                UPDATE canciones
                SET titulo = ?,
                    artista = ?,
                    album = ?,
                    anio = ?,
                    duracion = ?,
                    genero = ?
                WHERE codigo = ?
            """, (
                cancion.titulo,
                cancion.artista,
                cancion.album,
                cancion.anio,
                cancion.duracion,
                cancion.genero,
                cancion.codigo
            ))

            conexion.commit()
            return cursor.rowcount > 0

        finally:
            conexion.close()

    def eliminar(self, codigo):
        conexion = obtener_conexion()

        try:
            cursor = conexion.execute(
                "DELETE FROM canciones WHERE codigo = ?",
                (codigo,)
            )

            conexion.commit()
            return cursor.rowcount > 0

        finally:
            conexion.close()
