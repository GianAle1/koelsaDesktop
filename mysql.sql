CREATE DATABASE koelsa;
USE koelsa;
CREATE TABLE usuario (
    idusuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    contraseña VARCHAR(100) NOT NULL
);
CREATE TABLE proveedor (
    idproveedor INT AUTO_INCREMENT PRIMARY KEY,
    ruc  VARCHAR(11) ,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(199),
    telefono VARCHAR(20),
    correo VARCHAR(100)
);
CREATE TABLE almacen (
    idalmacen INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    capacidad INT
);
CREATE TABLE almacenDetalle (
    idalmacenDetalle INT AUTO_INCREMENT PRIMARY KEY,
    idalmacen int,
	ubicacion VARCHAR(100) NOT NULL,
    CONSTRAINT fk_almacen FOREIGN KEY (idalmacen) REFERENCES almacen(idalmacen) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE UnidadMedida (
    idunidadMedida INT AUTO_INCREMENT PRIMARY KEY,
    nomUnidad VARCHAR(15)
);
CREATE TABLE uso (
    iduso INT AUTO_INCREMENT PRIMARY KEY,
    nomUso VARCHAR(15)
);
CREATE TABLE marca (
    idmarca INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45)
);
CREATE TABLE familia (
    idfamilia INT AUTO_INCREMENT PRIMARY KEY,
    nomfamilia VARCHAR(45)
);
CREATE TABLE producto (
    idproducto INT AUTO_INCREMENT PRIMARY KEY,
    partname VARCHAR(100),
    descripcion VARCHAR(100),
    idmarca INT,
    idunidadMedida INT,
    cantidad INT,
    idproveedor INT,
    precio DECIMAL(10, 2),
    idsmscs INT,
    idfamilia INT,
    idalmacenDetalle INT,
    FOREIGN KEY (idmarca) REFERENCES marca(idmarca) ON DELETE SET NULL,
    FOREIGN KEY (idunidadMedida) REFERENCES unidadMedida(idunidadMedida) ON DELETE SET NULL,
    FOREIGN KEY (idproveedor) REFERENCES proveedor(idproveedor) ON DELETE SET NULL,
    FOREIGN KEY (idfamilia) REFERENCES familia(idfamilia) ON DELETE SET NULL,
    FOREIGN KEY (idalmacenDetalle) REFERENCES almacenDetalle(idalmacenDetalle) ON DELETE SET NULL
);
CREATE TABLE solicitador (
    idsolicitador INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);
CREATE TABLE supervisor (
    idsupervisor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);
