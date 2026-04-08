from flask import Flask, render_template, url_for, request, redirect, flash
from database import crear_tabla, insertar_producto, obtener_productos

app = Flask(__name__)

# clave necesaria para usar flash si luego la usas
app.secret_key = "clave_secreta"

# crear tabla de productos al iniciar
crear_tabla()

# -------------------------
# RUTAS PRINCIPALES
# -------------------------

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/productos")
def productos():
    lista = obtener_productos()
    return render_template("productos.html", productos=lista)


@app.route("/usuario/<nombre>")
def usuario(nombre):
    return f"Bienvenido {nombre} a Innovakids"


# -------------------------
# RUTA PARA AGREGAR PRODUCTOS
# -------------------------

@app.route("/agregar", methods=["GET", "POST"])
def agregar():

    if request.method == "POST":

        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]

        insertar_producto(nombre, cantidad, precio)

        flash("Producto agregado correctamente")

        return redirect(url_for("productos"))

    return render_template("producto_form.html")


# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
    