import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from models import db, Producto, Usuario, Venta

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///smartgastro.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_segura_produccion')

db.init_app(app)

@app.get("/")
def home():
    return jsonify({
        "status": "success",
        "mensaje": "Servidor SmartGastro Web operacional."
    }), 200

if __name__ == "__main__":
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(port=5000, debug=debug_mode)