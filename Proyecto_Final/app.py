from flask import Flask, render_template


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Bd2_123456789@pharmatech.c1084u60ifuv.us-east-1.rds.amazonaws.com/farmacia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva el seguimiento de modificaciones


# Importa los modelos después de inicializar db
from models import Medicamento, Empleado, Venta, DetalleVenta, db

db.init_app(app)

# Crea las tablas en la base de datos
with app.app_context():
    db.create_all()

# Rutas para cada módulo
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventario')
def inventario():
    medicamentos = Medicamento.query.all()
    return render_template('inventario.html', medicamentos=medicamentos)

@app.route('/reportes')
def reportes():
    ventas = Venta.query.all()
    return render_template('reportes.html', ventas=ventas)

@app.route('/empleados')
def empleados():
    empleados = Empleado.query.all()
    return render_template('empleados.html', empleados=empleados)

if __name__ == '__main__':
    app.run(debug=True)
