from database.db import db
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class TipousuarioModel(db.Model):
  __tablename__ = "tipousuario"


  id = db.Column(db.Integer, primary_key=True)
  descripcion = db.Column(db.String(100), unique=True)
  usuarios = db.relationship("UsuarioModel", backref="tipo", lazy=True)


  def __init__(self, descripcion):
    self.descripcion = descripcion


class TipousuarioSchema(ma.Schema):
  class Meta:
    fields = ("id", "descripcion")