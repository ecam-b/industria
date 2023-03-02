from database.db import db
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class OrdenproduccionModel(db.Model):
  __tablename__ = "ordenproduccion"


  id = db.Column(db.Integer, primary_key=True)
  fecha = db.Column(db.Date)
  mezcla = db.Column(db.Integer) # fk
  kilos = db.Column(db.Integer)
  turno = db.Column(db.Integer) # fk
  operador = db.Column(db.Integer) # fk
  observacion = db.Column(db.String(500))
  extruder = db.Column(db.Integer, db.ForeignKey("chorro.id"), nullable=False) # fk


  def __ini__(self, fecha, mezcla, kilos, extruder, turno, operador, observacion):
    self.fecha = fecha
    self.mezcla = mezcla
    self.kilos = kilos
    self.extruder = extruder
    self.turno = turno
    self.operador = operador
    self.observacion = observacion

  
class OrdenproduccionSchema(ma.Schema):
  class Meta:
    fields = ("id", "fecha", "mezcla", "kilos", "extruder", "turno", "operador", "observacion")