from datetime import date

from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import current_user, LoginManager, UserMixin, login_user, logout_user, login_required
app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Bd2_123456789@pharmatech.c1084u60ifuv.us-east-1.rds.amazonaws.com/farmacia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva el seguimiento de modificaciones
app.secret_key = 'pepito1334'
# Importa los modelos después de inicializar db
from models import Medicamento, Empleado, Venta, DetalleVenta, db, Usuario,Roles

db.init_app(app)
login_manager=LoginManager()
login_manager.login_view = 'login'
# Crea las tablas en la base de datos
with app.app_context():
    db.create_all()
@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
     return redirect(url_for('login'))  # Redireccionar al usuario al formulario de inicio de sesión

@login_manager.user_loader
def cargar_usuario(id_usuario):
    return Usuario.query.get(id_usuario)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']

        # Verificar las credenciales del usuario
        usuario = Usuario.query.filter_by(user_name=user_name).first()
        if usuario and usuario.password == password:
            return redirect('/home')  # Redireccionar al usuario a la página principal
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    return render_template('login.html')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/inventario', methods=['GET', 'POST'])
def inventario():
    if request.method == 'POST':
        # Agregar un nuevo medicamento
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        cantidad_disponible = request.form['cantidad_disponible']

        nuevo_medicamento = Medicamento(nombre=nombre, descripcion=descripcion, precio=precio,
                                        cantidad_disponible=cantidad_disponible)
        db.session.add(nuevo_medicamento)
        db.session.commit()

    medicamentos = Medicamento.query.all()
    return render_template('inventario.html', medicamentos=medicamentos)


@app.route('/eliminar_medicamento/<int:medicamento_id>', methods=['POST'])
def eliminar_medicamento(medicamento_id):
    medicamento = Medicamento.query.get_or_404(medicamento_id)
    db.session.delete(medicamento)
    db.session.commit()
    return redirect('/inventario')


@app.route('/editar_medicamento/<int:medicamento_id>', methods=['GET', 'POST'])
def editar_medicamento(medicamento_id):
    medicamento = Medicamento.query.get_or_404(medicamento_id)
    if request.method == 'POST':
        medicamento.nombre = request.form['nombre']
        medicamento.descripcion = request.form['descripcion']
        medicamento.precio = request.form['precio']
        medicamento.cantidad_disponible = request.form['cantidad_disponible']
        db.session.commit()
        return redirect('/inventario')
    return render_template('editar_medicamento.html', medicamento=medicamento)


from models import Venta, DetalleVenta


@app.route('/reportes')
def reportes():
    # Obtener la fecha de hoy
    fecha_hoy = date.today()

    # Consultar las ventas realizadas hoy
    ventas_hoy = Venta.query.filter_by(fecha=fecha_hoy).all()

    # Crear una lista para almacenar los detalles de las ventas
    detalles_ventas = []

    # Recorrer las ventas para obtener los detalles y el nombre del empleado
    for venta in ventas_hoy:
        detalles_venta = {
            'fecha': venta.fecha,
            'empleado': venta.empleado.nombre + ' ' + venta.empleado.apellido,
            'detalles': []
        }
        for detalle in venta.detalle_venta:
            detalles_venta['detalles'].append({
                'medicamento': detalle.medicamento.nombre,
                'cantidad': detalle.cantidad,
                'precio_unitario': detalle.precio_unitario
            })
        detalles_ventas.append(detalles_venta)

    return render_template('reportes.html', detalles_ventas=detalles_ventas)

@app.route('/empleados', methods=['GET', 'POST'])
def empleados():
    if request.method == 'POST':
        # Agregar un nuevo empleado
        nombre = request.form['nombre']
        apellido = request.form['apellido']  # Nuevo campo
        edad = int(request.form['edad'])  # Nuevo campo
        cargo = request.form['cargo']
        fecha_contratacion = request.form['fecha_contratacion']
        user_name = request.form['user_name']
        rol_id = request.form['rol']

        nuevo_empleado = Empleado(nombre=nombre, apellido=apellido, edad=edad, cargo=cargo,
                                  fecha_contratacion=fecha_contratacion)
        db.session.add(nuevo_empleado)
        db.session.commit()
        # Crear nuevo usuario relacionado
        nuevo_usuario = Usuario(user_name=user_name, password=123456,rol_id=rol_id, empleado_id=nuevo_empleado.id)
        db.session.add(nuevo_usuario)
        db.session.commit()
    roles = Roles.query.all()
    empleados = Empleado.query.all()
    return render_template('empleados.html', empleados=empleados, roles=roles)


@app.route('/eliminar_empleado/<int:empleado_id>', methods=['POST'])
def eliminar_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    db.session.delete(empleado)
    db.session.commit()
    return redirect('/empleados')


@app.route('/editar_empleado/<int:empleado_id>', methods=['GET', 'POST'])
def editar_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    if request.method == 'POST':
        empleado.nombre = request.form['nombre']
        empleado.apellido = request.form['apellido']  # Nuevo campo
        empleado.edad = int(request.form['edad'])  # Nuevo campo
        empleado.cargo = request.form['cargo']
        empleado.fecha_contratacion = request.form['fecha_contratacion']
        db.session.commit()
        return redirect('/empleados')
    return render_template('editar_empleado.html', empleado=empleado)


@app.route('/admin')
@login_required
def admin():
    # Verificar si el usuario actual tiene el rol de administrador
    usuario_actual = Usuario.query.filter_by(id=current_user.id).first()
    if usuario_actual.rol_id != 1:  # Suponiendo que el ID del rol de administrador es 1
        # Si el usuario no es administrador, puedes redirigirlo a otra página o mostrar un error
        return "Acceso denegado. Debes ser un administrador para acceder a esta página."

    # Si el usuario es administrador, obtener todos los usuarios para mostrarlos en la tabla
    usuarios = Usuario.query.all()
    return render_template('admin.html', usuarios=usuarios)
# Rutas para agregar, editar y eliminar usuarios
@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']

        nuevo_usuario = Usuario(username=username, password=password, rol=rol)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario agregado correctamente', 'success')
        return redirect(url_for('admin'))


@app.route('/editar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
def editar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    if request.method == 'POST':
        # Obtener los datos del formulario de edición
        # Actualizar la contraseña y el rol en la base de datos
        usuario.password = request.form['password']
        usuario.rol = request.form['rol']
        db.session.commit()
        flash('Usuario actualizado correctamente', 'success')
        return redirect('/administrar/usuarios')

    # Renderizar el formulario de edición con los datos del usuario
    return render_template('editar_usuario.html', usuario=usuario)


@app.route('/eliminar_usuario/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado correctamente', 'success')
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True)
