from datetime import datetime

import ttkbootstrap as tb

from producto import ETIQUETAS
from prolog.motor_prolog import revisarStock
from ui.componentes import Tabla, Vista, texto
from ui.config import plural


def cantidadStock(alerta):
    return alerta[0].cantidad_stock


# Pestaña Faltantes: Prolog dice que equipos hay que volver a pedir.
# Solo se revisa cuando le das al boton
class VistaAlertas(Vista):
    def armar(self):
        tb.Button(self, text="Analiza el stock", bootstyle="primary",
                  command=self.revisar).pack(anchor="e", pady=(0, 12))
        self.mensaje = texto(self)
        self.mensaje.configure(padding=(12, 8))
        self.tabla = Tabla(self, [("Equipo", 280, "w"), ("Compañía", 180, "w"), ("Estado", 110, "w"),
                                  ("Quedan", 80, "e"), ("Mínimo", 80, "e")],
                           alto=15, vacio="Dale clic a \"Analiza el stock\".")
        self.tabla.arbol.configure(selectmode="none")  # aqui no se puede elegir filas
        self.tabla.pack(fill="both", expand=True)

    def revisar(self):
        productos = self.app.inventario.productos
        try:
            alertas = revisarStock(productos)
        except FileNotFoundError:
            self.mostrar("No se encontró SWI-Prolog. Instálalo con: winget install SWI-Prolog.SWI-Prolog", "danger")
            self.tabla.cargar([])
            return
        except Exception as err:
            self.mostrar(f"Falló el análisis: {err}", "danger")
            self.tabla.cargar([])
            return

        # primero los que tienen menos stock
        alertas.sort(key=cantidadStock)
        filas = []
        for p, estado in alertas:
            proveedor = p.proveedor
            if proveedor == "":
                proveedor = "-"
            valores = (p.nombre, proveedor, ETIQUETAS[estado], p.cantidad_stock, p.stock_minimo)
            filas.append((p.producto_id, valores, estado))
        self.tabla.cargar(filas)

        hora = datetime.now().strftime("%H:%M")
        if len(alertas) > 0:
            self.mostrar(f"Faltan {plural(len(alertas), 'equipo', 'equipos')}. "
                         f"Revisado a las {hora}.", "warning")
        else:
            self.mostrar(f"Todo bien, no falta nada. Revisado a las {hora}.", "success")

    def mostrar(self, txt, color):
        # la franja de color que sale encima de la tabla
        self.mensaje.configure(text=txt, bootstyle=f"inverse-{color}")
        self.mensaje.pack(fill="x", before=self.tabla, pady=(0, 8))
