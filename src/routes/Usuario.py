from flask import Blueprint, request, jsonify
# database
from database.db import db
# model and schema
from models.UsuarioModel import UsuarioModel, UsuarioSchema

for_him = UsuarioSchema()
for_them = UsuarioSchema(many=True)


usuario_bp = Blueprint("usuario", __name__)


@usuario_bp.route("/")
def get_all_usuarios():
  try:
    usuarios = UsuarioModel.query.all()
    result = for_them.dump(usuarios)
    return jsonify(result)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400
  

@usuario_bp.route("/<id>")
def get_usuario(id):
  try:
    usuario = UsuarioModel.query.get(id)
    if usuario == None:
      return jsonify({"message": "Elemento no encontrado."}), 400
    return for_him.jsonify(usuario)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400


@usuario_bp.route("/add", methods=["POST"])
def add_usuario():
  try:
    data = request.json
    nombre = data["nombre"]
    usuario = data["usuario"]
    clave = data["clave"]
    tipousuario_id = data["tipousuario_id"]
    estado = data["estado"]
    usuario = UsuarioModel(nombre, usuario, clave, tipousuario_id, estado)
    db.session.add(usuario)
    db.session.commit()
    return for_him.jsonify(usuario)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400
  

@usuario_bp.route("/update/<id>", methods=["PUT"])
def update_usuario(id):
  try:
    data = request.json
    usuario = UsuarioModel.query.get(id)
    if usuario == None:
      return jsonify({"message": "Elemento no encontrado."}), 400
    if data["nombre"]:
      usuario.nombre = data["nombre"]
    if data["usuario"]:
      usuario.usuario = data["usuario"]
    if data["clave"]:
      usuario.clave = data["clave"]
    if data["tipousuario_id"]:
      usuario.tipousuario_id = data["tipousuario_id"]
    if data["estado"]:
      usuario.estado = data["estado"]
    db.session.commit()
    return for_him.jsonify(usuario)
  except Exception as ex:
    return jsonify({"message", str(ex)}), 400
  

@usuario_bp.route("/delete/<id>", methods=["DELETE"])
def delete_usuario(id):
  try:
    usuario = UsuarioModel.query.get(id)
    if usuario == None:
      return jsonify({"message": "Elemento no encontrado"}), 400
    db.session.delete(usuario)
    db.session.commit()
    return for_him.jsonify(usuario)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400