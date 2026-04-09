# Clase Producto para POO
class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"{self.id} - {self.nombre}: {self.cantidad} unidades a ${self.precio}"    