import os
import subprocess
import tempfile

rutaSwipl = r"C:\Program Files\swipl\bin\swipl.exe"


def limpiarTexto(texto):
    if not texto:
        return "sinnombre"
    limpio = str(texto).replace("\\", "/").replace("'", "\\'")
    return f"'{limpio}'"


def revisarStock(productos, minimoBase=5):
    dirActual = os.path.dirname(os.path.abspath(__file__))
    archivoReglas = os.path.join(dirActual, "reglas.pl")

    hechos = []
    for prod in productos:
        nom = limpiarTexto(prod.nombre)
        stock = int(prod.cantidad_stock)
        minimo = int(getattr(prod, "stock_minimo", minimoBase))
        hechos.append(f"item({nom}, {stock}, {minimo}).")

    if not hechos:
        return []

    with tempfile.NamedTemporaryFile("w", suffix=".pl", delete=False, encoding="utf-8") as temp:
        temp.write("\n".join(hechos) + "\n")
        rutaTemp = temp.name

    try:
        reglasUrl = archivoReglas.replace("\\", "/")
        tempUrl = rutaTemp.replace("\\", "/")

        consulta = (
            f"consult('{reglasUrl}'), "
            f"consult('{tempUrl}'), "
            "forall(item(N, S, M), ("
            "  estado_stock(N, S, M, E), "
            "  (E = sin_stock ; E = stock_bajo) -> "
            "    format('~w|~w|~w|~w~n', [N, S, M, E]) "
            "  ; true"
            ")), halt."
        )

        res = subprocess.run(
            [rutaSwipl, "-q", "-g", consulta],
            capture_output=True,
            text=True,
            timeout=10
        )

        if res.returncode != 0:
            raise RuntimeError(res.stderr.strip() or "Falló la consulta en Prolog.")

        alertas = []
        for fila in res.stdout.strip().splitlines():
            partes = fila.split("|")
            if len(partes) == 4:
                nom, stock, minimo, estado = partes
                alertas.append((nom, int(stock), int(minimo), estado))

        return alertas
    finally:
        if os.path.exists(rutaTemp):
            os.remove(rutaTemp)