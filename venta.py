from producto import Producto  # Importamos la clase Producto del módulo producto.py


# Clase Venta
class Venta:
    def __init__(self, ventaId, cantArt, medioPago, total, prods):
        self.venta_id = ventaId
        self._cantArt = cantArt
        self._medioPago = medioPago
        self._total = total
        self._prods = prods

    # CANTIDAD ARTICULOS
    @property
    def cant_articulos(self):
        return self._cantArt
    @cant_articulos.setter
    def cant_articulos(self, valor):
        self._cantArt = valor

    # MEDIO DE PAGO
    @property
    def medio_pago(self):
        return self._medioPago
    @medio_pago.setter
    def medio_pago(self, valor):
        self._medioPago = valor
    
    # TOTAL  
    @property
    def total(self):
        return self._total
    @total.setter
    def total(self, valor):
        self._total = valor
    
    # PRODUCTOS
    @property
    def productos(self):
        return self._prods
    @productos.setter
    def productos(self, valor):
        self._prods = valor

    # OBTENER VENTA
    def verVenta(self):
        texto = f"ID: {self.venta_id}\nCantidad de artículos: {self.cant_articulos}\nMedio de pago: {self.medio_pago}\n"
        texto += f"Total: {self.total}\nProductos: {self.productos}"
        return texto