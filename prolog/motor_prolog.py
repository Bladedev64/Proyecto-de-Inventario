# Aqui se llama a SWI-Prolog para saber que productos hay que volver a pedir.
# Las reglas estan en reglas.pl, desde Python solo mando los numeros y leo la respuesta
import os
import shutil
import subprocess

# Prolog no acepta la \ de Windows en las rutas, por eso la cambio por /
REGLAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reglas.pl").replace("\\", "/")

# lo que responde Prolog -> el estado que uso en Python
ESTADOS = {"sin_stock": "agotado", "stock_bajo": "bajo"}


def buscarSwipl():
    swipl = shutil.which("swipl")
    if swipl is None:
        swipl = r"C:\Program Files\swipl\bin\swipl.exe"
    if not os.path.exists(swipl):
        raise FileNotFoundError("SWI-Prolog no está instalado en esta PC.")
    return swipl


def revisarStock(productos):
    # devuelve una lista de (producto, estado) con los que faltan
    if len(productos) == 0:
        return []
    swipl = buscarSwipl()

    # a Prolog le paso item(numero, stock, minimo) de cada producto.
    # No le paso los nombres porque las tildes y comillas daban error
    items = []
    for i in range(len(productos)):
        p = productos[i]
        items.append(f"item({i}, {p.cantidad_stock}, {p.stock_minimo})")
    lista = ", ".join(items)
    consulta = f"consult('{REGLAS}'), revisar([{lista}]), halt."

    resultado = subprocess.run([swipl, "-q", "-g", consulta], capture_output=True, text=True, timeout=10)
    if resultado.returncode != 0:
        raise RuntimeError("Prolog falló: " + resultado.stderr)

    # Prolog responde una linea por producto, ej: "3 stock_bajo"
    alertas = []
    for linea in resultado.stdout.splitlines():
        partes = linea.split()
        numero = int(partes[0])
        estado = ESTADOS[partes[1]]
        alertas.append((productos[numero], estado))
    return alertas
