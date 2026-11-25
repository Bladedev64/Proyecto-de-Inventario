# Clase BaseDatos, conexion con MySQL
import mysql.connector

from producto import Producto
from venta import Venta

# datos de MySQL, si tu clave es otra cambiala aqui
HOST = "localhost"
PUERTO = 3306
USUARIO = "root"
CLAVE = "root"
BASE = "inventario_db"


class ErrorBaseDatos(Exception):
    pass


class BaseDatos:
    def __init__(self):
        self.con = None
        self.conectar()

    def conectar(self):
        try:
            self.con = mysql.connector.connect(host=HOST, port=PUERTO, user=USUARIO, password=CLAVE)
        except mysql.connector.Error:
            # en XAMPP root no tiene clave
            try:
                self.con = mysql.connector.connect(host=HOST, port=PUERTO, user=USUARIO, password="")
            except mysql.connector.Error as err:
                raise ErrorBaseDatos(f"No hay conexión con MySQL: {err}")

        # reviso que esten la base y las tablas
        cur = self.con.cursor()
        cur.execute("SHOW DATABASES LIKE %s", (BASE,))
        if cur.fetchone() is None:
            cur.close()
            self.cerrar()
            raise ErrorBaseDatos(f"No existe la base {BASE}")
        cur.execute(f"USE {BASE}")

        cur.execute("SHOW TABLES")
        tablas = []
        for fila in cur.fetchall():
            tablas.append(fila[0])
        cur.close()
        if "productos" not in tablas or "ventas" not in tablas:
            self.cerrar()
            raise ErrorBaseDatos(f"Faltan tablas en {BASE}")

    def cerrar(self):
        if self.con:
            self.con.close()

    # PRODUCTOS

    def traerProductos(self):
        cur = self.con.cursor()
        cur.execute("SELECT producto_id, nombre, descripcion, precio, cantidad_stock, proveedor, stock_minimo "
                    "FROM productos ORDER BY producto_id")
        productos = []
        for fila in cur.fetchall():
            productos.append(Producto(*fila))
        cur.close()
        return productos

    def insertarProducto(self, prod):
        cur = self.con.cursor()
        try:
            cur.execute("INSERT INTO productos (nombre, descripcion, precio, cantidad_stock, proveedor, stock_minimo) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (prod.nombre, prod.descripcion, prod.precio, prod.cantidad_stock,
                         prod.proveedor, prod.stock_minimo))
            self.con.commit()
        except mysql.connector.Error as err:
            raise ErrorBaseDatos(f"No se pudo guardar: {err}")
        finally:
            cur.close()

    def cambiarProducto(self, prod):
        cur = self.con.cursor()
        try:
            cur.execute("UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, cantidad_stock = %s, "
                        "proveedor = %s, stock_minimo = %s WHERE producto_id = %s",
                        (prod.nombre, prod.descripcion, prod.precio, prod.cantidad_stock,
                         prod.proveedor, prod.stock_minimo, prod.producto_id))
            self.con.commit()
        except mysql.connector.Error as err:
            raise ErrorBaseDatos(f"No se pudo guardar: {err}")
        finally:
            cur.close()

    def borrarProducto(self, prod):
        cur = self.con.cursor()
        try:
            cur.execute("DELETE FROM productos WHERE producto_id = %s", (prod.producto_id,))
            self.con.commit()
        except mysql.connector.Error as err:
            raise ErrorBaseDatos(f"No se pudo eliminar: {err}")
        finally:
            cur.close()

    # VENTAS

    def traerVentas(self):
        cur = self.con.cursor()
        cur.execute("SELECT venta_id, cant_articulos, medio_pago, total, productos, fecha_registro "
                    "FROM ventas ORDER BY venta_id")
        ventas = []
        for fila in cur.fetchall():
            ventas.append(Venta(*fila))
        cur.close()
        return ventas

    def registrarVenta(self, venta, lineas):
        # si algo falla hago rollback
        cur = self.con.cursor()
        try:
            for producto_id, cantidad in lineas:
                cur.execute("UPDATE productos SET cantidad_stock = cantidad_stock - %s WHERE producto_id = %s",
                            (cantidad, producto_id))
            cur.execute("INSERT INTO ventas (cant_articulos, medio_pago, total, productos) VALUES (%s, %s, %s, %s)",
                        (venta.cant_articulos, venta.medio_pago, venta.total, venta.productos))
            self.con.commit()
        except mysql.connector.Error as err:
            self.con.rollback()
            raise ErrorBaseDatos(f"No se pudo guardar la venta: {err}")
        finally:
            cur.close()