CREATE TABLE entrada (
    identrada INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE
);
CREATE TABLE entradaDetalle (
    identradaDetalle INT AUTO_INCREMENT PRIMARY KEY,
    identrada INT,
    idproducto INT,
    cantidad INT,
    FOREIGN KEY (identrada) REFERENCES entrada(identrada),
    FOREIGN KEY (idproducto) REFERENCES producto(idproducto)
);
CREATE TABLE maquinaria (
    idmaquinaria INT AUTO_INCREMENT PRIMARY KEY,
	tIPO varchar(50),
	Modelo varchar(50),
    marca VARCHAR(50)
);
CREATE TABLE salida (
    idsalida INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    responsable VARCHAR(50)
);
CREATE TABLE salidaDetalle (
    idsalidaDetalle INT AUTO_INCREMENT PRIMARY KEY,
    idsalida INT,
    idproducto INT,
    cantidad INT,
	idmaquinaria INT,
	FOREIGN KEY (idsalida) REFERENCES salida(idsalida),
    FOREIGN KEY (idproducto) REFERENCES producto(idproducto),
	FOREIGN KEY (idmaquinaria) REFERENCES maquinaria(idmaquinaria)
);
CREATE TABLE Requerimiento (
    idrequerimiento INT AUTO_INCREMENT PRIMARY KEY,      -- Clave primaria auto-incremental
    fechaRequerimiento DATE,                             -- Fecha del requerimiento
    critero VARCHAR(50),                                 -- Descripción o criterio del requerimiento (corrigiendo el nombre a "criterio")
    idsolicitador INT,                                   -- ID del solicitante
    idsupervisor INT,                                    -- ID del supervisor
    FOREIGN KEY (idsolicitador) REFERENCES solicitador(idsolicitador) ON DELETE CASCADE,  -- Relación con la tabla solicitador
    FOREIGN KEY (idsupervisor) REFERENCES supervisor(idsupervisor) ON DELETE CASCADE  -- Relación con la tabla supervisor
);
CREATE TABLE requerimientoDetalle (
    idrequerimientoDetalle INT AUTO_INCREMENT PRIMARY KEY, -- Clave primaria auto-incremental
    idrequerimiento INT,                                   -- ID del requerimiento asociado
    idproducto INT,                                        -- ID del producto asociado
    cantidad INT,                                          -- Cantidad solicitada
    iduso INT,                                             -- ID de uso asociado
    idproveedor INT,                                       -- ID del proveedor
    idmaquinaria INT,                                      -- ID de maquinaria asociada
    idalmacen INT,                                         -- ID del almacén
    precioUnitario DECIMAL(10, 2),                         -- Precio unitario
    precioTotal DECIMAL(10, 2),                  -- Precio total calculado (cantidad * precioUnitario) y persistido
    FOREIGN KEY (idproducto) REFERENCES producto(idproducto) ON DELETE CASCADE, -- Relación con producto
    FOREIGN KEY (iduso) REFERENCES uso(iduso) ON DELETE CASCADE,             -- Relación con uso
    FOREIGN KEY (idproveedor) REFERENCES proveedor(idproveedor) ON DELETE CASCADE, -- Relación con proveedor
    FOREIGN KEY (idalmacen) REFERENCES Almacen(idalmacen) ON DELETE CASCADE,     -- Relación con almacén
    FOREIGN KEY (idrequerimiento) REFERENCES Requerimiento(idrequerimiento) ON DELETE CASCADE -- Relación con requerimiento
);
INSERT INTO usuario (nombre, apellidos, correo, contraseña) VALUES
('Gian', 'Alejandro', 'gian.alejandro@koelsa.com', '123');
INSERT INTO marca (nombre) VALUES
('Tek Bond'),
('Komatsu'),
('XCMG'),
('SANY'),
('John Deere');
INSERT INTO proveedor (ruc, nombre, direccion, telefono, correo) VALUES
(20609509865, 'NRC PACK', 'Calle Falsa 123', '555-1234', 'proveedorA@email.com'),
(20547071931, 'L&L INDUSTRIAL', 'Avenida Real 456', '555-5678', 'proveedorB@email.com'),
(20602430325, 'COLOR Y MATIZ LOPEZ', 'Calle 14 789', '555-9101', 'proveedorC@email.com'),
(20610808655, 'A&C DYNAMIS', 'Paseo Central 101', '555-1122', 'proveedorD@email.com');
INSERT INTO almacen (nombre, direccion, capacidad) VALUES
('Taller Lima', 'Kilometro 26 Ant. Pan. Sur', 500);
INSERT INTO UnidadMedida (nomUnidad) VALUES ('Kilogramo');
INSERT INTO UnidadMedida (nomUnidad) VALUES ('Metro');
INSERT INTO UnidadMedida (nomUnidad) VALUES ('Cilindro');
INSERT INTO UnidadMedida (nomUnidad) VALUES ('Und');

INSERT INTO uso (nomUso) VALUES ('Consumible');
INSERT INTO uso (nomUso) VALUES ('Comercial');
INSERT INTO uso (nomUso) VALUES ('Doméstico');
INSERT INTO almacenDetalle (idalmacen, ubicacion)
VALUES 
(1, 'A1'),
(1, 'A2'),
(1, 'A3');
INSERT INTO familia (nomfamilia) values
('ADESIVO');
INSERT INTO producto (partname, descripcion, idmarca, idunidadMedida, cantidad, idproveedor, precio, idfamilia, idalmacenDetalle) 
VALUES ('122', 'ADESIVO INSTANTANEO 50 g', 4, 4, 6, 1, 5.6, 1, 1);
INSERT INTO entrada (fecha) VALUES
('2024-01-01'),
('2024-02-01'),
('2024-03-01'),
('2024-04-01'),
('2024-05-01');
select * from entrada;
select * from entradaDetalle;
INSERT INTO entradaDetalle (identrada, idproducto, cantidad) VALUES 
(1, 1, 10),
(2, 1, 20);


