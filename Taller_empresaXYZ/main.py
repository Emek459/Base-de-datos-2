from flask import Flask, request, jsonify, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'pepito2'
# Configuración de la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'empresaXYZ'
mysql = MySQL(app)

# CREATE - Crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nombre = data['nombre']
    apellido = data['apellido']
    estado = data['estado']
    contraseña = data['contraseña']
    cargo = data['cargo']
    salario = data['salario']
    fecha_ingreso = data['fecha_ingreso']
    perfil_nombre = data['perfil_nombre']  # Cambiar a perfil_nombre

    # Buscar el id del perfil basándose en el nombre del perfil proporcionado
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM Perfil WHERE nombre = %s", (perfil_nombre,))
    perfil_id = cur.fetchone()
    cur.close()

    if perfil_id:
        perfil_id = perfil_id[0]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Usuario (id, nombre, apellido, estado, contraseña, cargo, salario, fecha_ingreso, perfil_id) VALUES (UNHEX(REPLACE(UUID(), '-', '')), %s, %s, %s, %s, %s, %s, %s, %s)", (nombre, apellido, estado, contraseña, cargo, salario, fecha_ingreso, perfil_id))
        mysql.connection.commit()
        cur.close()

        return jsonify({"mensaje": "Usuario creado correctamente"}), 201
    else:
        return jsonify({"error": "Perfil no encontrado"}), 404



# READ - Obtener todos los usuarios por su user_name
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    user_name = request.args.get('user_name')  # Obtener user_name de la query string
    if user_name:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombre, apellido, user_name, estado, cargo, salario, fecha_ingreso FROM usuario WHERE user_name = %s", (user_name,))
        usuarios = cur.fetchall()
        cur.close()

        # Convertir los valores binarios de id a hexadecimal para ser JSON serializable
        usuarios_json = []
        for usuario in usuarios:
            usuario_dict = {
                "id": usuario[0].hex(),  # Convertir id binario a hexadecimal
                "nombre": usuario[1],
                "apellido": usuario[2],
                "user_name": usuario[3],
                "estado": usuario[4],
                "cargo": usuario[5],
                "salario": float(usuario[6]),  # Convertir salario a float
                "fecha_ingreso": str(usuario[7])  # Convertir fecha_ingreso a string
            }
            usuarios_json.append(usuario_dict)

        return jsonify(usuarios_json)
    else:
        return jsonify({"error": "Se requiere el parámetro 'user_name' en la consulta"}), 400



# UPDATE - Actualizar un usuario
@app.route('/usuarios/<string:user_name>', methods=['PUT'])
def actualizar_usuario(user_name):
    data = request.get_json()
    nombre = data['nombre']
    apellido = data['apellido']
    estado = data['estado']
    contraseña = data['contraseña']
    cargo = data['cargo']
    salario = data['salario']
    fecha_ingreso = data['fecha_ingreso']
    perfil_id = data['perfil_id']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE Usuario SET nombre = %s, apellido = %s, estado = %s, contraseña = %s, cargo = %s, salario = %s, fecha_ingreso = %s, perfil_id = %s WHERE user_name = %s", (nombre, apellido, estado, contraseña, cargo, salario, fecha_ingreso, perfil_id, user_name))
    mysql.connection.commit()
    cur.close()

    return jsonify({"mensaje": "Usuario actualizado correctamente"})

@app.route('/usuarios/<string:user_name>', methods=['DELETE'])
def eliminar_usuario(user_name):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Usuario WHERE user_name = %s", (user_name,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"mensaje": "Usuario eliminado correctamente"})



# Función para verificar las credenciales de inicio de sesión
def verificar_credenciales(usuario, contraseña):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Usuario WHERE user_name = %s AND contraseña = %s", (usuario, contraseña))
    usuario = cur.fetchone()
    cur.close()
    if usuario:
        return True
    else:
        return False

