// --- ELEMENTOS DEL DOM ---
const inputUrl = document.getElementById('urlImagen');
const btnAgregar = document.getElementById('btnAgregar');
const btnEliminar = document.getElementById('btnEliminar');
const galeria = document.getElementById('galeria');

let imagenSeleccionada = null;

// --- FUNCIÓN PARA VALIDAR QUE LA URL SEA DE IMAGEN ---
function esUrlImagen(url) {
    try {
        new URL(url); // Verifica formato válido de URL
    } catch {
        return false;
    }
    // Verifica extensión de imagen
    return /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(url);
}

// --- AGREGAR IMAGEN ---
btnAgregar.addEventListener('click', () => {
  const url = inputUrl.value.trim();

  if (!esUrlImagen(url)) {
    alert("Por favor ingresa una URL de imagen válida (termina en .jpg, .png, etc.)");
    return;
  }

  const nuevaImagen = document.createElement('img');
  nuevaImagen.src = url;
  nuevaImagen.alt = "Imagen de la galería";

  nuevaImagen.addEventListener('click', () => seleccionarImagen(nuevaImagen));
  
  galeria.appendChild(nuevaImagen);
  inputUrl.value = '';
});

// --- SELECCIONAR UNA IMAGEN ---
function seleccionarImagen(imagen) {
  if (imagenSeleccionada) {
    imagenSeleccionada.classList.remove('seleccionada');
  }
  imagenSeleccionada = imagen;
  imagenSeleccionada.classList.add('seleccionada');
}

// --- ELIMINAR IMAGEN SELECCIONADA ---
btnEliminar.addEventListener('click', () => {
  if (!imagenSeleccionada) {
    alert("No hay ninguna imagen seleccionada");
    return;
  }
  galeria.removeChild(imagenSeleccionada);
  imagenSeleccionada = null;
});

