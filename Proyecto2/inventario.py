class Producto:

    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio


class Inventario:

    def __init__(self):
        self.productos = {}   # diccionario

    def agregar_producto(self, producto):
        self.productos[producto.id] = producto

    def eliminar_producto(self, id):
        if id in self.productos:
            del self.productos[id]

    def mostrar_productos(self):
        return self.productos.values()
    