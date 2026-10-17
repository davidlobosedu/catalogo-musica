
import json
from pathlib import Path

from models.cancion import Cancion
from repositories.cancion_repository import CancionRepository


RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_JSON = RUTA_PROYECTO / "data" / "canciones.json"


class JsonService:
    def __init__(self):
        self.repositorio = CancionRepository()

    def exportar_canciones(self):
        canciones = self.repositorio.obtener_todas()

        datos = [
            {
                "codigo": cancion.codigo,
                "titulo": cancion.titulo,
                "artista": cancion.artista,
                "album": cancion.album,
                "anio": cancion.anio,
                "duracion": cancion.duracion,
            }
            for cancion in canciones
        ]

        RUTA_JSON.parent.mkdir(parents=True, exist_ok=True)

        with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

        return len(datos)

    def importar_canciones(self):
        if not RUTA_JSON.exists():
            raise FileNotFoundError(
                f"No existe el archivo JSON: {RUTA_JSON}"
            )

        with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError("El JSON debe contener una lista de canciones.")

        codigos = set()
        canciones = []

        for dato in datos:
            if not isinstance(dato, dict):
                raise ValueError("Cada canción debe ser un objeto JSON.")

            campos = {
                "codigo", "titulo", "artista",
                "album", "anio", "duracion"
            }

            if not campos.issubset(dato):
                raise ValueError("Una canción tiene campos faltantes.")

            cancion = Cancion(
                dato["codigo"],
                dato["titulo"],
                dato["artista"],
                dato["album"],
                dato["anio"],
                dato["duracion"],
            )

            if cancion.codigo in codigos:
                raise ValueError(
                    f"Código duplicado en el JSON: {cancion.codigo}"
                )

            codigos.add(cancion.codigo)
            canciones.append(cancion)

        # Insertamos solo códigos que todavía no existen.
        existentes = {
            cancion.codigo
            for cancion in self.repositorio.obtener_todas()
        }

        insertadas = 0

        for cancion in canciones:
            if cancion.codigo not in existentes:
                self.repositorio.insertar(cancion)
                insertadas += 1

        return insertadas
