from flask import Flask, render_template, request, redirect
import sqlite3
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración del correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'corolairem@gmail.com'  # tu email
app.config['MAIL_PASSWORD'] = 'TU_CONTRASEÑA_DE_APP'  # contraseña de aplicación de Gmail
app.config['MAIL_DEFAULT_SENDER'] = 'corolairem@gmail.com'

mail = Mail(app)

# Inicializar DB
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                email TEXT,
                mensaje TEXT
            )
        ''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form['mensaje']

    # Guardar en base de datos
    with sqlite3.connect('database.db') as conn:
        conn.execute(
            "INSERT INTO leads (nombre, email, mensaje) VALUES (?, ?, ?)",
            (nombre, email, mensaje)
        )
        conn.commit()

    # Enviar email
    msg = Message("Nuevo contacto desde tu Landing",
                  recipients=['corolairem@gmail.com'])
    msg.body = f"Nombre: {nombre}\nEmail: {email}\nMensaje:\n{mensaje}"
    mail.send(msg)

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