-- Insertar entrada
INSERT INTO salida (fecha) VALUES
('2024-01-01'),
('2024-02-01'),
('2024-03-01'),
('2024-04-01'),
('2024-05-01');
INSERT INTO salidaDetalle(idsalida, idproducto, cantidad) VALUES
(1, 1, 10),
(2, 2, 20),
(3, 3, 15),
(4, 4, 25),
(5, 1, 15);
INSERT INTO maquinaria (idmarca, descripcion) VALUES
(1, 'Excavadora'),
(2, 'Retroexcavadora'),
(3, 'Volquete');
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

select * from usuario;
go
INSERT INTO marca (nombre) VALUES
('Loctite')
INSERT INTO familia (nomfamilia) VALUES
('Embalaje')
select * from familia
DELETE FROM familia 
    WHERE idfamilia = 5
select * from usuario
DBCC CHECKIDENT ('marca', RESEED, 5);
UPDATE producto		
    SET idfamilia = 7 where idproducto=4

SELECT p.idproducto, p.partname, p.descripcion, m.nombre AS Marca,
                        pr.nombre AS Proveedor, f.nomfamilia AS Familia,
                        u.nomUnidad AS UnidadMedida, p.cantidad, p.precio, a.nombre AS Almacen
                    FROM producto p
                    LEFT JOIN marca m ON p.idmarca = m.idmarca
                    LEFT JOIN proveedor pr ON p.idproveedor = pr.idproveedor
                    LEFT JOIN familia f ON p.idfamilia = f.idfamilia
                    LEFT JOIN UnidadMedida u ON p.idunidadMedida = u.idunidadMedida
                    LEFT JOIN almacen a ON p.idalmacen = a.idalmacen
                    WHERE f.nomfamilia = 'embalaje'


select * from marca
INSERT INTO marca (nombre) VALUES
('Mobil')
DBCC CHECKIDENT ('marca', RESEED, 5);

SET IDENTITY_INSERT producto ON;

-- Step 2: Delete the row with idproducto = 3
DELETE FROM producto WHERE idproducto = 3;

-- Step 3: Insert the new row with the desired idproducto value (1002)
-- Make sure to include all the other necessary column values in the INSERT statement
INSERT INTO producto (idproducto, other_column1, other_column2) 
VALUES (1002, 'value1', 'value2');  -- Replace with actual column values

-- Step 4: Disable identity insert to return to default behavior
SET IDENTITY_INSERT producto OFF;

select * from entradaDetalle

select * from producto

select * from usuario

SELECT idproducto FROM producto WHERE partname

SELECT DISTINCT local_tcp_port FROM sys.dm_exec_connections WHERE local_tcp_port IS NOT NULL

select * from proveedor

DELETE FROM proveedor WHERE idproveedor = 1002;

DBCC CHECKIDENT ('proveedor', RESEED, 5);


select * from usuario

ALTER TABLE proveedor ADD  ruc varchar(11) 
SELECT idproveedor, nombre,ruc,direccion,telefono, correo FROM proveedor

select * from usuario

select * from producto

INSERT INTO maquinaria (Tipo, Modelo, marca)
VALUES 
    ('Excavadora', '330D L', 'Caterpillar'),
    ('Bulldozer', 'D155AX-8', 'Komatsu'),
    ('Retroexcavadora', 'L90H', 'Volvo'),
    ('Grúa', 'LTM 1350-6.1', 'Liebherr'),
    ('Pala Cargadora', 'ZAXIS 330LC', 'Hitachi');

	select * from producto


select * from salida
select * from salidaDetalle

SELECT e.fecha, d.cantidad
                FROM entradaDetalle d
                JOIN entrada e ON e.identrada = d.identrada
                WHERE d.idproducto = 1002

