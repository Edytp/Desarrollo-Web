import sqlite3


def conectar():
    conexion = sqlite3.connect("inventario.db")
    return conexion


def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            cantidad INTEGER,
            precio REAL
        )
    """)

    conexion.commit()
    conexion.close()


def insertar_producto(nombre, cantidad, precio):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO productos(nombre,cantidad,precio) VALUES(?,?,?)",
        (nombre, cantidad, precio)
    )

    conexion.commit()
    conexion.close()


def obtener_productos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    conexion.close()

    return productos