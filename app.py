from flask import Flask, render_template, request, redirect
import json
import os
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# 🔐 contraseña admin
PASSWORD = "1234"

# 📁 archivo donde se guardan los productos
PRODUCTOS_FILE = "productos.json"

# 🔹 CONFIGURACIÓN CLOUDINARY (PON TUS DATOS AQUÍ)
cloudinary.config(
    cloud_name="dj8adnlhn",
    api_key="395448994121461",
    api_secret="_1VV3uJ3WOZjv02ZBal2Py5Q2ho"
)

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

                # 🔥 SUBIR IMAGEN A CLOUDINARY
                resultado = cloudinary.uploader.upload(archivo)

                url_imagen = resultado["secure_url"]

                productos = cargar_productos()

                productos.append({
                    "nombre": nombre,
                    "precio": precio,
                    "imagen": url_imagen
                })

                guardar_productos(productos)

            return redirect("/")

    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)