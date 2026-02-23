from flask import Flask, render_template, request, redirect
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

print("APP INICIANDO...")

# contraseña admin
PASSWORD = "1234"

# archivo donde se guardan los productos
PRODUCTOS_FILE = "productos.json"

# carpeta donde se guardan las imágenes
UPLOAD_FOLDER = os.path.join("static", "uploads")

# decirle a flask donde subir archivos
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# crear carpeta si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# cargar productos
def cargar_productos():
    if not os.path.exists(PRODUCTOS_FILE):
        return []

    try:
        with open(PRODUCTOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


# guardar productos
def guardar_productos(productos):
    with open(PRODUCTOS_FILE, "w", encoding="utf-8") as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)


@app.route("/")
def index():
    productos = cargar_productos()
    return render_template("index.html", productos=productos)


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        password = request.form.get("password")

        if password == PASSWORD:

            nombre = request.form.get("nombre")
            precio = request.form.get("precio")
            archivo = request.files.get("imagen")

            if archivo and archivo.filename != "":

                nombre_archivo = secure_filename(archivo.filename)

                ruta = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)

                archivo.save(ruta)

                productos = cargar_productos()

                productos.append({
                    "nombre": nombre,
                    "precio": precio,
                    "imagen": f"uploads/{nombre_archivo}"
                })

                guardar_productos(productos)

            return redirect("/")

    return render_template("admin.html")

@app.route("/eliminar/<int:indice>", methods=["POST"])
def eliminar(indice):
    productos = cargar_productos()

    if 0 <= indice < len(productos):

        # obtener nombre del archivo
        nombre_archivo = productos[indice]["imagen"].split("/")[-1]

        ruta_imagen = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)

        # borrar imagen si existe
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # eliminar producto del json
        productos.pop(indice)
        guardar_productos(productos)

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)