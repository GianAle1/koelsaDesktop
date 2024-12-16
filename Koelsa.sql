CREATE DATABASE koelsa;
go
USE koelsa;
go
-- Tabla usuario
CREATE TABLE usuario (
    idusuario  INT IDENTITY(1,1)PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    contraseña VARCHAR(100) NOT NULL
);
go
select * from usuario
-- Tabla marca
CREATE TABLE marca (
    idmarca INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);
go
-- Tabla proveedor
CREATE TABLE proveedor (
    idproveedor INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(199),
    telefono VARCHAR(20),
    correo VARCHAR(100)
);
go
-- Tabla almacen
CREATE TABLE almacen (
    idalmacen INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    capacidad INT
);
go
-- Tabla producto
CREATE TABLE producto (
    idproducto INT IDENTITY(1,1) PRIMARY KEY,
    partname VARCHAR(100),
    descripcion VARCHAR(100),
    idmarca INT,
    undMedida VARCHAR(100),
    cantidad INT,
    idproveedor INT,
    idalmacen INT,
    uso VARCHAR(50),
    equipo VARCHAR(50),
    precio DECIMAL(10, 2),
    FOREIGN KEY (idmarca) REFERENCES marca(idmarca) ON DELETE SET NULL,
    FOREIGN KEY (idproveedor) REFERENCES proveedor(idproveedor) ON DELETE SET NULL,
    FOREIGN KEY (idalmacen) REFERENCES almacen(idalmacen) ON DELETE SET NULL
);
go
-- Consulta para obtener detalles de los productos
SELECT 
    p.idproducto,
    p.partname,
    p.descripcion,
    m.nombre AS marca,
    pr.nombre AS proveedor,
    a.nombre AS almacen,
    p.undMedida,
    p.cantidad
FROM producto p
JOIN marca m ON p.idmarca = m.idmarca
JOIN proveedor pr ON p.idproveedor = pr.idproveedor
JOIN almacen a ON p.idalmacen = a.idalmacen;
go
-- Tabla solicitador
CREATE TABLE solicitador (
    idsolicitador INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);
go
-- Tabla supervisor
CREATE TABLE supervisor (
    idsupervisor INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);
go
-- Tabla entrada
CREATE TABLE entrada (
    identrada INT IDENTITY(1,1) PRIMARY KEY,
    fecha DATE
);
go
-- Tabla entradaDetalle
CREATE TABLE entradaDetalle (
    identradaDetalle INT IDENTITY(1,1) PRIMARY KEY,
    idientrada INT,
    idproducto INT,
    cantidad INT,
    FOREIGN KEY (idientrada) REFERENCES entrada(identrada),
    FOREIGN KEY (idproducto) REFERENCES producto(idproducto)
);
go
-- Tabla maquinariaMarca
CREATE TABLE maquinariaMarca (
    idmaquinariaMarca INT IDENTITY(1,1) PRIMARY KEY,
    tipo VARCHAR(50),
    nombre VARCHAR(40)
);
go
CREATE TABLE maquinaria (
    idmaquinaria INT IDENTITY(1,1) PRIMARY KEY,
    idmaquinariaMarca int,
    idmarca INT,
    descripcion VARCHAR(50),
    FOREIGN KEY (idmaquinariaMarca) REFERENCES maquinariaMarca(idmaquinariaMarca)
);
go
CREATE TABLE salida (
    idsalida INT IDENTITY(1,1) PRIMARY KEY,
    idmaquinaria INT,
    fecha DATE,
    responsable VARCHAR(50),
    FOREIGN KEY (idmaquinaria) REFERENCES maquinaria(idmaquinaria)
);
go
CREATE TABLE salidaDetalle (
    idisalidaDetalle INT IDENTITY(1,1) PRIMARY KEY,
    idsalida INT,
    idproducto INT,
    cantidad INT,
	FOREIGN KEY (idsalida) REFERENCES salida(idsalida),
    FOREIGN KEY (idproducto) REFERENCES producto(idproducto)
);
go
-- Tabla Requerimiento
CREATE TABLE Requerimiento (
    idrequerimiento INT IDENTITY(1,1) PRIMARY KEY,
    fechaRequerimiento DATE,
    total DECIMAL(10, 2),
    critero VARCHAR(50),
    idsolicitador INT,
    idsupervisor INT,
    FOREIGN KEY (idsolicitador) REFERENCES solicitador(idsolicitador),
    FOREIGN KEY (idsupervisor) REFERENCES supervisor(idsupervisor)
);
go
-- Tabla requerimientoDetalle
CREATE TABLE requerimientoDetalle (
    idrequerimientoDetalle INT IDENTITY(1,1) PRIMARY KEY,
    idrequerimiento INT,
    idproducto INT,
    cantidad INT,
    idproveedor INT,
    precioUnitario DECIMAL(10, 2),
    FOREIGN KEY (idproducto) REFERENCES producto(idproducto),
    FOREIGN KEY (idproveedor) REFERENCES proveedor(idproveedor),
    FOREIGN KEY (idrequerimiento) REFERENCES Requerimiento(idrequerimiento)
);
go
-- Insertar usuarios
INSERT INTO usuario (nombre, apellidos, correo, contraseña) VALUES
('Gian', 'Alejandro', 'gian.alejandro@koelsa.com', '123');
-- Insertar marcas
INSERT INTO marca (nombre) VALUES
('Caterpillar'),
('Komatsu'),
('XCMG'),
('SANY'),
('John Deere');
go
-- Insertar proveedores
INSERT INTO proveedor (nombre, direccion, telefono, correo) VALUES
('NRC PACK', 'Calle Falsa 123', '555-1234', 'proveedorA@email.com'),
('L&L INDUSTRIAL', 'Avenida Real 456', '555-5678', 'proveedorB@email.com'),
('COLOR Y MATIZ LOPEZ', 'Calle 14 789', '555-9101', 'proveedorC@email.com'),
('A&C DYNAMIS', 'Paseo Central 101', '555-1122', 'proveedorD@email.com');

