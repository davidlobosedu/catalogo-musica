
from flask import Flask, render_template, request, redirect, url_for, flash

from repositories.cancion_repository import CancionRepository
from models.cancion import Cancion

app = Flask(__name__)
app.secret_key = "clave-desarrollo-catalogo-musical"

repositorio = CancionRepository()


@app.route("/")
def inicio():
    canciones = repositorio.obtener_todas()
    return render_template("index.html", canciones=canciones)


@app.route("/agregar", methods=["POST"])
def agregar_cancion():
    try:
        cancion = Cancion(
            codigo=int(request.form["codigo"]),
            titulo=request.form["titulo"].strip(),
            artista=request.form["artista"].strip(),
            album=request.form["album"].strip(),
            anio=int(request.form["anio"]),
            duracion=int(request.form["duracion"])
        )

        repositorio.insertar(cancion)
        flash("Canción agregada correctamente.", "exito")

    except ValueError as error:
        flash(f"No se pudo agregar la canción: {error}", "error")
    except Exception as error:
        flash(f"No se pudo agregar la canción. "
              f"Verificá que el código no esté repetido. Detalle: {error}", "error")

    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
