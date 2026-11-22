import tkinter as tk
from tkinter import ttk, messagebox
from bdd import BaseDatos
from inventario import Inventario
from producto import Producto
from venta import Venta
from ventas import Ventas
from prolog.motor_prolog import revisarStock


class InterfazInventario:
    def __init__(self, root):
        self.db = BaseDatos(
            host="localhost",
            user="root",
            password="root",
            database="inventario_db"
        )
        self.inventario = Inventario()
        self.ventas = Ventas()
        self.cargarDatos()

        self.root = root
        self.root.title("Sistema de Gestión de Inventarios")
        self.root.geometry("800x450")
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=True, fill="both")

        self.tabAgregar = ttk.Frame(self.tabs)
        self.tabModificar = ttk.Frame(self.tabs)
        self.tabStats = ttk.Frame(self.tabs)
        self.tabVentas = ttk.Frame(self.tabs)

        self.tabs.add(self.tabAgregar, text="Agregar Producto")
        self.tabs.add(self.tabModificar, text="Modificar Producto")
        self.tabs.add(self.tabStats, text="Estadísticas")
        self.tabs.add(self.tabVentas, text="Ventas")

        self.armarAgregar()
        self.armarModificar()
        self.armarBotonEliminar()
        self.armarBotonInforme()
        self.armarEstadisticas()
        self.armarVentas()
        self.armarBotonVentas()
        self.armarBotonProlog()

    def cargarDatos(self):
        self.inventario.productos = self.db.traerProductos()
        self.ventas.ventas = self.db.traerVentas()

    def actualizarCombo(self, elegido="Seleccionar"):
        nombres = [p.nombre for p in self.inventario.productos]
        self.combo["values"] = ["Seleccionar"] + nombres
        self.combo.set(elegido if elegido in nombres else "Seleccionar")

    def armarAgregar(self):
        campos = ["Nombre del Producto", "Descripción", "Precio", "Stock", "Proveedor"]
        self.cajasAgregar = {}
        for i, campo in enumerate(campos):
            tk.Label(self.tabAgregar, text=campo, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5)
            caja = tk.Entry(self.tabAgregar, font=("Arial", 12))
            caja.grid(row=i, column=1, padx=10, pady=5)
            self.cajasAgregar[campo] = caja

        tk.Button(
            self.tabAgregar, text="Agregar Producto", command=self.guardarProducto,
            font=("Arial", 12), bg="#4CAF50", fg="white"
        ).grid(row=len(campos) + 1, column=0, columnspan=2, pady=10)

    def armarModificar(self):
        campos = ["Seleccione Producto:", "Nombre del Producto", "Descripción", "Precio", "Stock", "Proveedor"]
        self.combo = ttk.Combobox(
            self.tabModificar,
            values=["Seleccionar"] + [p.nombre for p in self.inventario.productos],
            font=("Arial", 12),
            state="readonly"
        )
        self.combo.grid(row=0, column=1, padx=10, pady=5)
        self.combo.set("Seleccionar")
        self.combo.bind("<<ComboboxSelected>>", self.llenarCampos)

        self.cajasEditar = {}
        for i, campo in enumerate(campos[1:]):
            tk.Label(self.tabModificar, text=campo, font=("Arial", 12)).grid(row=i + 1, column=0, padx=10, pady=5)
            caja = tk.Entry(self.tabModificar, font=("Arial", 12))
            caja.grid(row=i + 1, column=1, padx=10, pady=5)
            self.cajasEditar[campo] = caja

        tk.Button(
            self.tabModificar, text="Modificar Producto", command=self.editarProducto,
            font=("Arial", 12), bg="#008CBA", fg="white"
        ).grid(row=len(campos) + 1, column=0, columnspan=2, pady=10)

    def armarEstadisticas(self):
        for item in self.tabStats.winfo_children():
            item.destroy()

        distintos = len(self.inventario.productos)
        totalStock = sum(p.cantidad_stock for p in self.inventario.productos)
        valorTotal = sum(p.precio * p.cantidad_stock for p in self.inventario.productos)
        promedio = valorTotal / totalStock if totalStock > 0 else 0

        textos = [
            f"Cantidad productos distintos: {distintos}",
            f"Cantidad Total de Productos: {totalStock}",
            f"Valor Total del Inventario: ${valorTotal:.2f}",
            f"Precio Promedio de Productos: ${promedio:.2f}"
        ]

        for i, texto in enumerate(textos):
            tk.Label(self.tabStats, text=texto, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5, sticky="nsew")

        self.root.after(1000, self.armarEstadisticas)

    def armarBotonEliminar(self):
        tk.Button(
            self.tabModificar, text="Eliminar Producto", command=self.borrarProducto,
            font=("Arial", 12), bg="#FF5733", fg="white"
        ).grid(row=8, column=0, columnspan=2, pady=10)

    def armarBotonInforme(self):
        tk.Button(
            self.root, text="Mostrar Informe", command=self.verInforme,
            font=("Arial", 12), bg="#333", fg="white"
        ).pack(pady=5)

    def armarVentas(self):
        campos = ["Cantidad Artículos", "Medio de Pago", "Total", "Productos"]
        self.cajasVentas = {}
        for i, campo in enumerate(campos):
            tk.Label(self.tabVentas, text=campo, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5)
            caja = tk.Entry(self.tabVentas, font=("Arial", 12))
            caja.grid(row=i, column=1, padx=10, pady=5)
            self.cajasVentas[campo] = caja

        tk.Button(
            self.tabVentas, text="Agregar Venta", command=self.guardarVenta,
            font=("Arial", 12), bg="#4CAF50", fg="white"
        ).grid(row=len(campos) + 1, column=0, columnspan=2, pady=10)

    def armarBotonVentas(self):
        tk.Button(
            self.root, text="Mostrar Ventas", command=self.verVentas,
            font=("Arial", 12), bg="#333", fg="white"
        ).pack(pady=5)

    def armarBotonProlog(self):
        tk.Button(
            self.root, text="Revisar Prolog", command=self.verAlertasProlog,
            font=("Arial", 12), bg="#6A1B9A", fg="white"
        ).pack(pady=5)

    def guardarVenta(self):
        try:
            cant = self.cajasVentas["Cantidad Artículos"].get().strip()
            pago = self.cajasVentas["Medio de Pago"].get().strip()
            total = float(self.cajasVentas["Total"].get())
            cantProd = int(self.cajasVentas["Productos"].get())

            if not cant or not pago:
                messagebox.showerror("Error", "Complete cantidad de artículos y medio de pago.")
                return

            venta = Venta(None, cant, pago, total, cantProd)
            nuevoId = self.db.insertarVenta(venta)
            if nuevoId is not None:
                self.ventas.agregarVenta(venta)
                for caja in self.cajasVentas.values():
                    caja.delete(0, tk.END)
                messagebox.showinfo("Éxito", "Venta registrada correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese datos válidos para la venta.")

    def verVentas(self):
        lista = self.ventas.hacerInforme()
        texto = "\n\n".join(lista) if lista else "No hay ventas registradas."
        self.abrirVentanaTexto("Informe de Ventas", texto)

    def guardarProducto(self):
        try:
            nombre = self.cajasAgregar["Nombre del Producto"].get().strip()
            desc = self.cajasAgregar["Descripción"].get().strip()
            precio = float(self.cajasAgregar["Precio"].get())
            stock = int(self.cajasAgregar["Stock"].get())
            prov = self.cajasAgregar["Proveedor"].get().strip()

            if not nombre:
                messagebox.showerror("Error", "Ingrese el nombre del producto.")
                return

            prod = Producto(None, nombre, desc, precio, stock, prov)
            nuevoId = self.db.insertarProducto(prod)
            if nuevoId is not None:
                self.inventario.agregarProducto(prod)
                self.actualizarCombo(self.combo.get())
                for caja in self.cajasAgregar.values():
                    caja.delete(0, tk.END)
                messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese datos válidos para el producto.")

    def llenarCampos(self, event):
        elegido = self.combo.get()
        if elegido != "Seleccionar":
            prod = next((p for p in self.inventario.productos if p.nombre == elegido), None)
            if prod:
                self.cajasEditar["Nombre del Producto"].delete(0, tk.END)
                self.cajasEditar["Nombre del Producto"].insert(0, prod.nombre)
                self.cajasEditar["Descripción"].delete(0, tk.END)
                self.cajasEditar["Descripción"].insert(0, prod.descripcion or "")
                self.cajasEditar["Precio"].delete(0, tk.END)
                self.cajasEditar["Precio"].insert(0, str(prod.precio))
                self.cajasEditar["Stock"].delete(0, tk.END)
                self.cajasEditar["Stock"].insert(0, str(prod.cantidad_stock))
                self.cajasEditar["Proveedor"].delete(0, tk.END)
                self.cajasEditar["Proveedor"].insert(0, prod.proveedor or "")

    def editarProducto(self):
        elegido = self.combo.get()
        if elegido == "Seleccionar":
            messagebox.showerror("Error", "Seleccione un producto para modificar.")
            return

        prod = next((p for p in self.inventario.productos if p.nombre == elegido), None)
        if not prod:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        nombre = self.cajasEditar["Nombre del Producto"].get().strip()
        desc = self.cajasEditar["Descripción"].get().strip()
        precio = self.cajasEditar["Precio"].get().strip()
        stock = self.cajasEditar["Stock"].get().strip()
        prov = self.cajasEditar["Proveedor"].get().strip()

        if not (nombre and precio and stock and prov and desc):
            messagebox.showerror("Error", "Complete nombre, descripción, precio, stock y proveedor.")
            return

        try:
            prod.nombre = nombre
            prod.descripcion = desc
            prod.precio = float(precio)
            prod.cantidad_stock = int(stock)
            prod.proveedor = prov

            self.db.cambiarProducto(prod)
            self.inventario.productos = self.db.traerProductos()
            self.actualizarCombo(prod.nombre)
            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese datos válidos para precio y stock.")

    def borrarProducto(self):
        elegido = self.combo.get()
        if elegido == "Seleccionar":
            messagebox.showerror("Error", "Seleccione un producto para eliminar.")
            return

        prod = next((p for p in self.inventario.productos if p.nombre == elegido), None)
        if not prod:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        self.db.borrarProducto(prod)
        self.inventario.borrarProducto(prod)
        self.actualizarCombo("Seleccionar")
        for caja in self.cajasEditar.values():
            caja.delete(0, tk.END)
        messagebox.showinfo("Éxito", "Producto eliminado correctamente.")

    def verInforme(self):
        lista = self.inventario.hacerInforme()
        texto = "\n\n".join(lista) if lista else "No hay productos en el inventario."
        self.abrirVentanaTexto("Informe de Inventarios", texto)

    def abrirVentanaTexto(self, titulo, texto):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)

        marco = tk.Frame(ventana)
        marco.pack(fill="both", expand=True)

        scroll = ttk.Scrollbar(marco, orient="vertical")
        scroll.pack(side="right", fill="y")

        area = tk.Text(marco, yscrollcommand=scroll.set)
        area.pack(fill="both", expand=True)
        area.insert("1.0", texto)
        scroll.config(command=area.yview)

    def verAlertasProlog(self):
        try:
            alertas = revisarStock(self.inventario.productos)

            if not alertas:
                messagebox.showinfo("Prolog", "Todo el inventario está bien por ahora.")
                return

            texto = "\n".join(
                f"- {nom}: stock {stock} (mín {minimo}) -> {estado}"
                for nom, stock, minimo, estado in alertas
            )
            messagebox.showwarning("Alertas Prolog", texto)
        except Exception as err:
            messagebox.showerror("Error Prolog", f"No se pudo revisar con Prolog:\n{err}")

    def cerrar(self):
        self.db.cerrar()
        self.root.destroy()