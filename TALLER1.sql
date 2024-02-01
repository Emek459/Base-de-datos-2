CREATE DATABASE Taller1;
CREATE TABLE Bitacora (
    id INT NOT NULL AUTO_INCREMENT,
    descripcion TEXT,
    fecha DATETIME,
    operacion VARCHAR(50),
    entidad_id INT,
    cliente_id INT,
    transaccion_id INT,
    rol_id INT,
    perfil_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (entidad_id) REFERENCES Entidades(id),
    FOREIGN KEY (cliente_id) REFERENCES Clientes(id),
    FOREIGN KEY (transaccion_id) REFERENCES Transacciones(id),
    FOREIGN KEY (rol_id) REFERENCES Roles(id),
    FOREIGN KEY (perfil_id) REFERENCES Perfiles(id)
);
CREATE TABLE Perfiles (
    id INT NOT NULL AUTO_INCREMENT,
    estatus VARCHAR(50),
    correo VARCHAR(255),
    tipo_perfil VARCHAR(50),
    PRIMARY KEY (id)
);
CREATE TABLE Roles (
    id INT NOT NULL AUTO_INCREMENT,
    nombre_de_rol VARCHAR(255),
    tipo_rol VARCHAR(50),
    nivel_seguridad INT,
    PRIMARY KEY (id)
);
CREATE TABLE Transacciones (
    id INT NOT NULL AUTO_INCREMENT,
    monto DECIMAL(10, 2),
    fecha DATE,
    tipo_transaccion VARCHAR(50),
    cliente_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (cliente_id) REFERENCES Clientes(id)
);
CREATE TABLE Clientes (
    id INT NOT NULL AUTO_INCREMENT,
    cedula_cliente VARCHAR(20),
    nombre_cliente VARCHAR(255),
    apellido_cliente VARCHAR(255),
    entidad_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (entidad_id) REFERENCES Entidades(id)
);
CREATE TABLE Entidades (
    id INT NOT NULL AUTO_INCREMENT,
    tipo_identidad VARCHAR(255),
    nombre_identidad VARCHAR(255),
    RUC VARCHAR(20),
    PRIMARY KEY (id)
);

--Proceso DML

-- Inserción de datos en la tabla `Entidades`
INSERT INTO Entidades (tipo_identidad, nombre_identidad, RUC) VALUES
    ('Tipo1', 'Entidad1', '123456789'),
    ('Tipo2', 'Entidad2', '987654321');

-- Inserción de datos en la tabla `Clientes`
INSERT INTO Clientes (cedula_cliente, nombre_cliente, apellido_cliente, entidad_id) VALUES
    ('Cedula1', 'Cliente1', 'Apellido1', 1),
    ('Cedula2', 'Cliente2', 'Apellido2', 2);

-- Inserción de datos en la tabla `Transacciones`
INSERT INTO Transacciones (monto, fecha, tipo_transaccion, cliente_id) VALUES
    (100.00, '2024-02-01', 'Compra', 1),
    (150.50, '2024-02-02', 'Venta', 2);

-- Inserción de datos en la tabla `Roles`
INSERT INTO Roles (nombre_de_rol, tipo_rol, nivel_seguridad) VALUES
    ('Admin', 'Administrativo', 1),
    ('Usuario', 'Operacional', 2);

-- Inserción de datos en la tabla `Perfiles`
INSERT INTO Perfiles (estatus, correo, tipo_perfil) VALUES
    ('Activo', 'correo1@ejemplo.com', 'Tipo1'),
    ('Inactivo', 'correo2@ejemplo.com', 'Tipo2');

-- Inserción de datos en la tabla `Bitacora`
INSERT INTO Bitacora (descripcion, fecha, operacion, entidad_id, cliente_id, transaccion_id, rol_id, perfil_id) VALUES
    ('Operación 1', '2024-02-01 12:00:00', 'Actualización', 1, 1, 1, 1, 1),
    ('Operación 2', '2024-02-02 14:30:00', 'Inserción', 2, 2, 2, 2, 2);


