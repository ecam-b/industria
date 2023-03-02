from database.db import db
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class ChorroModel(db.Model):
  __tablename__ = "chorro"


  id = db.Column(db.Integer, primary_key=True)
  descripcion = db.Column(db.String(100))
  extruder = db.Column(db.Integer)
  ordenproducciones = db.relationship("OrdenproduccionModel")

  
  def __init__(self, descripcion, extruder):
    self.descripcion = descripcion
    self.extruder = extruder


class ChorroSchema(ma.Schema):
  class Meta:
    fields = ("id", "description", "extruder")