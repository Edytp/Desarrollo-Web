from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Bienvenido a Innovakids - Plataforma de Robótica y Tecnología"

@app.route("/usuario/<nombre>")
def usuario(nombre):
    return f"Bienvenido {nombre} a Innovakids"

if __name__ == "__main__":
    app.run(debug=True)
