const productos = [
    {
        nombre: "Filtro de aceite",
        precio: 15,
        descripcion: "Filtro para motor de alto rendimiento"
    },
    {
        nombre: "Pastillas de freno",
        precio: 45,
        descripcion: "Juego de pastillas delanteras"
    }
];

const listaProductos = document.getElementById("lista-productos");
const inputNombre = document.getElementById("nombre");
const inputPrecio = document.getElementById("precio");
const inputDescripcion = document.getElementById("descripcion");
const btnAgregar = document.getElementById("btn-agregar");

function renderizarProductos() {
    listaProductos.innerHTML = "";

    productos.forEach(producto => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>${producto.nombre}</strong><br>
            Precio: $${producto.precio}<br>
            ${producto.descripcion}
        `;
        listaProductos.appendChild(li);
    });
}

btnAgregar.addEventListener("click", () => {
    if (
        inputNombre.value === "" ||
        inputPrecio.value === "" ||
        inputDescripcion.value === ""
    ) {
        alert("Completa todos los campos");
        return;
    }

    productos.push({
        nombre: inputNombre.value,
        precio: inputPrecio.value,
        descripcion: inputDescripcion.value
    });

    renderizarProductos();

    inputNombre.value = "";
    inputPrecio.value = "";
    inputDescripcion.value = "";
});

renderizarProductos();


