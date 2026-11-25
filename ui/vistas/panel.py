import ttkbootstrap as tb

from ui.componentes import Tabla, Vista, texto
from ui.config import ROJO, VERDE, soles

# cuadros de arriba
CUADROS = [("equipos", "Equipos distintos"), ("unidades", "Unidades en almacén"),
           ("valor", "Plata en el almacén"), ("faltan", "Faltantes"), ("vendido", "Total en ventas")]


# Pestaña Inicio
class VistaPanel(Vista):
    def armar(self):
        cols = tb.Frame(self)
        cols.pack(fill="both", expand=True)
        cols.columnconfigure((0, 1, 2), weight=1, uniform="col")
        cols.rowconfigure(1, weight=1)

        # fila de cuadros
        fila = tb.Frame(cols)
        fila.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 14))
        self.cuadros = {}
        for i, (clave, titulo) in enumerate(CUADROS):
            fila.columnconfigure(i, weight=1, uniform="cuadro")
            caja = tb.Labelframe(fila, text=titulo, padding=(14, 6, 14, 10))
            if i == 0:
                caja.grid(row=0, column=i, sticky="nsew")
            else:
                caja.grid(row=0, column=i, sticky="nsew", padx=(10, 0))
            numero = texto(caja, "-", tam=17, negrita=True)
            numero.pack(anchor="w")
            self.cuadros[clave] = numero

        caja = tb.Labelframe(cols, text="Cómo está el stock", padding=14)
        caja.grid(row=1, column=0, sticky="nsew")
        self.medidor = tb.Meter(caja, meter_size=170, meter_thickness=12, amount_total=1,
                                subtext="con buen stock", bootstyle="success")
        self.medidor.pack()
        self.leyenda = texto(caja)
        self.leyenda.configure(justify="center")
        self.leyenda.pack(pady=(10, 0))

        caja = tb.Labelframe(cols, text="Lo que falta", padding=10)
        caja.grid(row=1, column=1, sticky="nsew", padx=14)
        self.faltan = Tabla(caja, [("Equipo", 200, "w"), ("Quedan", 70, "e")], vacio="No falta nada.")
        self.faltan.pack(fill="both", expand=True)

        caja = tb.Labelframe(cols, text="Últimas ventas", padding=10)
        caja.grid(row=1, column=2, sticky="nsew")
        self.ultimas = Tabla(caja, [("#", 60, "w"), ("Pago", 110, "w"), ("Total", 110, "e")],
                             vacio="Aún no hay ventas, paciencia.")
        self.ultimas.pack(fill="both", expand=True)

    def refrescar(self):
        r = self.app.inventario.resumen()
        ventas = self.app.ventas

        self.cuadro("equipos", r["productos"])
        self.cuadro("unidades", r["unidades"])
        self.cuadro("valor", soles(r["valor"]))
        if r["faltan"] == 0:
            self.cuadro("faltan", 0, VERDE)
        else:
            # rojo si hay agotados, si no amarillo
            color = "#A16207"
            if r["agotados"] > 0:
                color = ROJO
            self.cuadro("faltan", r["faltan"], color)
        self.cuadro("vendido", soles(ventas.ingresos()))

        bien = r["productos"] - r["faltan"]
        total = r["productos"]
        if total == 0:
            total = 1  # el medidor no acepta 0
        self.medidor.configure(amount_total=total, amount_used=bien)
        self.leyenda.configure(text=f"{bien} bien, {r['bajos']} con poco stock, {r['agotados']} agotados")

        # los que faltan, ordenados por stock
        faltan = []
        for p in self.app.inventario.productos:
            if p.estado != "ok":
                faltan.append(p)
        faltan.sort(key=lambda p: p.cantidad_stock)
        filas = []
        for p in faltan:
            filas.append((p.producto_id, (p.nombre, p.cantidad_stock), p.estado))
        self.faltan.cargar(filas)

        # las ultimas 8 ventas, la mas nueva arriba
        ultimas = ventas.ventas[-8:]
        ultimas.reverse()
        filas = []
        for v in ultimas:
            filas.append((v.venta_id, (f"#{v.venta_id}", v.medio_pago, soles(v.total)), None))
        self.ultimas.cargar(filas)

    def cuadro(self, clave, valor, color=""):
        self.cuadros[clave].configure(text=valor, foreground=color)
