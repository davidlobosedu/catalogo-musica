
from structures.cola import Cola


class HistorialBusquedas:
    """Administra las últimas búsquedas mediante una cola FIFO."""

    def __init__(self, capacidad=10):
        self._cola = Cola(capacidad)

    def registrar(self, criterio, valor, cantidad_resultados):
        busqueda = {
            "criterio": criterio,
            "valor": valor,
            "resultados": cantidad_resultados
        }
        self._cola.encolar(busqueda)

    def listar(self):
        return self._cola.obtener_elementos()

    def cantidad(self):
        return self._cola.tamanio()
