import sqlite3
from .database import db, ProductoDB

DB = "inventario.db"

# ---------- SQLITE PURO ----------

def crear_tabla():
    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            cantidad INTEGER,
            precio REAL
        )
    """)
    conexion.commit()
    conexion.close()

def insertar_producto(nombre, cantidad, precio):
    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
        (nombre, cantidad, precio)
    )
    conexion.commit()
    conexion.close()

def obtener_productos():
    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_producto(id):
    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conexion.close()
    return producto

def actualizar_producto(id, nombre, cantidad, precio):
    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE productos SET nombre = ?, cantidad = ?, precio = ? WHERE id = ?",
        (nombre, cantidad, precio, id)
    )
    conexion.commit()
    conexion.close()

def eliminar_producto(id):
    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()

# ---------- SQLALCHEMY ----------

def agregar_producto_db(nombre, cantidad, precio):
    producto = ProductoDB(nombre=nombre, cantidad=cantidad, precio=precio)
    db.session.add(producto)
    db.session.commit()

def obtener_productos_db():
    return ProductoDB.query.all()

def obtener_producto_db(id):
    return ProductoDB.query.get(id)

def actualizar_producto_db(id, nombre, cantidad, precio):
    producto = ProductoDB.query.get(id)
    if producto:
        producto.nombre = nombre
        producto.cantidad = cantidad
        producto.precio = precio
        db.session.commit()

def eliminar_producto_db(id):
    producto = ProductoDB.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()

    