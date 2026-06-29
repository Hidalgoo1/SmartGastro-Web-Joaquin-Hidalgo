from flask_sqlalchemy import SQLAlchemy
from flask import HTTPException

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

    def descontar_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor a cero.")
        if self.stock < cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Error de Stock: No hay suficientes unidades de {self.nombre}. Stock actual: {self.stock}."
            )
        self.stock -= cantidad

    def aumentar_stock(self, cantidad):
        if cantidad < 0:
            raise ValueError("No se puede añadir una cantidad negativa de stock.")
        self.stock += cantidad

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)