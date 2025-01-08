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
CREATE TABLE unidadMedida (
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
    responsable VARCHAR(50),
    observacion VARCHAR(250)
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
    criterio VARCHAR(50),                                 -- Descripción o criterio del requerimiento (corrigiendo el nombre a "criterio")
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
    FOREIGN KEY (idalmacen) REFERENCES almacen(idalmacen) ON DELETE CASCADE,     -- Relación con almacén
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
INSERT INTO entradaDetalle (identrada, idproducto, cantidad) VALUES 
(1, 1, 10),
(2, 1, 20);
INSERT INTO salida (fecha) VALUES
('2024-01-01'),
('2024-02-01'),
('2024-03-01'),
('2024-04-01'),
('2024-05-01');
INSERT INTO salidaDetalle(idsalida, idproducto, cantidad) VALUES
(1, 1, 1),
(2, 1, 2);
INSERT INTO maquinaria (tipo,modelo,marca) VALUES
('Excavadora','330D L','Caterpillar'),
('Retroexcavadora','D155AX-8','Komatsu'),
('Volquete','LTM 1350-6.1','Volvo');
INSERT INTO solicitador (nombre) VALUES
('Diego'),
('Carlos'),
('Luis');
INSERT INTO supervisor (nombre) VALUES
('Henrry');
INSERT INTO Requerimiento (fechaRequerimiento, criterio, idsolicitador, idsupervisor) VALUES
('2024-01-01', 'Urgente', 1, 1),
('2024-02-01', 'Normal', 2, 1),
('2024-03-01', 'Urgente', 3, 1),
('2024-04-01', 'Normal', 1, 1),
('2024-05-01', 'Urgente', 1, 1);
INSERT INTO requerimientoDetalle (idrequerimiento, idproducto, cantidad, idproveedor, precioUnitario) VALUES
(1,1, 10, 1, 25.50),
(1,1, 20, 1, 30.75),
(2,1, 15, 1, 45.00),
(3,1, 15, 1, 45.00),
(4,1, 25, 1, 12.30);

INSERT INTO marca (nombre) VALUES 
('Abralit'),
('Abro'),
('Action'),
('ADEX'),
('AFD'),
('Africanito'),
('Alfa Pack'),
('Allen USA'),
('Alternativo'),
('Ambersil'),
('Anchor'),
('Anitsa'),
('Asaki'),
('Astron'),
('Atlas'),
('Bahco'),
('Bannek'),
('Bosch'),
('Buffalo'),
('CAT'),
('CGR'),
('CH'),
('Chain Hoist'),
('Clevite'),
('CNHowder'),
('Crossman'),
('CTP'),
('Cubull'),
('Dariza'),
('Denso'),
('Derek'),
('DeWalt'),
('Donaldson'),
('Dremel'),
('Duker'),
('Durón'),
('Ecco'),
('EDSI'),
('Encoparts'),
('ESAB'),
('Everwell'),
('FAG'),
('Faro LED'),
('Ferton'),
('Fleetguard'),
('Genérico'),
('Genuine Parts'),
('Gold Crown'),
('Golden Glove'),
('Halogeen'),
('Haltec'),
('Handock'),
('Handok Hydraulic'),
('Harris'),
('HD'),
('HKT'),
('Home Light'),
('HONT'),
('Hydraulic'),
('IMACO'),
('Importación'),
('Indeco'),
('Indura'),
('Insize'),
('Interface'),
('IPD'),
('JIC'),
('Jonnesway'),
('Kamasa'),
('Karcher'),
('Kleenguard'),
('Kleine'),
('Komatsu'),
('Kyotech'),
('KyotechS'),
('Libus'),
('Lincoln Electric'),
('Loctite'),
('Makita'),
('MammutHS'),
('Master'),
('Mastergloss'),
('Max'),
('Menekkes'),
('Mico'),
('Mixtrack'),
('Mobil'),
('Motorola'),
('MYX'),
('Narva'),
('Nazca'),
('Neodeter'),
('NOK'),
('Norton'),
('NSK'),
('NTN'),
('OAllen'),
('Oerlikon'),
('Omega'),
('Opalux'),
('Optibelt'),
('Parker'),
('Pegafan'),
('Permatex'),
('Picasso'),
('Pimmaksan'),
('Pollak'),
('Portiza'),
('Proto'),
('PTA'),
('Roberlo'),
('Saeflex'),
('Sander'),
('Sapolio'),
('SATA'),
('Schneider'),
('Schubert'),
('SCL'),
('Seiken'),
('Sherwin Williams'),
('Shield Flex'),
('Shurtape'),
('Sika'),
('SKF'),
('SMBX'),
('Snap On'),
('Soldimix'),
('Sonic'),
('Splendid'),
('Stanley'),
('Steel Pro'),
('Sumaq'),
('Sunwork'),
('Supercast'),
('SY-Klone'),
('Tagtix'),
('Tek Bond'),
('Timken'),
('Titan'),
('TKL'),
('Tolerance'),
('Tolsize'),
('Top Lift'),
('Toptul'),
('Tramontina'),
('Truper'),
('Tyrolit'),
('UNI-T'),
('Urrea'),
('UVEX XV100'),
('Uyustools'),
('Victor'),
('Virutex'),
('Voltex'),
('Washer'),
('WIKA'),
('Williams'),
('Willys Plast'),
('WLL'),
('Worldgasket'),
('Wurth'),
('Wypal'),
('Yellow'),
('Yellow Line');

use koelsa
select * from usuario

