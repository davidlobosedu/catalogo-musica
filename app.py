from flask import Flask, render_template, request, redirect, url_for, flash

from database.db import inicializar_db
from data.canciones_iniciales import cargar_canciones_iniciales

from repositories.cancion_repository import CancionRepository
from models.cancion import Cancion
from services.catalogo import Catalogo
from services.historial import HistorialOperaciones
from services.gestor_deshacer import GestorDeshacer
from services.json_service import JsonService
from structures.arbol_busqueda import ArbolBusqueda
from services.clasificador_categorias import cargar_categorias
from services.historial_busquedas import HistorialBusquedas


# ------------------------------------------------------------
# 1. Preparar la base de datos y cargar los datos iniciales
# ------------------------------------------------------------

# Crea la tabla si todavía no existe y agrega la columna genero
# si la base de datos ya existía sin esa columna.
inicializar_db()

# Agrega las canciones iniciales que todavía no estén guardadas.
# No duplica las canciones que ya existen.
cargar_canciones_iniciales()


# ------------------------------------------------------------
# 2. Crear la aplicación Flask y los objetos que utiliza
# ------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "clave-desarrollo-catalogo-musical"

json_service = JsonService()
repositorio = CancionRepository()
catalogo = Catalogo()
historial = HistorialOperaciones()
gestor_deshacer = GestorDeshacer(repositorio, historial)
historial_busquedas = HistorialBusquedas(capacidad=10)


# ------------------------------------------------------------
# 3. Funciones auxiliares
# ------------------------------------------------------------

def convertir_cancion_a_diccionario(cancion):
    """Convertir una canción en un diccionario para el historial."""
    return {
        "codigo": cancion.codigo,
        "titulo": cancion.titulo,
        "artista": cancion.artista,
        "album": cancion.album,
        "anio": cancion.anio,
        "duracion": cancion.duracion,
        "genero": cancion.genero
    }


def obtener_cancion_desde_formulario(codigo):
    """Construir una canción validando los datos recibidos del formulario."""
    return Cancion(
        codigo=codigo,
        titulo=request.form.get("titulo", "").strip(),
        artista=request.form.get("artista", "").strip(),
        album=request.form.get("album", "").strip(),
        anio=int(request.form.get("anio", "")),
        duracion=int(request.form.get("duracion", "")),
        genero=request.form.get("genero", "").strip()
    )


# ------------------------------------------------------------
# 4. Página principal
# ------------------------------------------------------------

@app.route("/")
def inicio():
    canciones = repositorio.obtener_todas()

    return render_template(
        "index.html",
        canciones=canciones,
        cantidad_historial=historial.cantidad()
    )


# ------------------------------------------------------------
# 5. Búsqueda secuencial por título, artista o álbum
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 6. Agregar una canción
# ------------------------------------------------------------

@app.route("/agregar", methods=["POST"])
def agregar_cancion():
    try:
        cancion = obtener_cancion_desde_formulario(
            codigo=int(request.form.get("codigo", ""))
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


# ------------------------------------------------------------
# 7. Editar una canción
# ------------------------------------------------------------

@app.route("/editar/<int:codigo>", methods=["GET", "POST"])
def editar_cancion(codigo):
    cancion = repositorio.obtener_por_codigo(codigo)

    if cancion is None:
        flash("No se encontró la canción.", "error")
        return redirect(url_for("inicio"))

    if request.method == "POST":
        try:
            # Guardamos los datos anteriores para permitir deshacer.
            datos_anteriores = convertir_cancion_a_diccionario(cancion)

            cancion_actualizada = obtener_cancion_desde_formulario(codigo)

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

        except Exception as error:
            flash(
                f"Ocurrió un error al modificar la canción: {error}",
                "error"
            )

    return render_template(
        "editar.html",
        cancion=cancion,
        cantidad_historial=historial.cantidad()
    )


# ------------------------------------------------------------
# 8. Eliminar una canción
# ------------------------------------------------------------

@app.route("/eliminar/<int:codigo>", methods=["POST"])
def eliminar_cancion(codigo):
    try:
        cancion = repositorio.obtener_por_codigo(codigo)

        if cancion is None:
            flash("No se encontró la canción.", "error")
            return redirect(url_for("inicio"))

        # Guardamos los datos para poder recuperar la canción al deshacer.
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


# ------------------------------------------------------------
# 9. Deshacer la última operación compatible
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 10. Exportar las canciones a JSON
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 11. Importar canciones desde JSON
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 12. Buscar por código usando un árbol binario de búsqueda
# ------------------------------------------------------------

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

    arbol = ArbolBusqueda()
    canciones = repositorio.obtener_todas()

    # Insertamos las canciones en el árbol.
    for cancion in canciones:
        arbol.insertar(cancion)

    cancion_encontrada, comparaciones_arbol = arbol.buscar(codigo)

    # Repetimos la búsqueda con una lista para comparar las comparaciones.
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


# ------------------------------------------------------------
# 13. Ordenar las canciones mediante el recorrido inorden del árbol
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 14. Explorar canciones por categoría
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 15. Consultar el historial de búsquedas
# ------------------------------------------------------------

@app.route("/historial-busquedas")
def ver_historial_busquedas():
    busquedas = historial_busquedas.listar()

    return render_template(
        "index.html",
        canciones=repositorio.obtener_todas(),
        historial_busquedas=busquedas,
        cantidad_historial=historial.cantidad()
    )


# ------------------------------------------------------------
# 16. Ver estadísticas por género
# ------------------------------------------------------------

@app.route("/estadisticas")
def ver_estadisticas():
    canciones = repositorio.obtener_todas()
    arbol = cargar_categorias()

    nombres_categorias = [
        "Rock Argentino",
        "Rock internacional",
        "Pop",
        "Folclore"
    ]

    estadisticas = {}

    for nombre in nombres_categorias:
        categoria = arbol.buscar_categoria(nombre)

        if categoria is not None:
            estadisticas[nombre] = len(categoria.canciones)
        else:
            estadisticas[nombre] = 0

    return render_template(
        "index.html",
        canciones=canciones,
        total_canciones=len(canciones),
        estadisticas=estadisticas,
        cantidad_historial=historial.cantidad()
    )


# ------------------------------------------------------------
# 17. Ejecutar la aplicación
# ------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
