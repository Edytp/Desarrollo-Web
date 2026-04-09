from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask import current_app
from flask_mail import Message
from mail_config import mail
from app import get_connection

auth = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.login_view = "auth.login"

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM usuarios WHERE id=?", (user_id,)).fetchone()
    conn.close()
    if not row:
        return None
    user = User()
    user.id = row["id"]
    user.nombre = row["nombre"]
    user.correo = row["correo"]
    return user

@auth.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        cedula = request.form["cedula"]
        correo = request.form["correo"]
        password = generate_password_hash(request.form["password"])
        conn = get_connection()
        conn.execute("INSERT INTO usuarios (cedula,nombre,correo,password) VALUES (?,?,?,?)",
                     (cedula, nombre, correo, password))
        conn.commit()
        conn.close()

        # Enviar correo de bienvenida
        msg = Message(
            "¡Bienvenido a INNOVAKIDS!",
            recipients=[correo]
        )
        msg.html = render_template("email_template.html", nombre=nombre)
        mail.send(msg)

        flash("Cuenta creada. Revisa tu correo para confirmarla", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        cedula = request.form["cedula"]
        password = request.form["password"]
        conn = get_connection()
        user = conn.execute("SELECT * FROM usuarios WHERE cedula=?", (cedula,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password"], password):
            user_obj = User()
            user_obj.id = user["id"]
            login_user(user_obj)
            return redirect(url_for("dashboard"))
        flash("Cédula o contraseña incorrecta", "error")
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from auth import auth, login_manager
from mail_config import mail
from app import get_connection

app = Flask(__name__)
app.secret_key = "innovakids_secret_key"

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "TU_CORREO@gmail.com"
app.config['MAIL_PASSWORD'] = "TU_CONTRASEÑA"
app.config['MAIL_DEFAULT_SENDER'] = "TU_CORREO@gmail.com"

mail.init_app(app)
login_manager.init_app(app)
app.register_blueprint(auth)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/acerca")
def acerca():
    return render_template("acerca.html")

@app.route("/cursos")
def cursos():
    conn = get_connection()
    cursos = conn.execute("SELECT * FROM cursos").fetchall()
    conn.close()
    return render_template("cursos.html", cursos=cursos)

@app.route("/curso/<int:id>")
@login_required
def curso_detalle(id):
    conn = get_connection()
    curso = conn.execute("SELECT * FROM cursos WHERE id=?", (id,)).fetchone()
    estudiantes = conn.execute("SELECT u.nombre FROM inscripciones i JOIN usuarios u ON i.usuario_id = u.id WHERE i.curso_id=?", (id,)).fetchall()
    conn.close()
    return render_template("curso_detalle.html", curso=curso, estudiantes=estudiantes)

@app.route("/inscribir/<int:curso_id>")
@login_required
def inscribir(curso_id):
    conn = get_connection()
    conn.execute("INSERT INTO inscripciones (usuario_id, curso_id) VALUES (?, ?)", (current_user.id, curso_id))
    conn.commit()
    conn.close()
    return redirect(url_for("curso_detalle", id=curso_id))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")