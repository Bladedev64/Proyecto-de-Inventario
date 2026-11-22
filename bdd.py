# Clase BaseDatos
# aqui esta todo lo que tiene que ver con MySQL
import os

import mysql.connector

from producto import Producto
from venta import Venta

# datos para entrar a MySQL. Si tu MySQL tiene otra clave cambiala aqui
HOST = "localhost"
PUERTO = 3306
USUARIO = "root"
CLAVE = "root"
BASE = "inventario_db"

ARCHIVO_SQL = os.path.join(os.path.dirname(__file__), "base_datos.sql")


class ErrorBaseDatos(Exception):
    pass


class BaseDatos:
    def __init__(self):
        self.con = None
        self.conectar()
        self.crearTablas()

    def conectar(self):
        try:
            self.con = mysql.connector.connect(host=HOST, port=PUERTO, user=USUARIO, password=CLAVE)
        except mysql.connector.Error:
            # en XAMPP el usuario root no tiene clave, entonces pruebo sin clave
            try:
                self.con = mysql.connector.connect(host=HOST, port=PUERTO, user=USUARIO, password="")
            except mysql.connector.Error as err:
                raise ErrorBaseDatos(f"No hay conexión con MySQL: {err}")

        cur = self.con.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {BASE}")
        cur.execute(f"USE {BASE}")
        cur.close()

    def cerrar(self):
        if self.con:
            self.con.close()

    # TABLAS

    def crearTablas(self):
        # las tablas y los productos de prueba estan en base_datos.sql
        f = open(ARCHIVO_SQL, encoding="utf-8")
        lineas = []
        for linea in f:
            if not linea.startswith("--"):
                lineas.append(linea)
        f.close()
        ordenes = "".join(lineas).split(";")

        cur = self.con.cursor()
        for orden in ordenes:
            if orden.strip().startswith("CREATE TABLE"):
                cur.execute(orden)

        # los productos de prueba solo se meten si la tabla esta vacia
        cur.execute("SELECT COUNT(*) FROM productos")
        cantidad = cur.fetchone()[0]
        if cantidad == 0:
            for orden in ordenes:
                if orden.strip().startswith("INSERT"):
                    cur.execute(orden)
        self.con.commit()
        cur.close()

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
        # lineas es una lista de (producto_id, cantidad)
        # primero bajo el stock de cada producto y despues guardo la venta.
        # Si algo falla hago rollback para que no quede la mitad guardada
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
