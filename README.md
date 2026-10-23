# Catálogo Musical

## Descripción del proyecto

Aplicación web desarrollada en Python para administrar un catálogo musical. Permite consultar, agregar, editar y eliminar canciones, realizar búsquedas y organizar el catálogo mediante estructuras de datos.

El proyecto utiliza Flask para la interfaz web y SQLite para almacenar la información de forma persistente.

## Integrantes

- David Lobos

## Tecnologías utilizadas

- **Python 3.11:** lenguaje de programación.
- **Flask:** framework para desarrollar la aplicación web.
- **SQLite:** base de datos relacional.
- **HTML y CSS:** estructura y presentación de la interfaz.
- **Git y GitHub:** control de versiones y trabajo colaborativo.
- **JSON:** intercambio, importación y exportación de datos.

## Requisitos previos

- Python 3.11 o compatible.
- Git.
- Visual Studio Code u otro editor de código.
- Navegador web.

## Instalación y ejecución

1. Clonar el repositorio:

   ```bash
   git clone URL_DEL_REPOSITORIO
   ```

2. Ingresar en la carpeta del proyecto:

   ```bash
   cd catalogo-musica
   ```

3. Crear un entorno virtual:

   ```powershell
   python -m venv .venv
   ```

4. Activar el entorno virtual en PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Instalar las dependencias:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Ejecutar la aplicación:

   ```powershell
   python app.py
   ```

7. Abrir en el navegador:

   http://127.0.0.1:5000

> Si el proyecto utiliza una base de datos SQLite existente, conservar el archivo correspondiente. Verificar también las instrucciones de inicialización de la base de datos antes de ejecutar el proyecto desde una instalación nueva.

## Funcionalidades

- Alta, consulta, modificación y eliminación de canciones.
- Búsqueda secuencial por diferentes criterios.
- Registro de la cantidad de comparaciones realizadas durante las búsquedas.
- Búsqueda por código mediante un árbol binario de búsqueda.
- Recorrido inorden para listar canciones ordenadas por código.
- Organización y exploración de canciones por categorías musicales.
- Importación y exportación de canciones en formato JSON.
- Deshacer operaciones anteriores mediante una pila.
- Historial de búsquedas mediante una cola.
- Estadísticas del catálogo por categoría, si se encuentra habilitada la ruta correspondiente.

## Estructuras de datos

### Lista de canciones

Permite recorrer los registros para realizar búsquedas secuenciales y operaciones sobre el catálogo.

### Árbol binario de búsqueda

Organiza las canciones según su código. Permite buscar una canción y recorrer el árbol en inorden para obtener los registros ordenados por clave.

### Árbol de categorías

Representa la organización jerárquica de las categorías musicales y permite explorar las canciones asociadas a cada una.

### Pila

Se utiliza para registrar operaciones y recuperar la última operación realizada, con el objetivo de implementar la función de deshacer.

### Cola

Se utiliza para conservar el historial de búsquedas en orden de llegada. El historial mantiene una cantidad limitada de registros.

## Organización del proyecto

- `app.py`: aplicación Flask y definición de rutas.
- `models/`: modelo de canción.
- `repositories/`: operaciones de acceso a la base de datos.
- `database/`: configuración y conexión con SQLite.
- `services/`: lógica del catálogo, clasificación, historial, deshacer y JSON.
- `structures/`: implementación de las estructuras de datos.
- `templates/`: páginas HTML.
- `static/`: archivos CSS y otros recursos estáticos.
- `data/`: archivos de datos iniciales y exportaciones JSON.
- `requirements.txt`: dependencias del proyecto.
- `USO-DE-IA.md`: descripción del uso de herramientas de inteligencia artificial.

## Persistencia

Los datos del catálogo se almacenan en SQLite. La importación y exportación JSON permiten intercambiar información entre archivos y la base de datos.

El historial de búsquedas y las operaciones pendientes de deshacer se mantienen en memoria mientras se ejecuta la aplicación, salvo que se haya implementado persistencia adicional.

## Uso de inteligencia artificial

Consultar el archivo `USO-DE-IA.md` para conocer cómo se utilizaron herramientas de IA durante el desarrollo.

## Estado del proyecto

Trabajo práctico de Python y estructuras de datos. Antes de la entrega, verificar las funcionalidades, las pruebas y el cumplimiento de las consignas del enunciado.
