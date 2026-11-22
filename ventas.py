from venta import Venta


# Clase Ventas
# guarda la lista de ventas y registra las nuevas
class Ventas:
    def __init__(self, db, inventario):
        self.db = db
        self.inventario = inventario
        self.ventas = []
        self.recargar()

    def recargar(self):
        self.ventas = self.db.traerVentas()

    def ingresos(self):
        total = 0
        for v in self.ventas:
            total += v.total
        return total

    def registrarVenta(self, lineas, medio_pago):
        # lineas es una lista de (Producto, cantidad)
        if len(lineas) == 0:
            raise ValueError("La lista está vacía, añade algún equipo.")
        for producto, cantidad in lineas:
            if cantidad <= 0:
                raise ValueError("La cantidad mínima es 1.")
            if cantidad > producto.cantidad_stock:
                raise ValueError(f"No alcanza: de \"{producto.nombre}\" solo quedan {producto.cantidad_stock}.")

        unidades = 0
        total = 0
        ids = []
        for producto, cantidad in lineas:
            unidades += cantidad
            total += producto.precio * cantidad
            ids.append((producto.producto_id, cantidad))
        venta = Venta(None, unidades, medio_pago, round(total, 2), len(lineas))
        try:
            self.db.registrarVenta(venta, ids)
        finally:
            # aunque falle vuelvo a leer todo para ver el stock como esta en la base
            self.inventario.recargar()
            self.recargar()
        return venta
