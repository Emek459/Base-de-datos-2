CREATE DATABASE distributor
-- Creación de la tabla Proveedores
USE distributor
CREATE TABLE Proveedores (
    Id INT AUTO_INCREMENT,
    Nombre VARCHAR(50),
    Status VARCHAR(50),
    Ciudad VARCHAR(50),
    PRIMARY KEY(Id)
);

-- Creación de la tabla Partes
USE distributor
CREATE TABLE Partes (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Numero_parte VARCHAR(50),
    Nombre VARCHAR(100),
    Color VARCHAR(50),
    Peso DECIMAL(10, 2),
    Precio DECIMAL(10, 2),
    Ciudad VARCHAR(100)
);

-- Creación de la tabla Taller
USE distributor
CREATE TABLE Taller (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_taller VARCHAR(100),
    Ciudad VARCHAR(100)
);

-- Creación de la tabla Movimiento_partes
USE distributor
CREATE TABLE Movimiento_partes (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Id_Proveedor INT,
    Id_Parte INT,
    Id_Taller INT,
    Cantidad_utilizada INT,
    FOREIGN KEY (Id_Proveedor) REFERENCES Proveedores(Id),
    FOREIGN KEY (Id_Parte) REFERENCES Partes(Id),
    FOREIGN KEY (Id_Taller) REFERENCES Taller(Id)
);


-- Inserciones en la tabla Proveedores
INSERT INTO Proveedores (Nombre, Status, Ciudad) VALUES
('Smith', '20', 'Londres'),
('Jones', '10', 'Paris'),
('Blake', '30', 'Paris'),
('Clark', '20', 'Londres'),
('Adams', '30', 'Atenas');


-- Inserciones en la tabla Partes
INSERT INTO Partes (Numero_parte, Nombre, Color, Peso, Precio, Ciudad) VALUES
('001', 'tuerca', 'rojo', 12, 0.5,'Londres'),
('002', 'Perno', 'verde', 17, 0.8,'Paris'),
('003', 'Tornillo', 'azul', 17, 0.7,'Roma'),
('004', 'Tornillo', 'rojo', 14, 0.6,'Londres'),
('005', 'Leva', 'Azul', 12, 1.2,'Paris'),
('006', 'Engrane', 'rojo', 19, 2.5, 'Londres');


-- Inserciones en la tabla Taller
INSERT INTO Taller (Nombre_taller, Ciudad) VALUES
('Clasificador', 'Paris'),
('Monitor', 'Roma'),
('OCR', 'Atenas'),
('Consola', 'Atenas'),
('RAID', 'Londres'),
('EDS', 'Oslo'),
('Cinta','Londres');

-- vista Proveedor
CREATE VIEW Vista_Proveedores AS
SELECT * FROM Proveedores;

-- vista partes disponible
CREATE VIEW Vista_Partes AS
SELECT * FROM Partes;


-- Vista de las partes por ciudad

CREATE VIEW Vista_Partes_Por_Ciudad AS
SELECT Nombre, Color, Precio, Ciudad FROM Partes;

-- Vista de los proveedores y sus parte
CREATE VIEW Vista_Proveedores_Partes AS
SELECT P.Nombre AS Proveedor, Pr.Nombre AS Parte, Pr.Color, Pr.Precio
FROM Proveedores P
JOIN Movimiento_partes M ON P.Id = M.Id_Proveedor
JOIN Partes Pr ON M.Id_Parte = Pr.Id;

-- partes utilizadas por cada proveedor 
CREATE VIEW Vista_Total_Partes_Proveedor AS
SELECT P.Nombre AS Proveedor, COUNT(*) AS Total_Partes
FROM Proveedores P
JOIN Movimiento_partes M ON P.Id = M.Id_Proveedor
GROUP BY P.Nombre;

-- Inserciones en la tabla Movimiento_partes
INSERT INTO Movimiento_partes (Id_Proveedor, Id_Parte, Id_Taller, Cantidad_utilizada) VALUES
(1, 1, 1, 10),
(2, 2, 2, 8),
(3, 3, 3, 5),
(4, 4, 4, 7),
(5, 5, 5, 12),
(1, 6, 1, 15),
(2, 1, 2, 6),
(3, 2, 3, 9),
(4, 3, 4, 3),
(5, 4, 5, 8),
(1, 5, 1, 11),
(2, 6, 2, 4),
(3, 1, 3, 7),
(4, 2, 4, 10),
(5, 3, 5, 5),
(1, 4, 1, 9),
(2, 5, 2, 13),
(3, 6, 3, 6),
(4, 1, 4, 8),
(5, 2, 5, 11);
