let selectedImage=null;

function addImage(){

let url=document.getElementById("imageUrl").value;

if(url==="") return;

let img=document.createElement("img");

img.src=url;

img.onclick=()=>selectImage(img);

document.getElementById("gallery").appendChild(img);

}

function selectImage(img){

document.querySelectorAll("#gallery img").forEach(i=>i.classList.remove("selected"));

img.classList.add("selected");

selectedImage=img;

}

function deleteImage(){

if(selectedImage){

selectedImage.remove();

selectedImage=null;

}

}



const nombre=document.getElementById("nombre");
const email=document.getElementById("email");
const password=document.getElementById("password");
const confirmPassword=document.getElementById("confirmPassword");
const edad=document.getElementById("edad");
const submitBtn=document.getElementById("submitBtn");

function validar(){

let valid=true;

if(nombre.value.length<3){
errorNombre.innerText="Mínimo 3 caracteres";
valid=false;
}else{
errorNombre.innerText="";
}

let regex=/^[^\s@]+@[^\s@]+\.[^\s@]+$/;

if(!regex.test(email.value)){
errorEmail.innerText="Correo inválido";
valid=false;
}else{
errorEmail.innerText="";
}

let passRegex=/^(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$/;

if(!passRegex.test(password.value)){
errorPassword.innerText="8 caracteres, número y símbolo";
valid=false;
}else{
errorPassword.innerText="";
}

if(password.value!==confirmPassword.value){
errorConfirm.innerText="No coincide";
valid=false;
}else{
errorConfirm.innerText="";
}

if(edad.value<18){
errorEdad.innerText="Debes ser mayor de edad";
valid=false;
}else{
errorEdad.innerText="";
}

submitBtn.disabled=!valid;

}

document.querySelectorAll("#formulario input").forEach(input=>{
input.addEventListener("input",validar);
});

document.getElementById("formulario").addEventListener("submit",function(e){

e.preventDefault();

alert("Formulario enviado correctamente");

});



let productos=[

{
nombre:"Kit Robótica Básica",
precio:150,
descripcion:"Construye tu primer robot"
},

{
nombre:"Sensor Inteligente",
precio:40,
descripcion:"Sensor para robots"
}

];

function renderProductos(){

let lista=document.getElementById("listaProductos");

lista.innerHTML="";

productos.forEach(producto=>{

let li=document.createElement("li");

li.innerHTML=

"<strong>"+producto.nombre+"</strong> - $"+producto.precio+
"<br>"+producto.descripcion;

lista.appendChild(li);

});

}

function agregarProducto(){

let nombre=document.getElementById("productoNombre").value;
let precio=document.getElementById("productoPrecio").value;
let descripcion=document.getElementById("productoDescripcion").value;

let nuevo={

nombre:nombre,
precio:precio,
descripcion:descripcion

};

productos.push(nuevo);

renderProductos();

}

document.addEventListener("DOMContentLoaded",renderProductos);