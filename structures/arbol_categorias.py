
class NodoCategoria:
    def __init__(self, nombre):
        self.nombre = nombre
        self.subcategorias = []
        self.canciones = []

    def agregar_subcategoria(self, nombre):
        """Crear una subcategoría dentro del nodo."""
        nueva = NodoCategoria(nombre)
        self.subcategorias.append(nueva)
        return nueva


class ArbolCategorias:
    def __init__(self):
        self.raiz = NodoCategoria("Música")

        rock = self.raiz.agregar_subcategoria("Rock")
        rock.agregar_subcategoria("Rock Argentino")
        rock.agregar_subcategoria("Rock internacional")

        self.raiz.agregar_subcategoria("Pop")
        self.raiz.agregar_subcategoria("Folclore")

    def buscar_categoria(self, nombre, nodo=None):
        """Buscar una categoría por su nombre."""
        if nodo is None:
            nodo = self.raiz

        if nodo.nombre.casefold() == nombre.casefold():
            return nodo

        for subcategoria in nodo.subcategorias:
            resultado = self.buscar_categoria(
                nombre,
                subcategoria
            )

            if resultado is not None:
                return resultado

        return None

    def agregar_cancion(self, nombre_categoria, cancion):
        """Agregar una canción a una categoría existente."""
        categoria = self.buscar_categoria(nombre_categoria)

        if categoria is None:
            return False

        categoria.canciones.append(cancion)
        return True

    def listar_categorias(self, nodo=None, nivel=0):
        """Mostrar las categorías (recorrido recursivo)."""
        if nodo is None:
            nodo = self.raiz

        resultado = ["  " * nivel + nodo.nombre]

        for subcategoria in nodo.subcategorias:
            resultado.extend(
                self.listar_categorias(subcategoria, nivel + 1)
            )

        return resultado
