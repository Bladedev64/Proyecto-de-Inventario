import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from producto import Producto
from venta import Venta


class BaseDatos:
    def __init__(self, host="localhost", user="root", password="", database="inventario_db", port=3306):
        self.datos = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "port": port,
        }
        self.con = None
        self.cur = None
        self.conectar()
        self.iniciarTablas()  # CREATE + UPDATE automático al ejecutar

    def conectar(self):
        try:
            self.con = mysql.connector.connect(**self.datos)
            self.cur = self.con.cursor()
        except Error as err:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a MySQL:\n{err}")
            raise

    def revisarConexion(self):
        if self.con is None or not self.con.is_connected():
            self.conectar()

    def existeColumna(self, tabla, col):
        consulta = """
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s
              AND COLUMN_NAME = %s
        """
        self.cur.execute(consulta, (tabla, col))
        return self.cur.fetchone()[0] > 0

    def iniciarTablas(self):
        """Crea las tablas si no existen (CREATE) y agrega columnas nuevas si faltan (UPDATE)."""
        self.revisarConexion()
        try:
            # 1. CREATE de tablas
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    producto_id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(150) NOT NULL,
                    descripcion TEXT,
                    precio DOUBLE NOT NULL,
                    cantidad_stock INT NOT NULL,
                    proveedor VARCHAR(150)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)

            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    venta_id INT AUTO_INCREMENT PRIMARY KEY,
                    cant_articulos VARCHAR(100) NOT NULL,
                    medio_pago VARCHAR(100) NOT NULL,
                    total DOUBLE NOT NULL,
                    productos INT NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)

            # 2. UPDATE automático de columnas (agrega aquí futuras columnas si cambias el modelo)
            cambios = [
                ("productos", "stock_minimo", "INT NOT NULL DEFAULT 5"),
                ("ventas", "fecha_registro", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
            ]

            for tabla, col, tipo in cambios:
                if not self.existeColumna(tabla, col):
                    self.cur.execute(f"ALTER TABLE `{tabla}` ADD COLUMN `{col}` {tipo}")

            self.con.commit()
        except Error as err:
            self.con.rollback()
            messagebox.showerror("Error en esquema BD", f"No se pudo inicializar/actualizar la base de datos:\n{err}")

    # --- MÉTODOS DE PRODUCTOS ---

    def traerProductos(self):
        self.revisarConexion()
        try:
            self.cur.execute("""
                SELECT producto_id, nombre, descripcion, precio, cantidad_stock, proveedor
                FROM productos
                ORDER BY producto_id ASC
            """)
            filas = self.cur.fetchall()
            return [Producto(*fila) for fila in filas]
        except Error as err:
            messagebox.showerror("Error en base de datos", f"No se pudieron obtener los productos:\n{err}")
            return []

    def insertarProducto(self, prod):
        self.revisarConexion()
        try:
            self.cur.execute("""
                INSERT INTO productos (nombre, descripcion, precio, cantidad_stock, proveedor)
                VALUES (%s, %s, %s, %s, %s)
            """, (prod.nombre, prod.descripcion, prod.precio, prod.cantidad_stock, prod.proveedor))
            self.con.commit()
            prod.producto_id = self.cur.lastrowid
            return prod.producto_id
        except Error as err:
            self.con.rollback()
            messagebox.showerror("Error en base de datos", f"No se pudo agregar el producto:\n{err}")
            return None

    def borrarProducto(self, prod):
        self.revisarConexion()
        try:
            self.cur.execute("DELETE FROM productos WHERE producto_id = %s", (prod.producto_id,))
            self.con.commit()
        except Error as err:
            self.con.rollback()
            messagebox.showerror("Error en base de datos", f"No se pudo eliminar el producto:\n{err}")

    def cambiarProducto(self, prod):
        self.revisarConexion()
        try:
            self.cur.execute("""
                UPDATE productos
                SET nombre = %s, descripcion = %s, precio = %s, cantidad_stock = %s, proveedor = %s
                WHERE producto_id = %s
            """, (
                prod.nombre,
                prod.descripcion,
                prod.precio,
                prod.cantidad_stock,
                prod.proveedor,
                prod.producto_id,
            ))
            self.con.commit()
        except Error as err:
            self.con.rollback()
            messagebox.showerror("Error en base de datos", f"No se pudo actualizar el producto:\n{err}")

    def buscarPorNombre(self, nombre):
        self.revisarConexion()
        try:
            self.cur.execute("SELECT * FROM productos WHERE nombre LIKE %s", ("%" + nombre + "%",))
            return self.cur.fetchall()
        except Error as err:
            messagebox.showerror("Error en base de datos", f"No se pudo obtener el producto:\n{err}")
            return []

    def buscarPorProveedor(self, prov):
        self.revisarConexion()
        try:
            self.cur.execute("SELECT * FROM productos WHERE proveedor = %s", (prov,))
            return self.cur.fetchall()
        except Error as err:
            messagebox.showerror("Error en base de datos", f"No se pudo obtener el producto:\n{err}")
            return []

    def buscarPorId(self, prodId):
        self.revisarConexion()
        try:
            self.cur.execute("SELECT * FROM productos WHERE producto_id = %s", (prodId,))
            return self.cur.fetchone()
        except Error as err:
            messagebox.showerror("Error en base de datos", f"No se pudo obtener el producto:\n{err}")
            return None

    # --- MÉTODOS DE VENTAS ---

    def traerVentas(self):
        self.revisarConexion()
        try:
            self.cur.execute("""
                SELECT venta_id, cant_articulos, medio_pago, total, productos
                FROM ventas
                ORDER BY venta_id ASC
            """)
            filas = self.cur.fetchall()
            return [Venta(*fila) for fila in filas]
        except Error as err:
            messagebox.showerror("Error en base de datos", f"No se pudieron obtener las ventas:\n{err}")
            return []

    def insertarVenta(self, venta):
        self.revisarConexion()
        try:
            self.cur.execute("""
                INSERT INTO ventas (cant_articulos, medio_pago, total, productos)
                VALUES (%s, %s, %s, %s)
            """, (venta.cant_articulos, venta.medio_pago, venta.total, venta.productos))
            self.con.commit()
            venta.venta_id = self.cur.lastrowid
            return venta.venta_id
        except Error as err:
            self.con.rollback()
            messagebox.showerror("Error en base de datos", f"No se pudo registrar la venta:\n{err}")
            return None

    def cerrar(self):
        if self.cur:
            self.cur.close()
        if self.con and self.con.is_connected():
            self.con.close()