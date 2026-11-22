-- Base de datos del inventario
-- el programa la crea solo al abrirlo, pero tambien se puede correr en Workbench

CREATE DATABASE IF NOT EXISTS inventario_db;
USE inventario_db;

CREATE TABLE IF NOT EXISTS productos (
    producto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio DOUBLE NOT NULL,
    cantidad_stock INT NOT NULL,
    proveedor VARCHAR(150),
    stock_minimo INT NOT NULL DEFAULT 5
);

CREATE TABLE IF NOT EXISTS ventas (
    venta_id INT AUTO_INCREMENT PRIMARY KEY,
    cant_articulos INT NOT NULL,
    medio_pago VARCHAR(100) NOT NULL,
    total DOUBLE NOT NULL,
    productos INT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- productos de prueba
INSERT INTO productos (nombre, descripcion, precio, cantidad_stock, proveedor, stock_minimo) VALUES
('Mouse Logitech',      'USB con cable',25,     40, 'Compu Wilson',     10),
('Teclado Logitech',    'Teclado USB',  45,     25, 'Compu Wilson',     8),
('Mouse inalambrico',   'bluetooth',    79,     4,  'Compu Wilson',     5),
('Audifonos JBL',       'bluetooth',    229,    10, 'Mundo Audio',      4),
('Audifonos Sony',      'con cable',    69,     15, 'Mundo Audio',      5),
('Parlante JBL Go',     'bluetooth',    179,    2,  'Mundo Audio',      3),
('Laptop Lenovo',       'i5 16gb ram',  2499,   4,  'Lima Digital',     2),
('Laptop HP',           'i3 8gb ram',   1799,   5,  'Lima Digital',     2),
('Monitor Samsung 24',  'full hd',      549,    6,  'Lima Digital',     2),
('Celular Samsung A15', '128gb',        699,    8,  'Celulandia',       3),
('Celular Xiaomi',      '256gb',        549,    0,  'Celulandia',       3),
('Cargador tipo C',     '20w',          59,     14, 'Celulandia',       5),
('Cable HDMI',          '2 metros',     29,     22, 'Tecno Lima',       6),
('USB Kingston',        '64gb',         29,     35, 'Tecno Lima',       10),
('Tinta Epson',         'color cian',   35,     0,  'Compu Wilson',     6);
