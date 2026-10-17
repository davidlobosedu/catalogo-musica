
from repositories.cancion_repository import CancionRepository


class Catalogo:
    def __init__(self):
        self._repositorio = CancionRepository()

    def listar_canciones(self):
        """Obtener todas las canciones."""
        return self._repositorio.obtener_todas()

    def buscar_secuencial(self, criterio, valor):
        """
        Buscar canciones por un criterio.
        Devuelve los resultados y la cantidad de comparaciones.
        """
        criterios_validos = {
            "titulo",
            "artista",
            "album"
        }

        if criterio not in criterios_validos:
            raise ValueError("El criterio de búsqueda no es válido.")

        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El valor de búsqueda no puede estar vacío.")

        canciones = self._repositorio.obtener_todas()
        resultados = []
        comparaciones = 0

        valor_buscado = valor.strip().casefold()

        for cancion in canciones:
            comparaciones += 1

            valor_cancion = getattr(cancion, criterio).casefold()

            if valor_cancion == valor_buscado:
                resultados.append(cancion)

        return resultados, comparaciones

    def buscar_por_titulo(self, titulo):
        """Buscar canciones por título."""
        return self.buscar_secuencial("titulo", titulo)

    def buscar_por_artista(self, artista):
        """Buscar canciones por artista."""
        return self.buscar_secuencial("artista", artista)

    def buscar_por_album(self, album):
        """Buscar canciones por álbum."""
        return self.buscar_secuencial("album", album)
