
from flask import Flask, render_template, request, redirect, url_for, flash

from repositories.cancion_repository import CancionRepository
from models.cancion import Cancion
from services.catalogo import Catalogo
from services.historial import HistorialOperaciones
from services.gestor_deshacer import GestorDeshacer
from services.json_service import JsonService
from pathlib import Path
from structures.arbol_busqueda import ArbolBusqueda
from services.clasificador_categorias import cargar_categorias
from services.historial_busquedas import HistorialBusquedas


app = Flask(__name__)
app.secret_key = "clave-desarrollo-catalogo-musical"
json_service = JsonService()
repositorio = CancionRepository()
catalogo = Catalogo()
historial = HistorialOperaciones()
gestor_deshacer = GestorDeshacer(repositorio, historial)
historial_busquedas = HistorialBusquedas(capacidad=10)


def convertir_cancion_a_diccionario(cancion):
    """Convertir una canción en un diccionario para el historial."""
    return {
        "codigo": cancion.codigo,
        "titulo": cancion.titulo,
        "artista": cancion.artista,
        "album": cancion.album,
        "anio": cancion.anio,
        "duracion": cancion.duracion
    }


@app.route("/")
def inicio():
    canciones = repositorio.obtener_todas()

    return render_template(
        "index.html",
        canciones=canciones,
        cantidad_historial=historial.cantidad()
    )


@app.route("/buscar", methods=["GET"])
def buscar_canciones():
    criterio = request.args.get("criterio", "").strip()
    valor = request.args.get("valor", "").strip()

    try:
        canciones, comparaciones = catalogo.buscar_secuencial(
            criterio,
            valor
        )

        historial_busquedas.registrar(
            criterio,
            valor,
            len(canciones)
        )

        return render_template(
            "index.html",
            canciones=canciones,
            criterio_busqueda=criterio,
            valor_busqueda=valor,
            comparaciones=comparaciones,
            busqueda_realizada=True,
            cantidad_historial=historial.cantidad()
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

        historial.registrar(
            "agregar",
            {"codigo": cancion.codigo}
        )

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
            datos_anteriores = convertir_cancion_a_diccionario(cancion)

            cancion_actualizada = Cancion(
                codigo=codigo,
                titulo=request.form["titulo"].strip(),
                artista=request.form["artista"].strip(),
                album=request.form["album"].strip(),
                anio=int(request.form["anio"]),
                duracion=int(request.form["duracion"])
            )

            modificada = repositorio.modificar(cancion_actualizada)

            if modificada:
                historial.registrar(
                    "modificar",
                    {"anterior": datos_anteriores}
                )

                flash("Canción modificada correctamente.", "exito")
                return redirect(url_for("inicio"))

            flash("No se pudo modificar la canción.", "error")

        except ValueError as error:
            flash(
                f"No se pudo modificar la canción: {error}",
                "error"
            )

    return render_template("editar.html", cancion=cancion)


@app.route("/eliminar/<int:codigo>", methods=["POST"])
def eliminar_cancion(codigo):
    try:
        cancion = repositorio.obtener_por_codigo(codigo)

        if cancion is None:
            flash("No se encontró la canción.", "error")
            return redirect(url_for("inicio"))

        datos_cancion = convertir_cancion_a_diccionario(cancion)
        eliminada = repositorio.eliminar(codigo)

        if eliminada:
            historial.registrar("eliminar", datos_cancion)
            flash("Canción eliminada correctamente.", "exito")
        else:
            flash("No se pudo eliminar la canción.", "error")

    except Exception as error:
        flash(
            f"No se pudo eliminar la canción: {error}",
            "error"
        )

    return redirect(url_for("inicio"))


@app.route("/deshacer", methods=["POST"])
def deshacer_operacion():
    try:
        exito, mensaje = gestor_deshacer.deshacer()

        if exito:
            flash(mensaje, "exito")
        else:
            flash(mensaje, "error")

    except Exception as error:
        flash(
            f"No se pudo deshacer la operación: {error}",
            "error"
        )

    return redirect(url_for("inicio"))

@app.route("/exportar-json", methods=["POST"])
def exportar_json():
    try:
        cantidad = json_service.exportar_canciones()

        flash(
            f"Se exportaron {cantidad} canciones al archivo JSON.",
            "exito"
        )

    except Exception as error:
        flash(
            f"No se pudieron exportar las canciones: {error}",
            "error"
        )

    return redirect(url_for("inicio"))


@app.route("/importar-json", methods=["POST"])
def importar_json():
    try:
        cantidad = json_service.importar_canciones()

        flash(
            f"Se importaron {cantidad} canciones nuevas desde JSON.",
            "exito"
        )

    except (ValueError, FileNotFoundError) as error:
        flash(
            f"No se pudo importar el archivo JSON: {error}",
            "error"
        )

    except Exception as error:
        flash(
            f"Ocurrió un error durante la importación: {error}",
            "error"
        )

    return redirect(url_for("inicio"))


@app.route("/buscar-arbol", methods=["GET"])
def buscar_arbol():
    valor = request.args.get("codigo", "").strip()

    try:
        codigo = int(valor)
        if codigo <= 0:
            raise ValueError
    except ValueError:
        flash("Ingresá un código numérico positivo.", "error")
        return redirect(url_for("inicio"))

    # Construimos el árbol con los datos actuales de SQLite.
    arbol = ArbolBusqueda()
    canciones = repositorio.obtener_todas()

    for cancion in canciones:
        arbol.insertar(cancion)

    cancion_encontrada, comparaciones_arbol = arbol.buscar(codigo)

    # Búsqueda secuencial por código para comparar los resultados.
    comparaciones_lista = 0
    encontrada_lista = None

    for cancion in canciones:
        comparaciones_lista += 1
        if cancion.codigo == codigo:
            encontrada_lista = cancion
            break

    resultados = (
        [cancion_encontrada]
        if cancion_encontrada is not None
        else []
    )

    return render_template(
        "index.html",
        canciones=resultados,
        busqueda_arbol_realizada=True,
        codigo_busqueda=codigo,
        comparaciones_arbol=comparaciones_arbol,
        comparaciones_lista=comparaciones_lista,
        cantidad_historial=historial.cantidad()
    )


@app.route("/ordenar-arbol")
def ordenar_arbol():
    arbol = ArbolBusqueda()

    for cancion in repositorio.obtener_todas():
        arbol.insertar(cancion)

    canciones_ordenadas = arbol.listar_inorden()

    return render_template(
        "index.html",
        canciones=canciones_ordenadas,
        listado_ordenado_arbol=True,
        cantidad_historial=historial.cantidad()
    )

@app.route("/explorar-categoria", methods=["GET"])
def explorar_categoria():
    nombre_categoria = request.args.get("categoria", "").strip()

    arbol = cargar_categorias()
    categorias = arbol.listar_categorias()

    nodo = arbol.buscar_categoria(nombre_categoria)

    if nodo is None:
        flash("La categoría seleccionada no existe.", "error")
        return redirect(url_for("inicio"))

    return render_template(
        "index.html",
        canciones=nodo.canciones,
        categoria_seleccionada=nodo.nombre,
        categorias=categorias,
        cantidad_historial=historial.cantidad()
    )



@app.route("/historial-busquedas")
def ver_historial_busquedas():
    busquedas = historial_busquedas.listar()

    return render_template(
        "index.html",
        canciones=repositorio.obtener_todas(),
        historial_busquedas=busquedas,
        cantidad_historial=historial.cantidad()
    )

if __name__ == "__main__":
    app.run(debug=True)
