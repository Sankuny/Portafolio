from flask import Flask, render_template, request, redirect, flash, session
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.security import check_password_hash
from datetime import timedelta


# ─────────────────────────────────────────────────────────────
# 🔐 Cargar variables de entorno
load_dotenv()
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS_HASH = os.getenv("ADMIN_PASS_HASH")

# ─────────────────────────────────────────────────────────────
# ⚙️ Configuración de la app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.debug = os.getenv("DEBUG", "False") == "True"
app.permanent_session_lifetime = timedelta(minutes=30)

# ─────────────────────────────────────────────────────────────
# 💾 Configuración de SQLite + SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensajes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#  Modelo para mensajes
class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

# ─────────────────────────────────────────────────────────────
#  Rutas públicas
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Guardar mensaje en la base de datos
        nuevo_mensaje = Mensaje(nombre=name, correo=email, contenido=message)
        db.session.add(nuevo_mensaje)
        db.session.commit()

        flash("¡Gracias por tu mensaje! Me pondré en contacto pronto.")
        return redirect("/contact")

    return render_template("contact.html")

# ─────────────────────────────────────────────────────────────
#  Rutas de autenticación
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USER and check_password_hash(ADMIN_PASS_HASH, password):
            session.permanent = True
            session["logged_in"] = True
            flash("Has iniciado sesión correctamente.")
            return redirect("/admin/mensajes")
        else:
            flash("Credenciales incorrectas.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.")
    return redirect("/login")

# ─────────────────────────────────────────────────────────────
# 🛡️ Vista protegida del panel admin
@app.route("/admin/mensajes")
def admin_mensajes():
    if not session.get("logged_in"):
        return redirect("/login")

    mensajes = Mensaje.query.order_by(Mensaje.fecha.desc()).all()
    return render_template("admin.html", mensajes=mensajes)

# ─────────────────────────────────────────────────────────────
# 🚀 Iniciar servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
