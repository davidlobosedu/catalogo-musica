
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
        """Exportar todas las canciones, incluido su género, a JSON."""
        canciones = self.repositorio.obtener_todas()

        datos = [
            {
                "codigo": cancion.codigo,
                "titulo": cancion.titulo,
                "artista": cancion.artista,
                "album": cancion.album,
                "anio": cancion.anio,
                "duracion": cancion.duracion,
                "genero": cancion.genero,
            }
            for cancion in canciones
        ]

        RUTA_JSON.parent.mkdir(parents=True, exist_ok=True)

        with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

        return len(datos)

    def importar_canciones(self):
        """Importar canciones nuevas desde JSON sin duplicar códigos."""
        if not RUTA_JSON.exists():
            raise FileNotFoundError(
                f"No existe el archivo JSON: {RUTA_JSON}"
            )

        try:
            with open(RUTA_JSON, "r", encoding="utf-8-sig") as archivo:
                datos = json.load(archivo)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"El archivo JSON tiene un formato inválido: {error}"
            ) from error

        if not isinstance(datos, list):
            raise ValueError(
                "El JSON debe contener una lista de canciones."
            )

        campos_obligatorios = {
            "codigo",
            "titulo",
            "artista",
            "album",
            "anio",
            "duracion",
        }

        canciones = []
        codigos = set()

        for numero, dato in enumerate(datos, start=1):
            if not isinstance(dato, dict):
                raise ValueError(
                    f"El elemento {numero} no es un objeto JSON válido."
                )

            faltantes = campos_obligatorios - dato.keys()

            if faltantes:
                raise ValueError(
                    f"La canción del elemento {numero} no contiene "
                    f"los campos obligatorios: {', '.join(sorted(faltantes))}."
                )

            try:
                codigo = dato["codigo"]
                titulo = dato["titulo"]
                artista = dato["artista"]
                album = dato["album"]
                anio = dato["anio"]
                duracion = dato["duracion"]
                genero = dato.get("genero") or "Sin especificar"

                cancion = Cancion(
                    codigo=codigo,
                    titulo=titulo,
                    artista=artista,
                    album=album,
                    anio=anio,
                    duracion=duracion,
                    genero=genero,
                )

            except (ValueError, TypeError) as error:
                raise ValueError(
                    f"Datos inválidos en la canción del elemento "
                    f"{numero}: {error}"
                ) from error

            if cancion.codigo in codigos:
                raise ValueError(
                    f"Código duplicado en el JSON: {cancion.codigo}"
                )

            codigos.add(cancion.codigo)
            canciones.append(cancion)

        existentes = {
            cancion.codigo
            for cancion in self.repositorio.obtener_todas()
        }

        insertadas = 0

        for cancion in canciones:
            if cancion.codigo not in existentes:
                self.repositorio.insertar(cancion)
                existentes.add(cancion.codigo)
                insertadas += 1

        return insertadas
