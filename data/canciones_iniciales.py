
from models.cancion import Cancion
from repositories.cancion_repository import CancionRepository


def cargar_canciones_iniciales():
    repositorio = CancionRepository()

    datos = [
        (1, "La Balada del diablo y la muerte", "La Renga", "Despedazado por mil partes", 1994, 300),
        (2, "El 38", "Divididos", "Acariciando lo aspero", 1991, 150),
        (3, "Crua Chan", "Sumo", "After Chabon", 1987, 212),
        (4, "Heroina", "Sumo", "Llegando a los monos", 1986, 341),
        (5, "Tren al sur", "Los Prisioneros", "Corazones", 1990, 300),
        (6, "Lamento boliviano", "Los Enanitos Verdes", "Big Bang", 1994, 210),
        (7, "La muralla verde", "Los Enanitos Verdes", "Contrarreloj", 1986, 210),
        (8, "Mil horas", "Los Abuelos de la Nada", "Vasos y besos", 1983, 210),
        (9, "Flaca", "Andres Calamaro", "Alta suciedad", 1997, 240),
        (10, "Crimen", "Gustavo Cerati", "Ahi vamos", 2006, 230),
        (11, "Puente", "Gustavo Cerati", "Bocanada", 1999, 290),
        (12, "Seguir viviendo sin tu amor", "Luis Alberto Spinetta", "Peluson of milk", 1991, 220),
        (13, "Muchacha ojos de papel", "Almendra", "Almendra", 1969, 240),
        (14, "Rasguña las piedras", "Sui Generis", "Confesiones de invierno", 1973, 210),
        (15, "Seminare", "Seru Giran", "Seru Giran", 1978, 250),
        (16, "Ji ji ji", "Patricio Rey y sus Redonditos de Ricota", "Oktubre", 1986, 330),
        (17, "Todo un palo", "Patricio Rey y sus Redonditos de Ricota", "Un baion para el ojo idiota", 1988, 300),
        (18, "Matador", "Los Fabulosos Cadillacs", "Vasos vacios", 1993, 250),
        (19, "El satánico Dr. Cadillac", "Los Fabulosos Cadillacs", "El leon", 1992, 260),
        (20, "Deja vu", "Gustavo Cerati", "Fuerza natural", 2009, 220),
        (21, "Billie Jean", "Michael Jackson", "Thriller", 1982, 294),
        (22, "Like a Prayer", "Madonna", "Like a Prayer", 1989, 340),
        (23, "Thriller", "Michael Jackson", "Thriller", 1982, 358),
        (24, "Imagine", "John Lennon", "Imagine", 1971, 183),
        (25, "Dancing Queen", "ABBA", "Arrival", 1976, 230),
        (26, "Yellow", "Coldplay", "Parachutes", 2000, 266),
        (27, "Viva la Vida", "Coldplay", "Viva la Vida", 2008, 242),
        (28, "La flor azul", "Mercedes Sosa", "Corazon libre", 2005, 210),
        (29, "Alfonsina y el mar", "Mercedes Sosa", "Mujeres argentinas", 1969, 240),
        (30, "Zamba para olvidar", "Daniel Toro", "Zambas", 1976, 220),
    ]

    existentes = {
        cancion.codigo
        for cancion in repositorio.obtener_todas()
    }

    insertadas = 0

    for dato in datos:
        codigo, titulo, artista, album, anio, duracion = dato

        if codigo not in existentes:
            cancion = Cancion(
                codigo, titulo, artista, album, anio, duracion
            )
            repositorio.insertar(cancion)
            insertadas += 1

    print(f"Canciones iniciales cargadas: {insertadas}")
    print(f"Total de canciones en la base: {len(repositorio.obtener_todas())}")


if __name__ == "__main__":
    cargar_canciones_iniciales()
