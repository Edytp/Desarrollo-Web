from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Para sesiones

DATABASE = "database.db"

# ---------------------- Conexión a la DB ----------------------
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------- Inicializar DB ----------------------
def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            descripcion TEXT,
            duracion TEXT,
            precio REAL,
            horario TEXT,
            imagen TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inscripciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            curso_id INTEGER
        )
    """)
    conn.commit()
    conn.close()

# ---------------------- Actualizar DB ----------------------
def update_db():
    conn = get_connection()
    try:
        conn.execute("ALTER TABLE cursos ADD COLUMN imagen TEXT")
        conn.commit()
        print("Columna 'imagen' agregada correctamente.")
    except sqlite3.OperationalError:
        print("La columna 'imagen' ya existe.")
    finally:
        conn.close()

# ---------------------- Seed de Cursos ----------------------
def seed_cursos():
    cursos_demo = [
        ("Robótica Infantil", "Aprende a construir robots divertidos", "3 meses", 120.0, "Lunes y Miércoles 15:00-17:00", "robot1.jpg"),
        ("Programación Básica", "Iniciación a Python para niños", "2 meses", 100.0, "Martes y Jueves 14:00-16:00", "robot2.jpg"),
        ("Electrónica Creativa", "Aprende circuitos y sensores", "2 meses", 110.0, "Viernes 15:00-17:00", "robot3.jpg")
    ]
    conn = get_connection()
    existing = conn.execute("SELECT * FROM cursos").fetchall()
    if len(existing) == 0:
        for c in cursos_demo:
            conn.execute(
                "INSERT INTO cursos (titulo, descripcion, duracion, precio, horario, imagen) VALUES (?, ?, ?, ?, ?, ?)",
                c
            )
        conn.commit()
    conn.close()

# ---------------------- Inicialización ----------------------
init_db()
update_db()
seed_cursos()

# ---------------------- Rutas ----------------------
@app.route('/')
def index():
    conn = get_connection()
    cursos = conn.execute("SELECT * FROM cursos").fetchall()
    conn.close()
    return render_template('index.html', cursos=cursos)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = generate_password_hash(request.form['password'])

        try:
            conn = get_connection()
            conn.execute("INSERT INTO usuarios (cedula, nombre, correo, password) VALUES (?, ?, ?, ?)",
                         (cedula, nombre, correo, password))
            conn.commit()
            conn.close()
            flash("¡Registro exitoso! Ahora puedes iniciar sesión.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Cédula o correo ya registrados.", "danger")
            return redirect(url_for('registro'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cedula = request.form['cedula']
        password = request.form['password']
        conn = get_connection()
        usuario = conn.execute("SELECT * FROM usuarios WHERE cedula = ?", (cedula,)).fetchone()
        conn.close()
        if usuario and check_password_hash(usuario['password'], password):
            session['usuario_id'] = usuario['id']
            session['usuario_nombre'] = usuario['nombre']
            flash(f"Bienvenido {usuario['nombre']}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Cédula o contraseña incorrecta.", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    cursos = conn.execute("SELECT * FROM cursos").fetchall()
    inscripciones = conn.execute("SELECT curso_id FROM inscripciones WHERE usuario_id = ?", (session['usuario_id'],)).fetchall()
    inscritos = [i['curso_id'] for i in inscripciones]
    conn.close()
    return render_template('dashboard.html', cursos=cursos, inscritos=inscritos)

@app.route('/inscribirse/<int:curso_id>')
def inscribirse(curso_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    conn.execute("INSERT INTO inscripciones (usuario_id, curso_id) VALUES (?, ?)", (session['usuario_id'], curso_id))
    conn.commit()
    conn.close()
    flash("¡Inscripción realizada con éxito!", "success")
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('index'))

# ---------------------- Ejecutar app ----------------------
if __name__ == "__main__":
    app.run(debug=True)