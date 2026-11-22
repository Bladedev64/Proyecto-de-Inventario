STOCK_MINIMO = 5

# el estado de un producto puede ser "ok", "bajo" o "agotado"
# y esto es lo que se ve en las tablas
ETIQUETAS = {"ok": "Bien", "bajo": "Poco stock", "agotado": "Agotado"}


# Clase Producto
# los setters revisan cada dato antes de guardarlo
class Producto:
    def __init__(self, producto_id, nombre, descripcion, precio, cantidad_stock,
                 proveedor, stock_minimo=STOCK_MINIMO):
        self.producto_id = producto_id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad_stock = cantidad_stock
        self.proveedor = proveedor
        self.stock_minimo = stock_minimo

    # NOMBRE
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or valor.strip() == "":
            raise ValueError("Pon el nombre del equipo.")
        self._nombre = valor.strip()

    # DESCRIPCION
    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        if valor is None:
            valor = ""
        self._descripcion = valor.strip()

    # PROVEEDOR
    @property
    def proveedor(self):
        return self._proveedor

    @proveedor.setter
    def proveedor(self, valor):
        if valor is None:
            valor = ""
        self._proveedor = valor.strip()

    # PRECIO
    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        try:
            precio = float(valor)
        except ValueError:
            raise ValueError("El costo va así: 25.50")
        if precio < 0:
            raise ValueError("El costo no puede ser negativo.")
        self._precio = precio

    # STOCK
    @property
    def cantidad_stock(self):
        return self._cantidad_stock

    @cantidad_stock.setter
    def cantidad_stock(self, valor):
        try:
            stock = int(valor)
        except ValueError:
            raise ValueError("El stock va sin decimales, ej: 5")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._cantidad_stock = stock

    # STOCK MINIMO, si quedan esas unidades o menos sale como faltante
    @property
    def stock_minimo(self):
        return self._stock_minimo

    @stock_minimo.setter
    def stock_minimo(self, valor):
        try:
            minimo = int(valor)
        except ValueError:
            raise ValueError("El mínimo va sin decimales, ej: 5")
        if minimo < 0:
            raise ValueError("El mínimo no puede ser negativo.")
        self._stock_minimo = minimo

    # cuanto vale todo el stock de este producto
    @property
    def valor_en_stock(self):
        return self.precio * self.cantidad_stock

    # es la misma regla que esta en prolog/reglas.pl, la uso aqui para pintar las tablas
    @property
    def estado(self):
        if self.cantidad_stock <= 0:
            return "agotado"
        if self.cantidad_stock <= self.stock_minimo:
            return "bajo"
        return "ok"

    @property
    def etiqueta(self):
        return ETIQUETAS[self.estado]
