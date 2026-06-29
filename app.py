import os
from flask import Flask, jsonify, request, session
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import db, Usuario, Producto, Venta

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///smartgastro.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_segura_produccion')

db.init_app(app)

with app.app_context():
    db.create_all()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return jsonify({"status": "error", "mensaje": "Acceso denegado: Inicie sesión primero."}), 401
        return f(*args, **kwargs)

    return decorated_function


@app.get("/")
def home():
    return jsonify({
        "status": "success",
        "mensaje": "Servidor SmartGastro Web operacional."
    }), 200


@app.post("/api/auth/register")
def registrar_usuario():
    datos = request.get_json()
    if not datos or 'username' not in datos or 'password' not in datos:
        return jsonify({"status": "error", "mensaje": "Datos obligatorios incompletos."}), 400

    try:
        password_encriptada = generate_password_hash(datos['password'])
        nuevo_usuario = Usuario(username=datos['username'], password_hash=password_encriptada)

        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"status": "success", "mensaje": "Usuario registrado exitosamente."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "mensaje": "El nombre de usuario ya existe o el servidor falló."}), 400


@app.post("/api/auth/login")
def login():
    datos = request.get_json()
    if not datos or 'username' not in datos or 'password' not in datos:
        return jsonify({"status": "error", "mensaje": "Credenciales incompletas."}), 400

    usuario = Usuario.query.filter_by(username=datos['username']).first()

    if usuario and check_password_hash(usuario.password_hash, datos['password']):
        session['usuario_id'] = usuario.id
        return jsonify({"status": "success", "mensaje": "Inicio de sesión exitoso."}), 200

    return jsonify({"status": "error", "mensaje": "Usuario o contraseña incorrectos."}), 401


@app.get("/api/dashboard")
@login_required
def ver_dashboard():
    return jsonify({
        "status": "success",
        "mensaje": "Bienvenido al panel privado de SmartGastro."
    }), 200


@app.post("/api/auth/logout")
def logout():
    session.pop('usuario_id', None)
    return jsonify({"status": "success", "mensaje": "Sesión cerrada correctamente."}), 200


if __name__ == "__main__":
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(port=5000, debug=debug_mode)