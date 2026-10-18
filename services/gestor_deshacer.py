
from models.cancion import Cancion


class GestorDeshacer:
    def __init__(self, repositorio, historial):
        self.repositorio = repositorio
        self.historial = historial

    def deshacer(self):
        if self.historial.esta_vacio():
            return False, "No hay operaciones para deshacer."

        registro = self.historial.obtener_ultima()
        operacion = registro["operacion"]
        datos = registro["datos"]

        try:
            if operacion == "agregar":
                resultado = self.repositorio.eliminar(datos["codigo"])

            elif operacion == "modificar":
                cancion_anterior = Cancion(**datos["anterior"])
                resultado = self.repositorio.modificar(cancion_anterior)

            elif operacion == "eliminar":
                cancion_eliminada = Cancion(**datos)
                self.repositorio.insertar(cancion_eliminada)
                resultado = True

            else:
                return False, f"Operación desconocida: {operacion}"

            if not resultado:
                return False, "No se pudo deshacer la operación."

            self.historial.deshacer_ultima()
            return True, "Última operación deshecha correctamente."

        except Exception as error:
            return False, f"Error al deshacer la operación: {error}"
