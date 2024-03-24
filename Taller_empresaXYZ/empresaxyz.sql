CREATE DATABASE empresaXYZ

-- Creación de las tablas con UUID como llaves primarias
SELECT*FROM usuario

CREATE TABLE Usuario (
    id BINARY(16) PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    estado ENUM('activo', 'inactivo'),
    contraseña VARCHAR(100),
    cargo VARCHAR(50),
    salario DECIMAL(10, 2),
    fecha_ingreso DATE,
    perfil_id BINARY(16),
    FOREIGN KEY (perfil_id) REFERENCES Perfil(id)
);

CREATE TABLE Perfil (
    id BINARY(16),
    nombre VARCHAR(50),
    fecha_vigencia DATE,
    descripcion TEXT,
    PRIMARY KEY(id)
);
SELECT*FROM perfil
INSERT INTO Perfil (id, nombre, fecha_vigencia, descripcion) 
VALUES 
(UNHEX(REPLACE(UUID(), '-', '')), 'Administrador', '2024-03-25', 'Encargado de la administración del sistema'),
(UNHEX(REPLACE(UUID(), '-', '')), 'Trabajador', '2024-03-25', 'Personal de la empresa'),
(UNHEX(REPLACE(UUID(), '-', '')), 'Cliente', '2024-03-25', 'Clientes de la empresa'),
(UNHEX(REPLACE(UUID(), '-', '')), 'Jefe', '2024-03-25', 'Encargado de supervisar equipos');
(UNHEX(REPLACE(UUID(), '-', '')), 'Analista de Datos', '2024-03-25', 'Encargado del análisis de datos de la empresa'),
(UNHEX(REPLACE(UUID(), '-', '')), 'Desarrollador Web', '2024-03-25', 'Encargado del desarrollo de aplicaciones web'),
(UNHEX(REPLACE(UUID(), '-', '')), 'Diseñador Gráfico', '2024-03-25', 'Encargado del diseño gráfico y la creatividad visual'),
(UNHEX(REPLACE(UUID(), '-', '')), 'Contador', '2024-03-25', 'Encargado de la contabilidad y las finanzas de la empresa'),
(UNHEX(REPLACE(UUID(), '-', '')), 'Recursos Humanos', '2024-03-25', 'Encargado de la gestión de recursos humanos y el reclutamiento'),
(UNHEX(REPLACE(UUID(), '-', '')), 'Marketing', '2024-03-25', 'Encargado de las estrategias de marketing y publicidad');

CREATE TABLE Login (
    id BINARY(16) PRIMARY KEY,
    usuario_id BINARY(16),
    fecha_hora DATETIME,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
);
CREATE TABLE Usuario_Actividad (
    usuario_id BINARY(16),
    actividad_id BINARY(16),
    PRIMARY KEY (usuario_id, actividad_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (actividad_id) REFERENCES Actividad(id)
);

CREATE TABLE Actividad (
    id BINARY(16) PRIMARY KEY,
    nombre VARCHAR(100),
    fecha DATE
);
-- Relacionar aleatoriamente actividades con usuarios existentes
INSERT INTO Usuario_Actividad (usuario_id, actividad_id)
SELECT 
    u.id AS usuario_id, 
    a.id AS actividad_id
FROM
    (SELECT id FROM Usuario ORDER BY RAND() LIMIT 15) AS u
CROSS JOIN
    (SELECT id FROM Actividad ORDER BY RAND() LIMIT 15) AS a;

-- Mostrar las actividades insertadas
SELECT * FROM Actividad;

-- Mostrar las actividades insertadas
SELECT * FROM Actividad;

INSERT INTO Actividad (id, nombre, fecha) VALUES (UNHEX(REPLACE(UUID(), '-', '')), 'Terminar labores', '2024-03-21');


CREATE TABLE Fidelizacion (
    id BINARY(16) PRIMARY KEY,
    usuario_id BINARY(16),
    actividad_id BINARY(16),
    puntos INT,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (actividad_id) REFERENCES Actividad(id)
);


CREATE VIEW UsuariosActivos AS
SELECT * FROM Usuario WHERE estado = 'activo';

DELIMITER //
CREATE PROCEDURE InsertarUsuario(
    IN nombre VARCHAR(50),
    IN apellido VARCHAR(50),
    IN estado ENUM('activo', 'inactivo'),
    IN contraseña VARCHAR(100),
    IN cargo VARCHAR(50),
    IN salario DECIMAL(10, 2),
    IN fecha_ingreso DATE,
    IN perfil_id INT
)
BEGIN
    INSERT INTO Usuario (nombre, apellido, estado, contraseña, cargo, salario, fecha_ingreso, perfil_id)
    VALUES (nombre, apellido, estado, contraseña, cargo, salario, fecha_ingreso, perfil_id);
END //
DELIMITER ;

-- Crear una vista para contar la cantidad de fidelizaciones por usuario en los últimos 12 meses
CREATE VIEW Fidelizaciones_12_meses AS
SELECT 
    f.usuario_id,
    COUNT(*) AS cantidad_fidelizaciones
FROM 
    Fidelizacion f
INNER JOIN 
    Actividad a ON f.actividad_id = a.id
WHERE 
    a.fecha >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
GROUP BY 
    f.usuario_id;

-- Calcular el total de usuarios fidelizados en los últimos 12 meses
SELECT 
    COUNT(*) AS total_fidelizados_12_meses
FROM 
    Fidelizaciones_12_meses;

