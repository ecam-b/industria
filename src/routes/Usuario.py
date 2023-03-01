from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
# database
from database.db import db
# uuid
import uuid
# jwt
import jwt
# datetime
from datetime import datetime, timedelta
# config
from config import SECRET_KEY
# model and schema
from models.UsuarioModel import UsuarioModel, UsuarioSchema

for_him = UsuarioSchema()
for_them = UsuarioSchema(many=True)


usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/login", methods=["POST"])
def login():
  try:
    data = request.json
    usuario = UsuarioModel.query.filter_by(usuario = data["usuario"]).first()
    if not usuario:
      return jsonify({"message": "Usuario no registrado."}), 400
    if check_password_hash(usuario.clave, data["clave"]):
      token = jwt.encode(
        {"id_privado": usuario.id_privado, "exp": datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY,
        algorithm = "HS256"
      )
      return jsonify({"token": token})
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400

@usuario_bp.route("/")
def get_all_usuarios():
  """
  Obtener todos los usuario
  Obtener todos los usuario registrados en la base de datos
  ---
  tags:
  - Usuario
  responses:
    200:
      description: OK
      schema:
        type: object
        properties:
          id:
            type: integer
            description: ID de usuario
          nombre:
            type: string
            description: Nombre de usuario
          usuario:
            type: string
            description: Nombre de usuario del usuario
          clave:
            type: string
            description: Clave de usuario
          tipousuario_id:
            type: integer
            description: Tipo de usuario al que corresponde este usuario
          estado:
            type: integer
            description: Estado del usuario
        example:
          id: 1
          nombre: Usuario Generico
          usuario: UsuaGene
          clave: clavesecreta
          tipousuario_id: 2
          estado: 1
    400:
      description: Recurso no encontrado.
    500:
      description: Error en el servidor.
  """
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
    identificador = uuid.uuid4()
    usuario = UsuarioModel(identificador, nombre, usuario, clave, tipousuario_id, estado)
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