from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Clave secreta para las sesiones

# Función para crear la tabla si no existe
def create_table():
    with sqlite3.connect('data.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS registros (
                        id INTEGER PRIMARY KEY,
                        ip TEXT NOT NULL,
                        nombre TEXT NOT NULL,
                        departamento TEXT NOT NULL,
                        anexo TEXT 
                    )''')

create_table()  # Llamada a la función para crear la tabla

# Función para crear la tabla de usuarios si no existe
def create_user_table():
    with sqlite3.connect('data.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        name TEXT NOT NULL
                    )''')

create_user_table()  # Llamada a la función para crear la tabla de usuarios

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('mostrar_registros'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
            user = c.fetchone()
        if user:
            session['username'] = user[1]  # Almacena el nombre de usuario en la sesión
            session['name'] = user[3]  # Almacena el campo 'name' en la sesión
            return redirect(url_for('mostrar_registros'))
        else:
            return render_template('login.html', mensaje='Credenciales incorrectas', tipo='danger')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Elimina el nombre de usuario de la sesión
    return redirect(url_for('login'))

@app.route('/crear', methods=['GET'])
def mostrar_formulario_creacion():
    return render_template('crear.html')

@app.route('/registro', methods=['POST'])
def crear_registro():
    if request.method == 'POST':
        data = request.form
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            # Insertar los datos en la tabla
            c.execute('''INSERT INTO registros (ip, nombre, departamento, anexo) VALUES (?, ?, ?, ?)''',
                        (data['ip'], data['nombre'], data['departamento'], data['anexo']))
        return redirect(url_for('mostrar_registros', mensaje='Registro creado satisfactoriamente', tipo='warning'))
    else:
        return "Método no permitido", 405

@app.route('/editar/<int:registro_id>', methods=['GET', 'POST'])
def editar_registro(registro_id):
    if request.method == 'GET':
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM registros WHERE id = ?''', (registro_id,))
            registro = c.fetchone()
        if registro:
            # Convertir la tupla a un diccionario para poder acceder a los valores por clave
            registro = {'id': registro[0], 'ip': registro[1], 'nombre': registro[2], 'departamento': registro[3], 'anexo': registro[4]}
            return render_template('editar.html', registro=registro)
        else:
            return jsonify({'mensaje': 'Registro no encontrado'}), 404
        
    elif request.method == 'POST':
        # Aquí manejas la lógica para guardar los cambios en el registro
        data = request.form
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            c.execute('''UPDATE registros SET ip = ?, nombre = ?, departamento = ?, anexo = ? WHERE id = ?''',
                        (data['ip'], data['nombre'], data['departamento'], data['anexo'], registro_id))
        return redirect(url_for('mostrar_registros', mensaje='Registro actualizado', tipo='warning'))

@app.route('/borrar/<int:registro_id>', methods=['POST'])
def borrar_registro(registro_id):
    if request.method == 'POST':
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            c.execute('''DELETE FROM registros WHERE id = ?''', (registro_id,))
        return redirect(url_for('mostrar_registros', mensaje='Registro eliminado', tipo='warning'))
    else:
        return "Método no permitido", 405

@app.route('/listar', methods=['GET'])
def mostrar_registros():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    mensaje = request.args.get('mensaje')
    tipo = request.args.get('tipo')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    query = request.args.get('query', '')  # Obtener el parámetro de búsqueda desde la URL
    with sqlite3.connect('data.db') as conn:
        c = conn.cursor()

        # Búsqueda por nombre o departamento
        search_query = f"%{query}%"

        # Consulta paginada con búsqueda
        offset = (page - 1) * per_page
        c.execute('''SELECT * FROM registros WHERE nombre LIKE ? OR departamento LIKE ? OR ip LIKE ? LIMIT ? OFFSET ?''',
                    (search_query, search_query, search_query, per_page, offset))
        registros = c.fetchall()  # Obtener registros de la página actual

        # Obtener total de registros para la paginación
        c.execute('''SELECT COUNT(*) FROM registros WHERE nombre LIKE ? OR departamento LIKE ? OR ip LIKE ?''', (search_query, search_query, search_query))
        total_count = c.fetchone()[0]
        total_pages = (total_count - 1) // per_page + 1

    return render_template('listar.html', registros=registros, mensaje=mensaje, tipo=tipo, page=page, total_pages=total_pages, query=query)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



