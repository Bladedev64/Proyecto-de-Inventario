import tkinter as tk

import ttkbootstrap as tb

from bdd import ErrorBaseDatos
from ui.componentes import Tabla, Vista, texto
from ui.config import MEDIOS_PAGO, ROJO, fecha, plural, soles


# Pestaña Ventas: a la izquierda se arma la venta y a la derecha el historial
class VistaVentas(Vista):
    def armar(self):
        self.carrito = {}   # producto_id: cantidad
        self.opciones = {}  # texto del combo: producto_id

        # izquierda: la venta nueva
        caja = tb.Labelframe(self, text="Nueva venta", padding=14, width=380)
        caja.pack(side="left", fill="y", padx=(0, 14))
        caja.pack_propagate(False)
        texto(caja, "Equipo", gris=True).pack(anchor="w")
        self.equipo = tb.Combobox(caja, state="readonly")
        self.equipo.pack(fill="x", pady=(2, 8))
        fila = tb.Frame(caja)
        fila.pack(fill="x")
        texto(fila, "Cantidad", gris=True).pack(side="left")
        self.cantidad = tk.StringVar(value="1")
        tb.Spinbox(fila, from_=1, to=999, textvariable=self.cantidad, width=6).pack(side="left", padx=8)
        tb.Button(fila, text="Añade", bootstyle="secondary", command=self.agregar).pack(side="right")

        # esto lo pongo antes que la tabla para que la tabla no tape los botones
        self.btn_cobrar = tb.Button(caja, text="Completa la venta", bootstyle="primary", command=self.cobrar)
        self.btn_cobrar.pack(side="bottom", fill="x", ipady=4)
        self.error = texto(caja)
        self.error.configure(foreground=ROJO, wraplength=340)
        self.error.pack(side="bottom", anchor="w")
        abajo = tb.Frame(caja)
        abajo.pack(side="bottom", fill="x", pady=10)
        texto(abajo, "Paga con", gris=True).pack(side="left")
        self.pago = tb.Combobox(abajo, values=MEDIOS_PAGO, state="readonly", width=12)
        self.pago.set(MEDIOS_PAGO[0])
        self.pago.pack(side="left", padx=8)
        self.total = texto(abajo, soles(0), tam=16, negrita=True)
        self.total.pack(side="right")
        tb.Button(caja, text="Quita el elegido", bootstyle="link", command=self.quitar).pack(side="bottom", anchor="w")

        self.tabla = Tabla(caja, [("Equipo", 160, "w"), ("Cant.", 50, "e"), ("Subtotal", 90, "e")],
                           alto=4, vacio="Aún no hay nada")
        self.tabla.pack(fill="both", expand=True, pady=(12, 0))

        # derecha: todas las ventas
        caja = tb.Labelframe(self, text="Todas las ventas", padding=14)
        caja.pack(side="left", fill="both", expand=True)
        self.historial = Tabla(caja, [("#", 60, "w"), ("Fecha", 140, "w"), ("Unid.", 60, "e"),
                                      ("Equipos", 80, "e"), ("Pago", 110, "w"), ("Total", 110, "e")],
                               alto=14, vacio="Aún no hay ventas.")
        self.historial.pack(fill="both", expand=True)
        self.resumen = texto(caja, gris=True)
        self.resumen.pack(anchor="w", pady=(8, 0))

    def refrescar(self):
        # en el combo solo salen los equipos que tienen stock
        self.opciones = {}
        nombres = []
        for p in self.app.inventario.productos:
            if p.cantidad_stock > 0:
                nombre = f"{p.nombre} ({p.cantidad_stock} disp.)"
                self.opciones[nombre] = p.producto_id
                nombres.append(nombre)
        self.equipo.configure(values=nombres)
        self.pintar_carrito()

        # historial, la venta mas nueva arriba
        ventas = self.app.ventas.ventas
        filas = []
        for v in reversed(ventas):
            valores = (f"#{v.venta_id}", fecha(v.fecha), v.cant_articulos, v.productos,
                       v.medio_pago, soles(v.total))
            filas.append((v.venta_id, valores, None))
        self.historial.cargar(filas)
        if ventas:
            self.resumen.configure(text=f"{plural(len(ventas), 'venta', 'ventas')}, en total "
                                        f"{soles(self.app.ventas.ingresos())}")
        else:
            self.resumen.configure(text="")

    def lineas(self):
        # devuelve el carrito como lista de (Producto, cantidad)
        # si un equipo ya no existe no lo pongo
        lineas = []
        for pid, cant in self.carrito.items():
            p = self.app.inventario.buscarProducto(pid)
            if p:
                lineas.append((p, cant))
        return lineas

    def pintar_carrito(self):
        lineas = self.lineas()
        filas = []
        total = 0
        for p, cant in lineas:
            filas.append((p.producto_id, (p.nombre, cant, soles(p.precio * cant)), None))
            total += p.precio * cant
        self.tabla.cargar(filas)
        self.total.configure(text=soles(total))
        if lineas:
            self.btn_cobrar.configure(state="normal")
        else:
            self.btn_cobrar.configure(state="disabled")

    def agregar(self):
        pid = self.opciones.get(self.equipo.get())
        if pid is None:
            return  # no eligio equipo
        cant = 0
        if self.cantidad.get().isdigit():
            cant = int(self.cantidad.get())
        p = self.app.inventario.buscarProducto(pid)
        ya_hay = self.carrito.get(pid, 0)  # por si ya estaba en el carrito
        if cant <= 0:
            self.error.configure(text="La cantidad mínima es 1.")
        elif ya_hay + cant > p.cantidad_stock:
            self.error.configure(text=f"Solo quedan {p.cantidad_stock} de \"{p.nombre}\".")
        else:
            self.carrito[pid] = ya_hay + cant
            self.cantidad.set("1")
            self.equipo.set("")
            self.error.configure(text="")
            self.pintar_carrito()

    def quitar(self):
        pid = self.tabla.elegido()
        if pid in self.carrito:
            del self.carrito[pid]
        self.pintar_carrito()

    def cobrar(self):
        try:
            self.app.ventas.registrarVenta(self.lineas(), self.pago.get())
        except (ValueError, ErrorBaseDatos) as err:
            self.error.configure(text=str(err))
            self.refrescar()
            return
        self.carrito.clear()
        self.error.configure(text="")
        self.refrescar()
        self.app.datos_cambiaron()