# Ruta para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data['user_name']
    contraseña = data['contraseña']
    if verificar_credenciales(usuario, contraseña):
        session['user_name'] = usuario
        return jsonify({"mensaje": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401

# Ruta para cerrar sesión
@app.route('/logout/<string:usuario>', methods=['GET'])
def logout(usuario):
    if usuario in session:
        session.pop(usuario, None)
        return jsonify({"mensaje": f"Sesión de {usuario} cerrada correctamente"}), 200
    else:
        return jsonify({"error": f"No hay ninguna sesión activa para {usuario}"}), 400

# Obtener todas las actividades de un usuario por su user_name
@app.route('/usuarios/<string:user_name>/actividades', methods=['GET'])
def obtener_actividades_usuario(user_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT a.id, a.nombre, a.fecha FROM Actividad a INNER JOIN Fidelizacion f ON a.id = f.actividad_id INNER JOIN Usuario u ON f.usuario_id = u.id WHERE u.user_name = %s", (user_name,))
    actividades = cur.fetchall()
    cur.close()
    return jsonify(actividades)

# Obtener todas las fidelizaciones de un usuario por su user_name
@app.route('/usuarios/<string:user_name>/fidelizaciones', methods=['GET'])
def obtener_fidelizaciones_usuario(user_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT f.id, f.puntos, a.nombre AS actividad_nombre, a.fecha AS actividad_fecha FROM Fidelizacion f INNER JOIN Actividad a ON f.actividad_id = a.id INNER JOIN Usuario u ON f.usuario_id = u.id WHERE u.user_name = %s", (user_name,))
    fidelizaciones = cur.fetchall()
    cur.close()
    return jsonify(fidelizaciones)

# CREATE - Crear una nueva actividad para un usuario específico
@app.route('/usuarios/<string:user_name>/actividades', methods=['POST'])
def crear_actividad_usuario(user_name):
    datos_actividad = request.json
    nombre = datos_actividad['nombre']
    fecha = datos_actividad['fecha']

    # Busca el usuario por su user_name para obtener su id
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM Usuario WHERE user_name = %s", (user_name,))
    usuario_id = cur.fetchone()
    cur.close()

    if usuario_id:
        # Si el usuario existe, inserta la actividad asociada a ese usuario
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Actividad (nombre, fecha) VALUES (%s, %s)", (nombre, fecha))
        actividad_id = cur.lastrowid  # Obtén el ID de la actividad recién creada
        cur.close()

        # Asocia la actividad recién creada con el usuario
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario_actividad (usuario_id, actividad_id) VALUES (%s, %s)", (usuario_id[0], actividad_id))
        mysql.connection.commit()
        cur.close()

        return jsonify({"mensaje": "Actividad creada correctamente"}), 201
    else:
        return jsonify({"error": f"No se encontró ningún usuario con el user_name {user_name}"}), 404

# DELETE - Eliminar una actividad de un usuario específico
@app.route('/usuarios/<string:user_name>/actividades/<uuid:id>', methods=['DELETE'])
def eliminar_actividad_usuario(user_name, id):
    # Verifica si el usuario existe
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM Usuario WHERE user_name = %s", (user_name,))
    usuario_id = cur.fetchone()
    cur.close()

    if usuario_id:
        # Si el usuario existe, elimina la relación entre usuario y actividad
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM usuario_actividad WHERE usuario_id = %s AND actividad_id = UUID_TO_BIN(%s)", (usuario_id[0], id))
        mysql.connection.commit()

        if cur.rowcount > 0:
            # Si se eliminó correctamente la relación, elimina la actividad
            cur.execute("DELETE FROM Actividad WHERE id = UUID_TO_BIN(%s)", (id,))
            mysql.connection.commit()
            cur.close()
            return jsonify({"mensaje": "Actividad eliminada correctamente"}), 200
        else:
            cur.close()
            return jsonify({"error": "La actividad no pertenece al usuario especificado"}), 404
    else:
        return jsonify({"error": f"No se encontró ningún usuario con el user_name {user_name}"}), 404

# DELETE - Eliminar una fidelización de un usuario específico
@app.route('/usuarios/<string:user_name>/fidelizaciones/<uuid:id>', methods=['DELETE'])
def eliminar_fidelizacion_usuario(user_name, id):
    # Primero, verifica si el usuario existe
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM Usuario WHERE user_name = %s", (user_name,))
    usuario_id = cur.fetchone()
    cur.close()

    if usuario_id:
        # Si el usuario existe, elimina la fidelización asociada a ese usuario
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Fidelizacion WHERE usuario_id = %s AND id = UUID_TO_BIN(%s)", (usuario_id[0], id))
        mysql.connection.commit()
        cur.close()

        if cur.rowcount > 0:
            return jsonify({"mensaje": "Fidelización eliminada correctamente"}), 200
        else:
            return jsonify({"error": "La fidelización no pertenece al usuario especificado"}), 404
    else:
        return jsonify({"error": f"No se encontró ningún usuario con el user_name {user_name}"}), 404

if __name__ == '__main__':
    app.run(debug=True)

