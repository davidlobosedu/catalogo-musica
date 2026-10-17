
from structures.pila import Pila


class HistorialOperaciones:
    def __init__(self):
        self._pila = Pila()

    def registrar(self, operacion, datos):
        registro = {
            "operacion": operacion,
            "datos": datos
        }
        self._pila.apilar(registro)

    def obtener_ultima(self):
        return self._pila.ver_tope()

    def deshacer_ultima(self):
        return self._pila.desapilar()

    def esta_vacio(self):
        return self._pila.esta_vacia()

    def cantidad(self):
        return self._pila.tamanio()
