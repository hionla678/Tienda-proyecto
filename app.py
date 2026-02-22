from flask import Flask, render_template, request, redirect
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# contraseña admin
PASSWORD = "1234"

# archivo donde se guardan los productos
PRODUCTOS_FILE = "productos.json"

# carpeta donde se guardan las imágenes
UPLOAD_FOLDER = "static/uploads"

# crear carpeta si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


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

        password = request.form["password"]

        if password == PASSWORD:

            nombre = request.form["nombre"]
            precio = request.form["precio"]

            archivo = request.files["imagen"]

            if archivo and archivo.filename != "":
                nombre_archivo = secure_filename(archivo.filename)

                ruta = os.path.join(UPLOAD_FOLDER, nombre_archivo)

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


app.run(host="0.0.0.0", port=5000, debug=True)