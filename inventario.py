# Clase Inventario
# tiene la lista de productos. Cada cambio se guarda primero en MySQL
# y despues vuelvo a leer la lista para que quede igual que la base
from producto import Producto, STOCK_MINIMO


class Inventario:
    def __init__(self, db):
        self.db = db
        self.productos = []
        self.recargar()

    def recargar(self):
        self.productos = self.db.traerProductos()

    def buscarProducto(self, producto_id):
        for p in self.productos:
            if p.producto_id == producto_id:
                return p
        return None

    def listaProveedores(self):
        proveedores = []
        for p in self.productos:
            if p.proveedor != "" and p.proveedor not in proveedores:
                proveedores.append(p.proveedor)
        proveedores.sort()
        return proveedores

    def filtrarProductos(self, texto="", estado=None):
        texto = texto.strip().lower()
        lista = []
        for p in self.productos:
            todo = (p.nombre + " " + p.descripcion + " " + p.proveedor).lower()
            if texto in todo:
                if estado is None or p.estado == estado:
                    lista.append(p)
        return lista

    def resumen(self):
        # los numeros que salen en la pestaña Inicio
        unidades = 0
        valor = 0
        agotados = 0
        bajos = 0
        for p in self.productos:
            unidades += p.cantidad_stock
            valor += p.valor_en_stock
            if p.estado == "agotado":
                agotados += 1
            elif p.estado == "bajo":
                bajos += 1
        promedio = 0
        if unidades > 0:
            promedio = valor / unidades
        return {
            "productos": len(self.productos),
            "unidades": unidades,
            "valor": valor,
            "promedio": promedio,
            "agotados": agotados,
            "bajos": bajos,
            "faltan": agotados + bajos,
        }

    # si un dato esta mal Producto() lanza ValueError y no se guarda nada

    def agregarProducto(self, nombre, descripcion, precio, cantidad_stock, proveedor, stock_minimo=STOCK_MINIMO):
        producto = Producto(None, nombre, descripcion, precio, cantidad_stock, proveedor, stock_minimo)
        self.db.insertarProducto(producto)
        self.recargar()

    def modificarProducto(self, producto_id, nombre, descripcion, precio, cantidad_stock, proveedor, stock_minimo):
        producto = Producto(producto_id, nombre, descripcion, precio, cantidad_stock, proveedor, stock_minimo)
        self.db.cambiarProducto(producto)
        self.recargar()

    def borrarProducto(self, producto):
        self.db.borrarProducto(producto)
        self.recargar()
