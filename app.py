from flask import Flask, render_template, request, redirect
import json
import os
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

print("APP INICIANDO...")

# contraseña admin
PASSWORD = "1234"

# archivo productos
PRODUCTOS_FILE = "productos.json"

# CONFIG CLOUDINARY
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

        password = request.form.get("password")

        if password == PASSWORD:

            nombre = request.form.get("nombre")
            precio = request.form.get("precio")
            archivo = request.files.get("imagen")

            if archivo:

                subida = cloudinary.uploader.upload(archivo)

                url_imagen = subida["secure_url"]
                public_id = subida["public_id"]

                productos = cargar_productos()

                productos.append({
                    "nombre": nombre,
                    "precio": precio,
                    "imagen": url_imagen,
                    "public_id": public_id
                })

                guardar_productos(productos)

            return redirect("/admin")

    productos = cargar_productos()
    return render_template("admin.html", productos=productos)

@app.route("/eliminar/<int:indice>", methods=["POST"])
def eliminar(indice):

    productos = cargar_productos()

    if 0 <= indice < len(productos):

        public_id = productos[indice]["public_id"]

        cloudinary.uploader.destroy(public_id)

        productos.pop(indice)
        guardar_productos(productos)

    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)