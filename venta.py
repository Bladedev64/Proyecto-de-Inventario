# Clase Venta, solo getters porque no se cambia
class Venta:
    def __init__(self, venta_id, cant_articulos, medio_pago, total, productos, fecha=None):
        if medio_pago is None or medio_pago.strip() == "":
            raise ValueError("Falta el medio de pago.")
        if float(total) < 0:
            raise ValueError("El total no puede ser negativo.")
        self._venta_id = venta_id
        self._cant_articulos = int(cant_articulos)  # unidades vendidas
        self._medio_pago = medio_pago.strip()
        self._total = float(total)
        self._productos = int(productos)  # productos distintos
        self._fecha = fecha

    @property
    def venta_id(self):
        return self._venta_id

    @property
    def cant_articulos(self):
        return self._cant_articulos

    @property
    def medio_pago(self):
        return self._medio_pago

    @property
    def total(self):
        return self._total

    @property
    def productos(self):
        return self._productos

    @property
    def fecha(self):
        return self._fecha