SELECT s.fecha, sd.cantidad, m.tipo, m.modelo, m.marca
                FROM salidaDetalle sd
                JOIN salida s ON s.idsalida = sd.idsalida
                JOIN maquinaria m ON m.idmaquinaria = sd.idmaquinaria
                WHERE sd.idproducto = 1002

Select * from usuario

UPDATE almacen     SET nombre = 'Taller Lima'
CREATE TABLE almacenDetalle (
    idalmacenDetalle INT IDENTITY(1,1) PRIMARY KEY,
    idalmacen int,
	ubicacion VARCHAR(100) NOT NULL,
);
go

INSERT INTO almacen(nombre, direccion, capacidad)
VALUES 
    ('Shougang', ' Departamento A', '1000')

INSERT INTO almacen(nombre, direccion, capacidad)
VALUES 
    ('Chicama', ' Departamento Chicama', '3000')

select * from almacenDetalle

-- Insertar datos en la tabla almacenDetalle
INSERT INTO almacenDetalle (idalmacen, ubicacion)
VALUES 
(2, 'A1'),
(2, 'A2'),
(3, 'A3')

-- Luego agregar la llave foránea:
ALTER TABLE almacen
ADD CONSTRAINT fk_almacenDetalle
FOREIGN KEY (idalmacenDetalle)
REFERENCES almacenDetalle(idalmacenDetalle);

SELECT * FROM usuario

SELECT * FROM salida

select * from salidaDetalle


ALTER TABLE salida
ADD observacion VARCHAR(200);

select * from producto
	SELECT 
		p.idproducto AS ID,
		p.partname AS PartName,
		p.descripcion AS Descripción,
		m.nombre AS Marca,
		pr.nombre AS Proveedor,
		f.nomfamilia AS Familia,
		u.nomUnidad AS "Unidad de Medida",
		p.cantidad AS Cantidad,
		p.precio AS Precio,
		a.nombre AS Almacen,
		ad.ubicacion AS Ubicacion
	FROM producto p
	LEFT JOIN marca m ON p.idmarca = m.idmarca
	LEFT JOIN proveedor pr ON p.idproveedor = pr.idproveedor
	INNER JOIN UnidadMedida u ON p.idunidadMedida = u.idunidadMedida
	INNER JOIN familia f ON p.idfamilia = f.idfamilia
	LEFT JOIN almacenDetalle ad ON p.idalmacenDetalle = ad.idalmacenDetalle 
	INNER JOIN almacen a ON a.idalmacen = ad.idalmacen  


select * from usuario

Select * from producto

Select * from salidaDetalle


UPDATE salida SET observacion = 'Sin OBSERVACION' where observacion is null

select * from usuario

select * from requerimiento

select * from requerimientoDetalle

BEGIN TRANSACTION;
INSERT INTO Requerimiento (fechaRequerimiento, critero, total) VALUES ('2024-12-26', 'Prueba', 0.0);
SELECT SCOPE_IDENTITY() AS last_id;
ROLLBACK TRANSACTION;

SELECT SCOPE_IDENTITY() AS last_id

INSERT INTO Requerimiento (fechaRequerimiento, critero, total) VALUES ('2024-12-23', 'urgente',2)

SELECT

                        p.descripcion AS Descripción,
                        rd.cantidad AS Cantidad,
                        rd.precioUnitario AS PrecioUnitario,
                        rd.precioTotal AS PrecioTotal,
                        u.nomUso AS Uso,
                        pr.nombre AS Proveedor,
                        m.Modelo AS Maquinaria,
                        a.nombre AS Almacén
                    FROM requerimientoDetalle rd
                    LEFT JOIN producto p ON rd.idproducto = p.idproducto
                    LEFT JOIN uso u ON rd.iduso = u.iduso
                    LEFT JOIN proveedor pr ON rd.idproveedor = pr.idproveedor
                    LEFT JOIN maquinaria m ON rd.idmaquinaria = m.idmaquinaria
                    LEFT JOIN almacen a ON rd.idalmacen = a.idalmacen

	
select * from proveedor

select * from usuario