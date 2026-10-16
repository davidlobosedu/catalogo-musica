
class Cancion:
    def __init__(self, codigo, titulo, artista, album, anio, duracion):
        self._codigo = codigo
        self._titulo = titulo
        self._artista = artista
        self._album = album
        self._anio = anio
        self._duracion = duracion

    @property
    def codigo(self):
        return self._codigo

    @property
    def titulo(self):
        return self._titulo

    @property
    def artista(self):
        return self._artista

    @property
    def album(self):
        return self._album

    @property
    def anio(self):
        return self._anio

    @property
    def duracion(self):
        return self._duracion

    def __str__(self):
        return (
            f"{self.titulo} - {self.artista} "
            f"({self.anio})"
        )
