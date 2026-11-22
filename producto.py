# Clase Producto
class Producto:
    def __init__(self, prodId, nombre, desc, precio, stock, prov):
        self.producto_id = prodId
        self._nombre = nombre
        self._desc = desc
        self._precio = precio
        self._stock = stock
        self._prov = prov

    # NOMBRE
    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    # DESCRIPCION
    @property
    def descripcion(self):
        return self._desc
    @descripcion.setter
    def descripcion(self, valor):
        self._desc = valor
    
    # PRECIO  
    @property
    def precio(self):
        return self._precio
    @precio.setter
    def precio(self, valor):
        self._precio = valor
    
    # STOCK
    @property
    def cantidad_stock(self):
        return self._stock
    @cantidad_stock.setter
    def cantidad_stock(self, valor):
        self._stock = valor

    # PROVEEDOR
    @property
    def proveedor(self):
        return self._prov
    @proveedor.setter
    def proveedor(self, valor):
        self._prov = valor

    # OBTENER DETALLES
    def verDetalles(self):
        info = f"ID: {self.producto_id}\nNombre: {self.nombre}\nDescripción: {self.descripcion}\n"
        info += f"Precio: {self.precio}\nStock: {self.cantidad_stock}\nProveedor: {self.proveedor}"
        return info