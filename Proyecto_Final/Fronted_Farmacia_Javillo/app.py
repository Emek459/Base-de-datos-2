from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Bd2_123456789@pharmatech.c1084u60ifuv.us-east-1.rds.amazonaws.com/farmacia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva el seguimiento de modificaciones


# Importa los modelos después de inicializar db
from models import Medicamento, Empleado, Venta, DetalleVenta, db, Usuario, Roles
db.init_app(app)

# Crea las tablas en la base de datos
with app.app_context():
    db.create_all()

# Rutas para cada módulo
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/inicio')
def index():
    return render_template('index.html')


@app.route('/inventario')
def inventario():
    medicamentos = Medicamento.query.all()
    return render_template('inventario.html', medicamentos=medicamentos)


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
            'empleado': Empleado.query.get(venta.id_empleado).nombre,
            'detalles': []
        }
        # Obtener los detalles de la venta actual
        detalles_venta_db = DetalleVenta.query.filter_by(id_venta=venta.id).all()
        for detalle in detalles_venta_db:
            # Obtener el nombre del medicamento a partir de su ID
            nombre_medicamento = Medicamento.query.get(detalle.id_medicamento).nombre
            detalles_venta['detalles'].append({
                'medicamento': nombre_medicamento,
                'cantidad': detalle.cantidad,
                'precio_unitario': detalle.precio_unitario
            })
        detalles_ventas.append(detalles_venta)

    return render_template('reportes.html', detalles_ventas=detalles_ventas)

# @app.route('/eliminar_empleado/<int:empleado_id>', methods=['POST'])
# def eliminar_empleado(empleado_id):
#     empleado = Empleado.query.get_or_404(empleado_id)
#     db.session.delete(empleado)
#     db.session.commit()
#     return redirect('/empleados')


@app.route('/show_menu')
def menu():
    return render_template('menu.html')


@app.route('/show_navbar')
def navbar():
    return render_template('nav-bar.html')


@app.route('/login', methods=['POST'])
def user_auth():
    data = request.get_json()
    content = data.get("content")
    user_name = content['user_id']
    password = content['password']
    usuario = Usuario.query.filter_by(user_name=user_name).first()
    if usuario and usuario.password == password:
        print(f"Usuario autenticado: {usuario.user_name}")
        return {'status': 200, 'message': 'Usuario autenticado'}
    else:
        return {'status': 401, 'message': 'Usuario Incorrecto o contraseña incorrecta'}


if __name__ == '__main__':
    app.run(debug=True, port=7512, host='0.0.0.0')
