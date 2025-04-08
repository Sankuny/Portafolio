from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración desde variables de entorno
app.secret_key = os.getenv("SECRET_KEY")
app.debug = os.getenv("DEBUG", "False") == "True"  # Interpreta correctamente True/False

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
        
        print("Mensaje recibido:")
        print(f"Nombre: {name}")
        print(f"Correo: {email}")
        print(f"Mensaje: {message}")
        
        flash("¡Gracias por tu mensaje! Me pondré en contacto pronto.")
        return redirect("/contact")

    return render_template("contact.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
