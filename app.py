
from flask import Flask, render_template, request, redirect, url_for, flash

from repositories.cancion_repository import CancionRepository
from models.cancion import Cancion
from services.catalogo import Catalogo


app = Flask(__name__)
app.secret_key = "clave-desarrollo-catalogo-musical"

repositorio = CancionRepository()
catalogo = Catalogo()


@app.route("/")
def inicio():
    canciones = repositorio.obtener_todas()
    return render_template("index.html", canciones=canciones)


@app.route("/buscar", methods=["GET"])
def buscar_canciones():
    criterio = request.args.get("criterio", "").strip()
    valor = request.args.get("valor", "").strip()

    try:
        canciones, comparaciones = catalogo.buscar_secuencial(
            criterio,
            valor
        )

        return render_template(
            "index.html",
            canciones=canciones,
            criterio_busqueda=criterio,
            valor_busqueda=valor,
            comparaciones=comparaciones,
            busqueda_realizada=True
        )

    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("inicio"))


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
        flash(
            "No se pudo agregar la canción. "
            f"Verificá que el código no esté repetido. Detalle: {error}",
            "error"
        )

    return redirect(url_for("inicio"))


@app.route("/editar/<int:codigo>", methods=["GET", "POST"])
def editar_cancion(codigo):
    cancion = repositorio.obtener_por_codigo(codigo)

    if cancion is None:
        flash("No se encontró la canción.", "error")
        return redirect(url_for("inicio"))

    if request.method == "POST":
        try:
            cancion_actualizada = Cancion(
                codigo=codigo,
                titulo=request.form["titulo"].strip(),
                artista=request.form["artista"].strip(),
                album=request.form["album"].strip(),
                anio=int(request.form["anio"]),
                duracion=int(request.form["duracion"])
            )

            repositorio.modificar(cancion_actualizada)
            flash("Canción modificada correctamente.", "exito")

            return redirect(url_for("inicio"))

        except ValueError as error:
            flash(
                f"No se pudo modificar la canción: {error}",
                "error"
            )

    return render_template("editar.html", cancion=cancion)


@app.route("/eliminar/<int:codigo>", methods=["POST"])
def eliminar_cancion(codigo):
    try:
        eliminado = repositorio.eliminar(codigo)

        if eliminado:
            flash("Canción eliminada correctamente.", "exito")
        else:
            flash(
                "No se encontró la canción que intentás eliminar.",
                "error"
            )

    except Exception as error:
        flash(
            f"No se pudo eliminar la canción: {error}",
            "error"
        )

    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
