# llama a Prolog para ver que productos faltan
import os
import shutil
import subprocess

# Prolog usa / en las rutas
REGLAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reglas.pl").replace("\\", "/")

# estados de Prolog a Python
ESTADOS = {"sin_stock": "agotado", "stock_bajo": "bajo"}


def buscarSwipl():
    swipl = shutil.which("swipl")
    if swipl is None:
        swipl = r"C:\Program Files\swipl\bin\swipl.exe"
    if not os.path.exists(swipl):
        raise FileNotFoundError("SWI-Prolog no está instalado en esta PC.")
    return swipl


def revisarStock(productos):
    # devuelve los productos que faltan
    if len(productos) == 0:
        return []
    swipl = buscarSwipl()

    # no mando los nombres por las tildes
    items = []
    for i in range(len(productos)):
        p = productos[i]
        items.append(f"item({i}, {p.cantidad_stock}, {p.stock_minimo})")
    lista = ", ".join(items)
    consulta = f"consult('{REGLAS}'), revisar([{lista}]), halt."

    resultado = subprocess.run([swipl, "-q", "-g", consulta], capture_output=True, text=True, timeout=10)
    if resultado.returncode != 0:
        raise RuntimeError("Prolog falló: " + resultado.stderr)

    # Prolog responde una linea por producto
    alertas = []
    for linea in resultado.stdout.splitlines():
        partes = linea.split()
        numero = int(partes[0])
        estado = ESTADOS[partes[1]]
        alertas.append((productos[numero], estado))
    return alertas
