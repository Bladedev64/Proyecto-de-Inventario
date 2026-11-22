import tkinter as tk

import ttkbootstrap as tb

from ui.config import AMARILLO_FILA, GRIS, ROJO, ROJO_FILA


# un Label con el tamaño de letra que quiera, en gris o en negrita
def texto(padre, txt="", gris=False, tam=10, negrita=False):
    fuente = f"-size {tam}"
    if negrita:
        fuente += " -weight bold"
    etiqueta = tb.Label(padre, text=txt, font=fuente)
    if gris:
        etiqueta.configure(foreground=GRIS)
    return etiqueta


# Clase Vista, de aqui heredan todas las pestañas
# armar() pone los botones y tablas, refrescar() vuelve a cargar los datos
class Vista(tb.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, padding=(4, 14, 4, 4))
        self.app = app
        self.armar()

    def armar(self):
        pass

    def refrescar(self):
        pass


# Clase Tabla, un Treeview con su barra y un mensaje si esta vacia
# cada columna es (titulo, ancho, lado), lado "w" es izquierda y "e" derecha
class Tabla(tb.Frame):
    def __init__(self, padre, columnas, alto=8, vacio="Sin datos."):
        super().__init__(padre)

        # a cada columna le pongo de nombre su numero: "0", "1", "2"...
        ids = []
        for i in range(len(columnas)):
            ids.append(str(i))

        self.arbol = tb.Treeview(self, columns=ids, show="headings", height=alto, selectmode="browse")
        barra = tb.Scrollbar(self, command=self.arbol.yview)
        self.arbol.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")  # la barra va primero, si no la tabla ocupa todo
        self.arbol.pack(fill="both", expand=True)

        for i in range(len(columnas)):
            titulo, ancho, lado = columnas[i]
            self.arbol.heading(ids[i], text=titulo, anchor=lado)
            # solo las columnas de texto se estiran
            if lado == "w":
                self.arbol.column(ids[i], width=ancho, minwidth=40, anchor=lado, stretch=True)
            else:
                self.arbol.column(ids[i], width=ancho, minwidth=40, anchor=lado, stretch=False)
        self.arbol.tag_configure("bajo", background=AMARILLO_FILA)
        self.arbol.tag_configure("agotado", background=ROJO_FILA)
        self.vacio = texto(self, vacio, gris=True)

    def cargar(self, filas):
        # cada fila es (id, valores, estado). Con "bajo" sale amarilla y con "agotado" roja
        for fila in self.arbol.get_children():
            self.arbol.delete(fila)
        for iid, valores, estado in filas:
            if estado:
                self.arbol.insert("", "end", iid=iid, values=valores, tags=(estado,))
            else:
                self.arbol.insert("", "end", iid=iid, values=valores)
        if len(filas) > 0:
            self.vacio.place_forget()
        else:
            self.vacio.place(relx=0.5, rely=0.5, anchor="center")

    def elegido(self):
        # el id de la fila elegida, o None
        sel = self.arbol.selection()
        if sel:
            return int(sel[0])
        return None


# Ventana para crear o editar un equipo
# si producto es None es uno nuevo, si no se edita ese
class FormProducto(tb.Toplevel):
    def __init__(self, catalogo, producto=None):
        if producto is None:
            titulo = "Nuevo equipo"
        else:
            titulo = "Edita el equipo"
        super().__init__(title=titulo, transient=catalogo.winfo_toplevel(), resizable=(False, False))
        self.catalogo = catalogo
        self.inventario = catalogo.app.inventario
        self.producto = producto

        caja = tb.Frame(self, padding=24)
        caja.pack()

        self.nombre = tk.StringVar()
        self.descripcion = tk.StringVar()
        self.precio = tk.StringVar()
        self.stock = tk.StringVar(value="0")
        self.minimo = tk.StringVar(value="5")
        self.proveedor = tk.StringVar()
        if producto is not None:
            self.nombre.set(producto.nombre)
            self.descripcion.set(producto.descripcion)
            self.precio.set(producto.precio)
            self.stock.set(producto.cantidad_stock)
            self.minimo.set(producto.stock_minimo)
            self.proveedor.set(producto.proveedor)

        texto(caja, "Equipo", gris=True).grid(row=0, column=0, sticky="w", pady=6, padx=(0, 14))
        primero = tb.Entry(caja, textvariable=self.nombre, width=36)
        primero.grid(row=0, column=1, pady=6)
        texto(caja, "Detalle (modelo, capacidad)", gris=True).grid(row=1, column=0, sticky="w", pady=6, padx=(0, 14))
        tb.Entry(caja, textvariable=self.descripcion, width=36).grid(row=1, column=1, pady=6)
        texto(caja, "Cuánto cuesta (S/)", gris=True).grid(row=2, column=0, sticky="w", pady=6, padx=(0, 14))
        tb.Entry(caja, textvariable=self.precio, width=36).grid(row=2, column=1, pady=6)
        texto(caja, "Unidades en almacén", gris=True).grid(row=3, column=0, sticky="w", pady=6, padx=(0, 14))
        tb.Entry(caja, textvariable=self.stock, width=36).grid(row=3, column=1, pady=6)
        texto(caja, "Aviso si quedan", gris=True).grid(row=4, column=0, sticky="w", pady=6, padx=(0, 14))
        tb.Entry(caja, textvariable=self.minimo, width=36).grid(row=4, column=1, pady=6)
        texto(caja, "Compañía", gris=True).grid(row=5, column=0, sticky="w", pady=6, padx=(0, 14))
        tb.Combobox(caja, textvariable=self.proveedor, values=self.inventario.listaProveedores(),
                    width=34).grid(row=5, column=1, pady=6)
        primero.focus_set()

        self.error = texto(caja)
        self.error.configure(foreground=ROJO, wraplength=420)
        self.error.grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 0))
        pie = tb.Frame(caja)
        pie.grid(row=7, column=0, columnspan=2, sticky="e", pady=(14, 0))
        tb.Button(pie, text="Cancela", bootstyle="secondary-outline", command=self.destroy).pack(side="left")
        tb.Button(pie, text="Listo", bootstyle="primary", command=self.guardar).pack(side="left", padx=(8, 0))

        self.place_window_center()
        self.grab_set()

    def guardar(self):
        nombre = self.nombre.get().strip()
        descripcion = self.descripcion.get().strip()
        precio = self.precio.get().strip().replace(",", ".")  # por si escriben 25,50
        stock = self.stock.get().strip()
        minimo = self.minimo.get().strip()
        proveedor = self.proveedor.get().strip()
        try:
            if self.producto is None:
                self.inventario.agregarProducto(nombre, descripcion, precio, stock, proveedor, minimo)
            else:
                self.inventario.modificarProducto(self.producto.producto_id, nombre, descripcion, precio,
                                                  stock, proveedor, minimo)
        except Exception as err:
            # el error puede venir de Producto (dato mal puesto) o de MySQL
            self.error.configure(text=str(err))
            return
        self.destroy()
        self.catalogo.listo()
