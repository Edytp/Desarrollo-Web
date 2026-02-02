function mostrarAlerta() {
    alert("¡Gracias por visitar nuestra página elegante!");
}

document.getElementById("formulario").addEventListener("submit", function (e) {
    e.preventDefault();

    let nombre = document.getElementById("nombre").value.trim();
    let email = document.getElementById("email").value.trim();
    let mensaje = document.getElementById("mensaje").value.trim();

    let valido = true;

    document.getElementById("errorNombre").textContent = "";
    document.getElementById("errorEmail").textContent = "";
    document.getElementById("errorMensaje").textContent = "";

    if (nombre === "") {
        document.getElementById("errorNombre").textContent = "El nombre es obligatorio";
        valido = false;
    }

    if (email === "") {
        document.getElementById("errorEmail").textContent = "El correo es obligatorio";
        valido = false;
    }

    if (mensaje === "") {
        document.getElementById("errorMensaje").textContent = "El mensaje es obligatorio";
        valido = false;
    }

    if (valido) {
        alert("Formulario enviado correctamente");
        document.getElementById("formulario").reset();
    }
});
