
class NodoABB:
    def __init__(self, clave, elemento):
        self.clave = clave
        self.elemento = elemento
        self.izquierda = None
        self.derecha = None


class ArbolBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, elemento):
        clave = elemento.codigo

        if self.raiz is None:
            self.raiz = NodoABB(clave, elemento)
            return True

        actual = self.raiz

        while True:
            if clave == actual.clave:
                # No permitimos códigos duplicados.
                return False

            elif clave < actual.clave:
                if actual.izquierda is None:
                    actual.izquierda = NodoABB(clave, elemento)
                    return True
                actual = actual.izquierda

            else:
                if actual.derecha is None:
                    actual.derecha = NodoABB(clave, elemento)
                    return True
                actual = actual.derecha

    def buscar(self, codigo):
        actual = self.raiz
        comparaciones = 0

        while actual is not None:
            comparaciones += 1

            if codigo == actual.clave:
                return actual.elemento, comparaciones

            elif codigo < actual.clave:
                actual = actual.izquierda

            else:
                actual = actual.derecha

        return None, comparaciones

    def listar_inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo is not None:
            self._inorden(nodo.izquierda, resultado)
            resultado.append(nodo.elemento)
            self._inorden(nodo.derecha, resultado)
