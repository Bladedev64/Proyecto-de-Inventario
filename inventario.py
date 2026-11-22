# Clase Inventario
class Inventario:
    def __init__(self):
        self.productos = []

    def agregarProducto(self, prod):
        self.productos.append(prod)

    def borrarProducto(self, prod):
        self.productos = [p for p in self.productos if p.producto_id != prod.producto_id]

    def buscarProducto(self, prodId):
        for prod in self.productos:
            if prod.producto_id == prodId:
                return prod
        return None

    def hacerInforme(self):
        reporte = [prod.obtener_detalles() for prod in self.productos]
        return reporte