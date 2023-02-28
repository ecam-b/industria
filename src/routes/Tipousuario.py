from flask import Blueprint, request, jsonify
# database
from database.db import db
# models and schemas
from models.TipousuarioModel import TipousuarioModel, TipousuarioSchema

for_him = TipousuarioSchema()
for_them = TipousuarioSchema(many=True)

tipousuario_bp = Blueprint("tipousuario", __name__)

@tipousuario_bp.route("/")
def gell_all_tipousuarios():
  """
  Obtener todos los tipos de usuarios
  Obtener todos los tipos de usuario registrados en la base de datos
  ---
  tags:
  - Tipousuario
  responses:
    200:
      description: OK
      schema:
        type: object
        properties:
          id:
            type: integer
            description: ID de tipo de usuario
          descripcion:
            type: string
            description: Descripción de usuario
        example:
          id: 3
          descripcion: user
    400:
      description: Recurso no encontrado.
    500:
      description: Error en el servidor.
  """
  try:
    tipousuarios = TipousuarioModel.query.all()
    result = for_them.dump(tipousuarios)
    return jsonify(result)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400


@tipousuario_bp.route("/<id>")
def get_tipousuario(id):
  try:
    tipousuario = TipousuarioModel.query.get(id)
    if tipousuario == None:
      return jsonify({"message": "Elemento no encontrado."}), 400
    return for_him.jsonify(tipousuario)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400
  

@tipousuario_bp.route("/add", methods=["POST"])
def add_tipousuario():
  try:
    data = request.json
    descripcion = data["descripcion"]
    tipousuario = TipousuarioModel(descripcion)
    db.session.add(tipousuario)
    db.session.commit()
    return for_him.jsonify(tipousuario)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400
  

@tipousuario_bp.route("/update/<id>", methods=["PUT"])
def update_tipousuario(id):
  try:
    data = request.json
    tipousuario = TipousuarioModel.query.get(id)
    if tipousuario == None:
      return jsonify({"message": "Elemento no encontrado."}), 400
    if data["descripcion"]:
      tipousuario.descripcion = data["descripcion"]
    db.session.commit()
    return for_him.jsonify(tipousuario)
  except Exception as ex:
    return jsonify({"message": str(ex)})


@tipousuario_bp.route("/delete/<id>", methods=["DELETE"])
def delete_tipousuario(id):
  try:
    tipousuario = TipousuarioModel.query.get(id)
    if tipousuario == None:
      return jsonify({"message": "Elemento no encontrado."}), 400
    db.session.delete(tipousuario)
    db.session.commit()
    return for_him.jsonify(tipousuario)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400