
class Pila:
    def __init__(self):
        self._elementos = []

    def esta_vacia(self):
        return len(self._elementos) == 0

    def apilar(self, elemento):
        self._elementos.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            return None

        return self._elementos.pop()

    def ver_tope(self):
        if self.esta_vacia():
            return None

        return self._elementos[-1]

    def tamanio(self):
        return len(self._elementos)
