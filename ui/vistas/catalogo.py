import tkinter as tk

import ttkbootstrap as tb

from bdd import ErrorBaseDatos
from ui.componentes import FormProducto, Tabla, Vista, texto
from ui.config import plural, soles

# opciones del combo Estado
ESTADOS = {"Todos": None, "Bien": "ok", "Poco stock": "bajo", "Agotados": "agotado"}


# Pestaña Catálogo
class VistaCatalogo(Vista):
    def armar(self):
        filtros = tb.Frame(self)
        filtros.pack(fill="x", pady=(0, 10))
        texto(filtros, "Busca").pack(side="left", padx=(0, 6))
        self.buscar = tk.StringVar()
        entrada = tb.Entry(filtros, textvariable=self.buscar, width=40)
        entrada.pack(side="left")
        entrada.bind("<KeyRelease>", lambda e: self.refrescar())  # busca mientras escribes
        texto(filtros, "Estado").pack(side="left", padx=(18, 6))
        self.estado = tb.Combobox(filtros, values=["Todos", "Bien", "Poco stock", "Agotados"],
                                  state="readonly", width=14)
        self.estado.set("Todos")
        self.estado.bind("<<ComboboxSelected>>", lambda e: self.refrescar())
        self.estado.pack(side="left")
        tb.Button(filtros, text="+ Nuevo equipo", bootstyle="primary", command=self.nuevo).pack(side="right")

        self.tabla = Tabla(self, [("ID", 45, "e"), ("Equipo", 230, "w"), ("Detalle", 190, "w"),
                                  ("Compañía", 130, "w"), ("Estado", 85, "w"), ("Costo", 90, "e"),
                                  ("Stock", 55, "e"), ("Mín.", 45, "e"), ("Total", 100, "e")],
                           alto=15, vacio="No hay nada con esa búsqueda.")
        self.tabla.pack(fill="both", expand=True)

        pie = tb.Frame(self)
        pie.pack(fill="x", pady=(10, 0))
        self.conteo = texto(pie, gris=True)
        self.conteo.pack(side="left")
        tb.Button(pie, text="Elimina", bootstyle="danger-outline", command=self.eliminar).pack(side="right")
        tb.Button(pie, text="Edita", bootstyle="secondary-outline", command=self.editar).pack(side="right", padx=8)

    def refrescar(self):
        lista = self.app.inventario.filtrarProductos(self.buscar.get(), ESTADOS[self.estado.get()])
        filas = []
        for p in lista:
            valores = (p.producto_id, p.nombre, p.descripcion, p.proveedor, p.etiqueta,
                       soles(p.precio), p.cantidad_stock, p.stock_minimo, soles(p.valor_en_stock))
            color = None
            if p.estado != "ok":
                color = p.estado
            filas.append((p.producto_id, valores, color))
        self.tabla.cargar(filas)
        total = len(self.app.inventario.productos)
        self.conteo.configure(text=f"{len(lista)} de {plural(total, 'equipo', 'equipos')}")

    def elegido(self):
        # producto elegido en la tabla
        return self.app.inventario.buscarProducto(self.tabla.elegido())

    def nuevo(self):
        FormProducto(self)

    def editar(self):
        p = self.elegido()
        if not p:
            return
        FormProducto(self, p)

    def eliminar(self):
        p = self.elegido()
        if not p:
            return
        resp = tb.Messagebox.show_question(f"Eliminar \"{p.nombre}\"", "Alerta", parent=self,
                                           buttons=["No:secondary", "Sí, elimínalo:danger"])
        if resp != "Sí, elimínalo":
            return
        try:
            self.app.inventario.borrarProducto(p)
        except ErrorBaseDatos as err:
            tb.Messagebox.show_error(str(err), "Falló la eliminación", parent=self)
            return
        self.listo()

    def listo(self):
        # despues de guardar o eliminar
        self.refrescar()
        self.app.datos_cambiaron()
