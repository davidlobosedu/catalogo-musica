
class Cola:
    """Estructura FIFO: el primero en entrar es el primero en salir."""

    def __init__(self, capacidad=10):
        self._elementos = []
        self._capacidad = capacidad

    def encolar(self, elemento):
        """Agrega un elemento al final y conserva la capacidad máxima."""
        self._elementos.append(elemento)

        if len(self._elementos) > self._capacidad:
            self.desencolar()

    def desencolar(self):
        """Retira y devuelve el elemento más antiguo."""
        if self.esta_vacia():
            return None

        return self._elementos.pop(0)

    def obtener_elementos(self):
        """Devuelve una copia de los elementos en orden de llegada."""
        return self._elementos.copy()

    def esta_vacia(self):
        return len(self._elementos) == 0

    def tamanio(self):
        return len(self._elementos)
