import os
from flask import Flask, jsonify, request, session
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import db, Usuario, Producto, Venta
import requests
from requests.exceptions import Timeout, RequestException

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


@app.get("/api/clima")
@login_required
def obtener_clima():
    api_key = os.getenv('API_KEY_CLIMA')

    url_clima = "https://api.open-meteo.com/v1/forecast?latitude=-34.61&longitude=-58.38&current_weather=true"

    try:
        respuesta = requests.get(url_clima, timeout=5)

        respuesta.raise_for_status()

        datos_clima = respuesta.json()
        weather_code = datos_clima['current_weather']['weathercode']
        temperatura = datos_clima['current_weather']['temperature']

        llueve = weather_code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]

        return jsonify({
            "status": "success",
            "temperatura": temperatura,
            "alerta_lluvia": llueve,
            "recomendacion": "ALERTA: Pronóstico de lluvia. Reducir producción de stock para evitar mermas." if llueve else "Buen clima. Operar con stock estándar."
        }), 200

    except Timeout:
        app.logger.warning("Timeout alcanzado al consultar la API de clima.")
        return jsonify(
            {"status": "error", "mensaje": "El servicio de clima tardó demasiado en responder. Reintente."}), 504

    except RequestException as e:
        app.logger.error(f"Fallo en la comunicación con la API externa: {e}")
        return jsonify({"status": "error", "mensaje": "No se pudo obtener el reporte climático actual."}), 502


if __name__ == "__main__":
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(port=5000, debug=debug_mode)