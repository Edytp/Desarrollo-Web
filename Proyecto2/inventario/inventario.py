from .productos import Producto

class Inventario:
    def __init__(self):
        self.productos = {}  # diccionario id -> Producto

    def agregar_producto(self, producto):
        self.productos[producto.id] = producto

    def eliminar_producto(self, id):
        if id in self.productos:
            del self.productos[id]

    def actualizar_producto(self, id, nombre=None, cantidad=None, precio=None):
        if id in self.productos:
            if nombre: self.productos[id].nombre = nombre
            if cantidad: self.productos[id].cantidad = cantidad
            if precio: self.productos[id].precio = precio

    def buscar_por_nombre(self, nombre):
        return [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]

    def mostrar_todos(self):
        return list(self.productos.values())