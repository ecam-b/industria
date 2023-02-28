from database.db import db
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class UsuarioModel(db.Model):
  __tablename__ = "usuario"


  id = db.Column(db.Integer, primary_key=True)
  nombre = db.Column(db.String(100))
  usuario = db.Column(db.String(100), nullable=False, unique=True)
  clave = db.Column(db.String(300))
  tipousuario_id = db.Column(db.Integer, db.ForeignKey("tipousuario.id"), nullable=False)
  estado = db.Column(db.Integer)


  def __init__(self, nombre, usuario, clave, tipousuario_id, estado):
    self.nombre = nombre
    self.usuario = usuario
    self.clave = clave
    self.tipousuario_id = tipousuario_id
    self.estado = estado


class UsuarioSchema(ma.Schema):
  class Meta:
    fields = ("id", "nombre", "usuario", "clave", "tipousuario_id", "estado")