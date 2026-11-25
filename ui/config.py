# Configuracion
import os

import ttkbootstrap as tb

NOMBRE_TIENDA = "TecnoStock"
LEMA = "Stock y ventas"
MONEDA = "S/"
MEDIOS_PAGO = ("Efectivo", "Yape", "Plin", "POS", "Depósito")  # POS es con tarjeta

AZUL = "#1D4ED8"
VERDE = "#15803D"
ROJO = "#B91C1C"
GRIS = "#6B7280"
AMARILLO_FILA = "#FEF3C7"  # poco stock
ROJO_FILA = "#FEE2E2"      # agotado

CARPETA = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(CARPETA, "logo.png")
ICONO = os.path.join(CARPETA, "icono.png")

# tema de colores
tb.Theme(name="tecno", primary=AZUL, success=VERDE, info="#0891B2", warning="#CA8A04",
         danger=ROJO, light=dict(background="#F4F6F9", foreground="#1F2937")).register()


def soles(monto):
    return f"{MONEDA} {monto:,.2f}"  # monto en soles


def fecha(valor):
    if valor is None:
        return "-"
    return valor.strftime("%d/%m/%Y %H:%M")


# singular o plural
def plural(n, uno, varios):
    if n == 1:
        return f"{n} {uno}"
    return f"{n} {varios}"
