// Obtener elementos
const formulario = document.getElementById('formulario');
const nombre = document.getElementById('nombre');
const correo = document.getElementById('correo');
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirmPassword');
const edad = document.getElementById('edad');

const btnEnviar = document.getElementById('btnEnviar');

// Expresiones regulares
const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const regexPassword = /^(?=.*[0-9])(?=.*[!@#$%^&*])/;

// Validar en tiempo real
nombre.addEventListener('input', validarNombre);
correo.addEventListener('input', validarCorreo);
password.addEventListener('input', validarPassword);
confirmPassword.addEventListener('input', validarConfirmPassword);
edad.addEventListener('input', validarEdad);

formulario.addEventListener('input', activarEnvio);

formulario.addEventListener('submit', function(e) {
    e.preventDefault();
    alert("¡Formulario enviado con éxito!");
    formulario.reset();
    btnEnviar.disabled = true;
});

// Funciones de validación
function validarNombre() {
    const error = document.getElementById('error-nombre');
    if (nombre.value.trim().length < 3) {
        nombre.classList.add('invalid');
        nombre.classList.remove('valid');
        error.textContent = "El nombre debe tener al menos 3 caracteres.";
        return false;
    }
    nombre.classList.add('valid');
    nombre.classList.remove('invalid');
    error.textContent = "";
    return true;
}

function validarCorreo() {
    const error = document.getElementById('error-correo');
    if (!regexEmail.test(correo.value)) {
        correo.classList.add('invalid');
        correo.classList.remove('valid');
        error.textContent = "Correo electrónico no válido.";
        return false;
    }
    correo.classList.add('valid');
    correo.classList.remove('invalid');
    error.textContent = "";
    return true;
}

function validarPassword() {
    const error = document.getElementById('error-password');
    if (!regexPassword.test(password.value) || password.value.length < 8) {
        password.classList.add('invalid');
        password.classList.remove('valid');
        error.textContent = "La contraseña debe tener mínimo 8 caracteres, un número y un carácter especial.";
        return false;
    }
    password.classList.add('valid');
    password.classList.remove('invalid');
    error.textContent = "";
    return true;
}

function validarConfirmPassword() {
    const error = document.getElementById('error-confirmPassword');
    if (confirmPassword.value !== password.value || confirmPassword.value === "") {
        confirmPassword.classList.add('invalid');
        confirmPassword.classList.remove('valid');
        error.textContent = "Las contraseñas no coinciden.";
        return false;
    }
    confirmPassword.classList.add('valid');
    confirmPassword.classList.remove('invalid');
    error.textContent = "";
    return true;
}

function validarEdad() {
    const error = document.getElementById('error-edad');
    if (parseInt(edad.value) < 18 || edad.value === "") {
        edad.classList.add('invalid');
        edad.classList.remove('valid');
        error.textContent = "Debes ser mayor o igual a 18 años.";
        return false;
    }
    edad.classList.add('valid');
    edad.classList.remove('invalid');
    error.textContent = "";
    return true;
}

function activarEnvio() {
    if (validarNombre() && validarCorreo() && validarPassword() && validarConfirmPassword() && validarEdad()) {
        btnEnviar.disabled = false;
    } else {
        btnEnviar.disabled = true;
    }
}
