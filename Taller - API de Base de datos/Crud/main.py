from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurar la conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="sistema_expediente"
)
cursor = db.cursor()

# Rutas para las operaciones CRUD
@app.route('/')
def index():
    # Obtener todos los expedientes de la base de datos
    cursor.execute("SELECT * FROM expediente")
    expedientes = cursor.fetchall()
    return render_template('index.html', expedientes=expedientes)

@app.route('/crear', methods=['POST'])
def crear():
    # Obtener datos del formulario
    conductor = request.form['conductor']
    aseguradora_id = int(request.form['aseguradora'])  # Convertir a entero
    numero_de_caso = request.form['numero_de_caso']
    tipo_de_proceso = request.form['tipo_de_proceso']
    # Insertar nuevo expediente en la base de datos
    cursor.execute("INSERT INTO expediente (conductor, aseguradora_id, numero_de_caso, tipo_de_proceso) VALUES (%s, %s, %s, %s)", (conductor, aseguradora_id, numero_de_caso, tipo_de_proceso))
    db.commit()
    return redirect(url_for('index'))

@app.route('/actualizar', methods=['POST'])
def actualizar():
    # Obtener datos del formulario
    expediente_id = request.form['expediente_id']
    conductor = request.form['conductor']
    aseguradora_id = int(request.form['aseguradora'])  # Cambiado a 'aseguradora_id'
    numero_de_caso = request.form['numero_de_caso']
    tipo_de_proceso = request.form['tipo_de_proceso']
    # Actualizar expediente en la base de datos
    cursor.execute("UPDATE expediente SET conductor=%s, aseguradora_id=%s, numero_de_caso=%s, tipo_de_proceso=%s WHERE expediente_id=%s", (conductor, aseguradora_id, numero_de_caso, tipo_de_proceso, expediente_id))
    db.commit()
    return redirect(url_for('index'))


@app.route('/eliminar/<int:expediente_id>',methods=['POST'])
def eliminar(expediente_id):
    # Eliminar expediente de la base de datos
    cursor.execute("DELETE FROM expediente WHERE expediente_id=%s", (expediente_id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
