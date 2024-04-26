from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'))
    empleado = db.relationship('Empleado', backref=db.backref('usuario', uselist=False), lazy=True)


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)


class Medicamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    cantidad_disponible = db.Column(db.Integer, nullable=False)


class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)  # Nuevo campo
    edad = db.Column(db.Integer, nullable=False)  # Nuevo campo
    cargo = db.Column(db.String(100), nullable=False)
    fecha_contratacion = db.Column(db.Date, nullable=False)


class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    empleado = db.relationship('Empleado', backref=db.backref('ventas', lazy=True))


class DetalleVenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    id_medicamento = db.Column(db.Integer, db.ForeignKey('medicamento.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)