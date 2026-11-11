
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

    def calcular_segundos_totales(self, canciones=None):
        """
        Calcular la suma total de segundos de una lista de canciones.
        Si no se pasa una lista, calcula el total de todas las canciones del catálogo.
        """
        if canciones is None:
            canciones = self.listar_canciones()

        total = 0
        for cancion in canciones:
            total += cancion.duracion

        return total

    @staticmethod
    def formatear_duracion(segundos):
        """
        Convierte una cantidad de segundos a un formato legible en horas, minutos y segundos.
        """
        if segundos is None or segundos < 0:
            return "0 s"

        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segs = segundos % 60

        partes = []
        if horas > 0:
            partes.append(f"{horas} h")
        if minutos > 0 or horas > 0:
            partes.append(f"{minutos} min")
        partes.append(f"{segs} s")

        return " ".join(partes)
