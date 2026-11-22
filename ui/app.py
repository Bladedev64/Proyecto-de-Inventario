import tkinter as tk

import ttkbootstrap as tb

from bdd import BaseDatos, ErrorBaseDatos
from inventario import Inventario
from ui.componentes import texto
from ui.config import ICONO, LEMA, LOGO, NOMBRE_TIENDA
from ui.vistas.alertas import VistaAlertas
from ui.vistas.catalogo import VistaCatalogo
from ui.vistas.panel import VistaPanel
from ui.vistas.ventas import VistaVentas
from ventas import Ventas

# las pestañas: (clave, titulo, clase)
SECCIONES = [
    ("panel", "Inicio", VistaPanel),
    ("catalogo", "Catálogo", VistaCatalogo),
    ("ventas", "Ventas", VistaVentas),
    ("alertas", "Faltantes", VistaAlertas),
]


# Clase App: la ventana principal
class App:
    def __init__(self, root):
        self.root = root
        self.db = None
        self.vistas = {}
        root.title(f"{NOMBRE_TIENDA} - {LEMA}")
        root.minsize(1120, 660)
        root.iconphoto(True, tk.PhotoImage(file=ICONO))
        root.protocol("WM_DELETE_WINDOW", self.cerrar)
        root.style.configure("Treeview", rowheight=30)
        root.style.configure("Treeview.Heading", font="-size 10 -weight bold")
        root.style.configure("TNotebook.Tab", padding=(18, 8), font="-size 10")

        # banda de arriba: logo y nombre
        banda = tb.Frame(root, bootstyle="primary", padding=(24, 12))
        banda.pack(fill="x")
        self.logo = tk.PhotoImage(file=LOGO)  # hay que guardarla en self, si no tk la borra
        tb.Label(banda, image=self.logo, text=f"  {NOMBRE_TIENDA}", compound="left",
                 font="-size 15 -weight bold", bootstyle="inverse-primary").pack(side="left")
        tb.Label(banda, text=f"   {LEMA}", bootstyle="inverse-primary").pack(side="left")

        self.cuerpo = tb.Frame(root, padding=(24, 16))
        self.cuerpo.pack(fill="both", expand=True)
        self.conectar()

    def conectar(self):
        # borro lo que haya en la ventana, por si viene del boton "Intenta de nuevo"
        for hijo in self.cuerpo.winfo_children():
            hijo.destroy()
        try:
            self.db = BaseDatos()
            self.inventario = Inventario(self.db)
            self.ventas = Ventas(self.db, self.inventario)
        except ErrorBaseDatos:
            self.sin_conexion()
            return

        self.pestanas = tb.Notebook(self.cuerpo)
        self.pestanas.pack(fill="both", expand=True)
        for clave, titulo, clase in SECCIONES:
            self.vistas[clave] = clase(self.pestanas, self)
            self.pestanas.add(self.vistas[clave], text=titulo)
        self.pestanas.bind("<<NotebookTabChanged>>", lambda e: self.vista_actual().refrescar())
        self.vista_actual().refrescar()
        self.datos_cambiaron()

    def sin_conexion(self):
        caja = tb.Frame(self.cuerpo)
        caja.place(relx=0.5, rely=0.4, anchor="center")
        texto(caja, "No hay conexión", tam=14, negrita=True).pack(pady=(0, 18))
        tb.Button(caja, text="Intenta de nuevo", bootstyle="primary", command=self.conectar).pack()

    def vista_actual(self):
        numero = self.pestanas.index("current")
        clave = SECCIONES[numero][0]
        return self.vistas[clave]

    def datos_cambiaron(self):
        # en la pestaña Faltantes pongo cuantos hay, ej: "Faltantes (3)"
        faltan = self.inventario.resumen()["faltan"]
        if faltan > 0:
            self.pestanas.tab(self.vistas["alertas"], text=f"Faltantes ({faltan})")
        else:
            self.pestanas.tab(self.vistas["alertas"], text="Faltantes")

    def cerrar(self):
        if self.db:
            self.db.cerrar()
        self.root.destroy()


def iniciar():
    root = tb.Window(theme="tecno-light", size=(1280, 780))
    root.place_window_center()
    App(root)
    root.mainloop()
