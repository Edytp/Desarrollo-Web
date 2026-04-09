from flask import Flask, render_template, request, redirect, url_for, flash
import json, csv
from inventario.database import db
from inventario.bd import (
    crear_tabla, insertar_producto, obtener_productos,
    eliminar_producto, obtener_producto, actualizar_producto,
    agregar_producto_db, obtener_productos_db, obtener_producto_db,
    actualizar_producto_db, eliminar_producto_db
)

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Configuración SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario_sqlalchemy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Crear tabla SQLite puro al iniciar
crear_tabla()

# ---------- RUTAS ----------

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/productos")
def productos():
    lista = obtener_productos_db()
    return render_template("productos.html", productos=lista)

@app.route("/agregar", methods=["GET","POST"])
def agregar():
    if request.method=="POST":
        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]

        # SQLite puro
        insertar_producto(nombre, cantidad, precio)
        # SQLAlchemy
        agregar_producto_db(nombre, cantidad, precio)

        # Archivos
        with open("inventario/data/datos.txt","a") as f: f.write(f"{nombre},{cantidad},{precio}\n")

        producto = {"nombre": nombre,"cantidad":cantidad,"precio":precio}
        try:
            with open("inventario/data/datos.json","r") as f: datos = json.load(f)
        except: datos=[]
        datos.append(producto)
        with open("inventario/data/datos.json","w") as f: json.dump(datos,f,indent=4)

        with open("inventario/data/datos.csv","a",newline="") as f:
            writer = csv.writer(f)
            writer.writerow([nombre,cantidad,precio])

        flash("Producto agregado correctamente")
        return redirect(url_for("productos"))

    return render_template("producto_form.html")

@app.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):
    producto = obtener_producto_db(id)
    if request.method=="POST":
        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]

        actualizar_producto(id,nombre,cantidad,precio)
        actualizar_producto_db(id,nombre,cantidad,precio)

        flash("Producto actualizado")
        return redirect(url_for("productos"))

    return render_template("editar_producto.html", producto=producto)

@app.route("/eliminar/<int:id>")
def eliminar(id):
    eliminar_producto(id)
    eliminar_producto_db(id)
    flash("Producto eliminado correctamente")
    return redirect(url_for("productos"))

@app.route("/datos")
def datos():
    txt_datos=[]
    json_datos=[]
    csv_datos=[]
    try: txt_datos = open("inventario/data/datos.txt").readlines()
    except: pass
    try: json_datos = json.load(open("inventario/data/datos.json"))
    except: pass
    try: csv_datos = list(csv.reader(open("inventario/data/datos.csv")))
    except: pass
    return render_template("datos.html", txt=txt_datos,json=json_datos,csv=csv_datos)

@app.route("/buscar", methods=["GET","POST"])
def buscar():
    resultados=[]
    if request.method=="POST":
        nombre = request.form["nombre"]
        resultados = [p for p in obtener_productos_db() if nombre.lower() in p.nombre.lower()]
    return render_template("buscar.html", resultados=resultados)

# ---------- Crear tablas SQLAlchemy ----------
with app.app_context():
    db.create_all()

if __name__=="__main__":
    app.run(debug=True)