-- Insertar almacenes
INSERT INTO almacen (nombre, direccion, capacidad) VALUES
('Almacen 1', 'Kilometro 26 Ant. Pan. Sur', 500);

-- Insertar productos
INSERT INTO producto (partname, descripcion, idmarca, undMedida, cantidad, idproveedor, idalmacen, uso, equipo, precio) VALUES
('20SF1.70', 'STRETCH FILM 20'' x 2 KG', 1, 'UND', 100, 1, 1, 'CONSUMIBLES', '-', 3.98),
('446', 'LOCTITE COD 620 X 50 ML', 2, 'UND', 200, 2, 1, 'CONSUMIBLES', 'EQUIPOS', 13.26),
('S/N', 'PQTE ,LIJA AL AGUA 180', 3, 'UND', 150, 3, 1, 'CONSUMIBLES', 'EQUIPOS', 12.20),
('S/N', 'Paño Industrial Suelto Color', 4, 'KG', 250, 4, 1, 'CONSUMIBLES', 'LIMPIEZA', 12.30);
go
-- Insertar entrada
INSERT INTO entrada (fecha) VALUES
('2024-01-01'),
('2024-02-01'),
('2024-03-01'),
('2024-04-01'),
('2024-05-01');

-- Insertar entradaDetalle
INSERT INTO entradaDetalle (idientrada, idproducto, cantidad) VALUES
(1, 1, 10),
(2, 2, 20),
(3, 3, 15),
(4, 4, 25);
go
-- Insertar maquinaria
INSERT INTO maquinaria (idmarca, descripcion) VALUES
(1, 'Excavadora'),
(2, 'Retroexcavadora'),
(3, 'Volquete');
go
-- Insertar maquinariaMarca
INSERT INTO maquinariaMarca (tipo, nombre) VALUES
('Tipo A', 'Caterpillar'),
('Tipo B', 'Komatsu'),
('Tipo C', 'XCMG'),
('Tipo D', 'SANY');
go
INSERT INTO solicitador (nombre) VALUES
('Diego'),
('Carlos'),
('Luis');
go
INSERT INTO supervisor (nombre) VALUES
('Henrry');
go
-- Insertar requerimiento
INSERT INTO Requerimiento (fechaRequerimiento, total, critero, idsolicitador, idsupervisor) VALUES
('2024-01-01', 1000.50, 'Urgente', 1, 1),
('2024-02-01', 2500.75, 'Normal', 2, 1),
('2024-03-01', 3000.00, 'Urgente', 3, 1),
('2024-04-01', 500.25, 'Normal', 1, 1),
('2024-05-01', 1200.60, 'Urgente', 1, 1);
go
-- Insertar requerimientoDetalle
INSERT INTO requerimientoDetalle (idrequerimiento, idproducto, cantidad, idproveedor, precioUnitario) VALUES
(1,1, 10, 1, 25.50),
(1,2, 20, 2, 30.75),
(2,3, 15, 3, 45.00),
(3,4, 15, 3, 45.00),
(4,4, 25, 4, 12.30);
go
-- Seleccionar todos los productos con información de marca, proveedor y almacén (JOIN)
SELECT 
    ed.identradaDetalle,
    ed.idientrada,
    e.fecha AS fecha_entrada,
    ed.idproducto,
    p.partname,
    ed.cantidad
FROM entradaDetalle ed
JOIN entrada e ON ed.idientrada = e.identrada
JOIN producto p ON ed.idproducto = p.idproducto;
go
-- Seleccionar todas las maquinarias con sus marcas (JOIN)
SELECT 
    m.idmaquinaria,
    m.descripcion AS maquinaria,
    ma.nombre AS marca
FROM maquinaria m
JOIN marca ma ON m.idmarca = ma.idmarca;
go
-- Seleccionar todos los requerimientos (con JOIN para solicitador y supervisor)
SELECT 
    r.idrequerimiento,
    r.fechaRequerimiento,
    r.total,
    r.critero,
    s.nombre AS solicitador,
    su.nombre AS supervisor
FROM Requerimiento r
JOIN solicitador s ON r.idsolicitador = s.idsolicitador
JOIN supervisor su ON r.idsupervisor = su.idsupervisor;
go
select * from  requerimientoDetalle;
-- Seleccionar todos los detalles de requerimientos (con JOIN para producto y proveedor)
go
SELECT
    rd.idrequerimientoDetalle,
    rd.idrequerimiento,
    r.fechaRequerimiento,
    p.partname,
    p.descripcion AS producto,
    rd.cantidad,
    pr.nombre AS proveedor,
    rd.precioUnitario
FROM requerimientoDetalle rd
JOIN Requerimiento r ON rd.idrequerimiento = r.idrequerimiento
JOIN producto p ON rd.idproducto = p.idproducto
JOIN proveedor pr ON rd.idproveedor = pr.idproveedor;
go

select * from producto
select * from usuario
DELETE FROM marca 
    WHERE idmarca >= 100 
select * from usuario
DBCC CHECKIDENT ('marca', RESEED, 5);
