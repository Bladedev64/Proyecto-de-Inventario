# Clase Ventas
class Ventas:
    def __init__(self):
        self.ventas = []

    def agregarVenta(self, venta):
        self.ventas.append(venta)

    def borrarVenta(self, venta):
        self.ventas = [v for v in self.ventas if v.venta_id != venta.venta_id]

    def hacerInforme(self):
        reporte = [venta.verVenta() for venta in self.ventas]
        return reporte