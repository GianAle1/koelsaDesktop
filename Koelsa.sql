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
CREATE TABLE UnidadMedida (
    idunidadMedida INT IDENTITY(1,1) PRIMARY KEY,
    nomUnidad VARCHAR(15)
);
go
CREATE TABLE equipo (
    idequipo INT IDENTITY(1,1) PRIMARY KEY,
    nomEquipo VARCHAR(15)
);
go
CREATE TABLE uso (
    iduso INT IDENTITY(1,1) PRIMARY KEY,
    nomUso VARCHAR(15)
);
go
-- Tabla producto
CREATE TABLE producto (
    idproducto INT IDENTITY(1,1) PRIMARY KEY,
    partname VARCHAR(100),
    descripcion VARCHAR(100),
    idmarca INT,
    idunidadMedida int,
    cantidad INT,
    idproveedor INT,
    idalmacen INT,
    iduso int,
    idequipo int,
    precio DECIMAL(10, 2),
    FOREIGN KEY (idmarca) REFERENCES marca(idmarca) ON DELETE SET NULL,
    FOREIGN KEY (idproveedor) REFERENCES proveedor(idproveedor) ON DELETE SET NULL,
    FOREIGN KEY (idalmacen) REFERENCES almacen(idalmacen) ON DELETE SET NULL,
	FOREIGN KEY (idUnidadMedida) REFERENCES UnidadMedida(idUnidadMedida) ON DELETE SET NULL,
    FOREIGN KEY (idUso) REFERENCES Uso(idUso) ON DELETE SET NULL,                 
    FOREIGN KEY (idEquipo) REFERENCES Equipo(idEquipo) ON DELETE SET NULL  
);
go

select * from UnidadMedida

select * from producto
-- Consulta para obtener detalles de los productos
SELECT 
    p.idproducto,
    p.partname,
    p.descripcion,
    m.nombre AS marca,            -- Esta tabla debe existir
    pr.nombre AS proveedor,       -- Esta tabla debe existir
    a.nombre AS almacen,
    u.nomUnidad AS UndMedida,
    p.cantidad
FROM producto p
-- Se debe asegurar que las tablas marca y proveedor existan
LEFT JOIN marca m ON p.idmarca = m.idmarca  -- O INNER JOIN si la tabla existe
LEFT JOIN proveedor pr ON p.idproveedor = pr.idproveedor -- O INNER JOIN si la tabla existe
INNER JOIN UnidadMedida u ON p.idunidadMedida = u.idunidadMedida
INNER JOIN almacen a ON p.idalmacen = a.idalmacen;

go

select * from salidaDetalle
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
select*from entrada;
go
-- Tabla entradaDetalle
CREATE TABLE entradaDetalle (
    identradaDetalle INT IDENTITY(1,1) PRIMARY KEY,
    identrada INT,
    idproducto INT,
    cantidad INT,
    FOREIGN KEY (identrada) REFERENCES entrada(identrada),
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
    idsalidaDetalle INT IDENTITY(1,1) PRIMARY KEY,
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

go

INSERT INTO UnidadMedida (nomUnidad) VALUES ('Kilogramo');
INSERT INTO UnidadMedida (nomUnidad) VALUES ('Metro');
INSERT INTO UnidadMedida (nomUnidad) VALUES ('Cilindro');
INSERT INTO UnidadMedida (nomUnidad) VALUES ('Und');

INSERT INTO equipo (nomEquipo) VALUES ('Equipos');
INSERT INTO equipo (nomEquipo) VALUES ('Personal');
INSERT INTO equipo (nomEquipo) VALUES ('Oficina');
INSERT INTO equipo (nomEquipo) VALUES ('Excavadora');
INSERT INTO equipo (nomEquipo) VALUES ('Limpieza');
INSERT INTO uso (nomUso) VALUES ('Consumible');
INSERT INTO uso (nomUso) VALUES ('Comercial');
INSERT INTO uso (nomUso) VALUES ('Doméstico');

-- Insertar productos
INSERT INTO producto (partname, descripcion, idmarca, idUnidadMedida, cantidad, idproveedor, idalmacen, iduso, idequipo, precio) 
VALUES
('20SF1.70', 'STRETCH FILM 20'' x 2 KG', 1, 4, 100, 1, 1, 1, NULL, 3.98),
('446', 'LOCTITE COD 620 X 50 ML', 2, 4, 200, 2, 1, 1, 1, 13.26),
('S/N', 'PQTE ,LIJA AL AGUA 180', 3, 4, 150, 3, 1, 1, 1, 12.20),
('S/N', 'Paño Industrial Suelto Color', 4, 1, 250, 4, 1, 1, NULL, 12.30);
go
-- Insertar entrada
INSERT INTO entrada (fecha) VALUES
('2024-01-01'),
('2024-02-01'),
('2024-03-01'),
('2024-04-01'),
('2024-05-01');
select * from entrada
-- Insertar entradaDetalle
INSERT INTO entradaDetalle (identrada, idproducto, cantidad) VALUES
(1, 1, 10),
(2, 2, 20),
(3, 3, 15),
(4, 4, 25),
(5, 1, 15);
go
-- Insertar entrada
INSERT INTO salida (fecha) VALUES
('2024-01-01'),
('2024-02-01'),
('2024-03-01'),
('2024-04-01'),
('2024-05-01');
select * from salidaDetalle
-- Insertar entradaDetalle
INSERT INTO salidaDetalle(idsalida, idproducto, cantidad) VALUES
(1, 1, 10),
(2, 2, 20),
(3, 3, 15),
(4, 4, 25),
(5, 1, 15);
go
select * from entradaDetalle
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
select * from Requerimiento
select * from requerimientoDetalle
select * from producto
-- Insertar requerimientoDetalle
INSERT INTO requerimientoDetalle (idrequerimiento, idproducto, cantidad, idproveedor, precioUnitario) VALUES
(1,2, 10, 1, 25.50),
(1,3, 20, 2, 30.75),
(2,4, 15, 3, 45.00),
(3,1, 15, 3, 45.00),
(4,1, 25, 4, 12.30);
go

select * from producto
-- Seleccionar todos los productos con información de marca, proveedor y almacén (JOIN)
SELECT 
	p.idproducto as CodProducto,
    e.fecha AS fecha_entrada,
    p.descripcion,
    p.partname,
    ed.cantidad as CantidadEntrada
FROM entradaDetalle ed
JOIN entrada e ON ed.identrada = e.identrada
JOIN producto p ON ed.idproducto = p.idproducto
where p.idproducto=1
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
