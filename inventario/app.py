from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, send_file, session
import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'Soing2024'  # Reemplaza con una clave secreta segura
def create_database():
    logging.debug("Creating database")
    with sqlite3.connect('base.db') as conn:
        pass
#crea las tablas y la base de datos
def crear_base_producto():
    print("Creando tabla productos...")
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS productos(
                  id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                  producto TEXT NOT NULL,
                  cantidad INTEGER NOT NULL,
                  dispositivo TEXT NOT NULL )''')
    conn.commit()
    conn.close()

    print("Tabla productos creada.")
def crear_base_usos():
        conn = sqlite3.connect('base.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS usos(
                  id_usos INTEGER PRIMARY KEY AUTOINCREMENT,
                  producto TEXT NOT NULL,
                  cantidad INTEGER NOT NULL,
                  numero_ticket INTEGER NOT NULL,
                  dispositivo TEXT NOT NULL,
                  id_producto_previo INTEGER NOT NULL,
                  FOREIGN KEY (id_producto_previo) REFERENCES productos(id_producto))''')
        conn.commit()
        conn.close()
def crear_base_login():
        conn = sqlite3.connect('base.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS usuarios(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  usuario TEXT UNIQUE NOT NULL,
                  contraseña TEXT NOT NULL,
                  nombre_usuario TEXT NOT NULL )''')
        conn.commit()
        conn.close()
try:
    create_database()
    crear_base_producto()
    crear_base_usos()
    crear_base_login()
except Exception as e:
    print(f"Error: {e}")

@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Elimina el nombre de usuario de la sesión
    return redirect(url_for('login'))
#empieza la creacion de links y funciones relacionados
#index
@app.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    c.execute("SELECT * FROM productos")
    productos = c.fetchall()
    c.execute("SELECT * FROM usuarios")
    usuarios = c.fetchall()
    conn.close()
    user_id = usuarios[0][0] if usuarios else None
    id_producto = productos[0][0] if productos else None
    resp = make_response(render_template('index.html', id_producto=id_producto, usuarios=usuarios, productos=productos))
    if user_id:
        resp.set_cookie('user_id', str(user_id))
        resp.set_cookie('id_tarea', str(id_producto))
    return resp
#agregar producto
@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    c.execute("SELECT * FROM productos")
    producto = c.fetchall()
    conn.close()
    if request.method =='POST':
        producto = request.form['producto_a']
        cantidad = request.form['cantidad_a']
        dispositivo = request.form['dispositivo_a']


        conn = sqlite3.connect('base.db')
        c = conn.cursor()
        c.execute("INSERT INTO productos (producto, cantidad, dispositivo) VALUES (?,?,?)", (producto, cantidad, dispositivo))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    else:
        conn = sqlite3.connect('base.db')
        c = conn.cursor()
        c.execute("SELECT * FROM productos")
        productos = c.fetchall()
        conn.close()

        user_id = request.cookies.get('user_id')
        return render_template('crear_tarea.html', productos=productos, user_id=user_id)
    
#editar producto
@app.route('/editar_producto/<int:id_producto>')
def editar_producto(id_producto):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    c.execute("SELECT * FROM productos WHERE id_producto = ?", (id_producto))
    producto = c.fetchone()

    if request.method == 'POST':
        producto = request.form('producto')
        cantidad  = request.form('cantidad')
        dispositivo = request.form('dispositivo')
        id_producto = request.cookies.get('id_producto')
        c.execute("""UPDATE productos SET producto= ?,cantidad= ?,dispositivo= ? WHERE id_producto = ? """,(producto, cantidad, dispositivo, id_producto))
        conn.commit()
        conn.close()
        return redirect(url_for('index', id_producto=id_producto))
    conn.commit()
    conn.close()
    return render_template('editar_producto.html', producto=producto, id_producto=id_producto)
#inicio de sesion

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        with sqlite3.connect('base.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
            user = c.fetchone()

        if user:
            session['usuario'] = user[1]
            session['nombre_usuario'] = user[3]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', mensaje='Credenciales incorrectas', tipo='danger')
    else:
        return render_template('login.html')

#agregar producto
@app.route('/agregar_uso')
def agregar_uso():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    c.execute("SELECT * FROM productos")
    producto = c.fetchall()
    conn.close()
    if request.method =='POST':
        producto = request.form['producto_a']
        cantidad = request.form['cantidad_a']
        numero_ticket = request.form['dispositivo_a']


        conn = sqlite3.connect('base.db')
        c = conn.cursor()
        c.execute("INSERT INTO productos (producto, cantidad, dispositivo) VALUES (?,?,?)", (producto, cantidad, numero_ticket))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    else:
        conn = sqlite3.connect('base.db')
        c = conn.cursor()
        c.execute("SELECT * FROM productos")
        productos = c.fetchall()
        conn.close()

        user_id = request.cookies.get('user_id')
        return render_template('agregar_uso.html', productos=productos, user_id=user_id)
    

#eliminar producto
@app.route('/borrar/<int:id_producto>', methods=['POST'])
def eliminar(id_producto):

    if request.method == 'POST':
        with sqlite3.connect('base.db') as conn:
            c = conn.cursor()
            c.execute('''DELETE FROM productos WHERE producto = ?''', (id_producto,))
        return redirect(url_for('index', mensaje='Registro eliminado', tipo='warning'))
    else:
        return "Método no permitido", 405








if __name__ == '__main__':
    #app.run(host='192.168.1.144', debug=True)
    app.run(host='10.6.163.14', debug=True)