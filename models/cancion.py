
class Cancion:
    def __init__(self, codigo, titulo, artista, album, anio, duracion, genero):
        self.codigo = codigo
        self.titulo = titulo
        self.artista = artista
        self.album = album
        self.anio = anio
        self.duracion = duracion
        self.genero = genero

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError("El código debe ser un entero positivo.")
        self._codigo = valor

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El título no puede estar vacío.")
        self._titulo = valor.strip()

    @property
    def artista(self):
        return self._artista

    @artista.setter
    def artista(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El artista no puede estar vacío.")
        self._artista = valor.strip()

    @property
    def album(self):
        return self._album

    @album.setter
    def album(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El álbum no puede estar vacío.")
        self._album = valor.strip()

    @property
    def anio(self):
        return self._anio

    @anio.setter
    def anio(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError("El año debe ser un entero positivo.")
        self._anio = valor

    @property
    def duracion(self):
        return self._duracion

    @duracion.setter
    def duracion(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError("La duración debe ser un entero positivo en segundos.")
        self._duracion = valor

    @property
    def genero(self):
        return self._genero

    @genero.setter
    def genero(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El género musical no puede estar vacío.")
        self._genero = valor.strip()

    def __str__(self):
        return (
            f"{self.titulo} - {self.artista} "
            f"({self.anio}) - Género: {self.genero}"
        )
