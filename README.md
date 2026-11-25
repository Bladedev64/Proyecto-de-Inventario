# TecnoStock

Programa para llevar el inventario y las ventas de una tienda de tecnología.
Está hecho en Python con Tkinter y ttkbootstrap, los datos se guardan en MySQL y
la parte de los productos que faltan la decide Prolog.

## Qué necesitas

- Python 3.10 o más
- XAMPP con MySQL prendido
- SWI-Prolog para la pestaña Faltantes. Si no lo tienes instálalo en la terminal de PowerShell con:
  winget install SWI-Prolog.SWI-Prolog

## Cómo abrirlo

Primero crea la base de datos (mira la parte de Base de datos más abajo).

En la terminal ejecutar: 
1. pip install -U mysql-connector-python ttkbootstrap
2. python main.py

Para entrar a MySQL usa el usuario root con clave root, y si no puede entra sin clave
(así viene XAMPP). Si la clave es otra cámbiala arriba en `bdd.py`.

## Base de datos

Antes de abrir el programa hay que crear la base de datos:

1. Abre XAMPP y dale Start a MySQL y a Apache
2. Entra a http://localhost/phpmyadmin y ve a la pestaña SQL
3. Copia todo el código de `base_datos.sql`, pégalo y dale Continuar

Ojo: si ya tenías la base `inventario_db`, esto la borra y la crea de nuevo con los
productos de prueba.


## Archivos

- `main.py`: abre el programa
- `bdd.py`: todo lo de MySQL
- `producto.py` y `venta.py`: las clases Producto y Venta
- `inventario.py`: la lista de productos, la búsqueda y el resumen
- `ventas.py`: guarda las ventas
- `prolog/`: las reglas en Prolog y el código que llama a swipl
- `ui/`: las ventanas, una pestaña por archivo en `ui/vistas`

Cada producto tiene un stock mínimo. Si le quedan esas unidades o menos sale en
amarillo, y si llega a 0 sale en rojo.
