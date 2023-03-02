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
# token_required
from token_required import token_required
# model and schema
from models.UsuarioModel import UsuarioModel, UsuarioSchema

for_him = UsuarioSchema()
for_them = UsuarioSchema(many=True)


usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/login", methods=["POST"])
def login():
  """
  Login para obtener un token
  Metodo para obtener el token de acceso al sistema
  ---
  tags:
  - Ingreso
  parameters:
    - name: login
      in: body
      description: Datos para el login
      required: true
      schema: 
        type: object
        properties:
          usuario: 
            type: string
            description: Nombre de usuario.
          clave: 
            type: string
            description: Clave de usuario.
        example:
          usuario: "ecas"
          clave: "1234"
  responses:
    200:
      description: OK
      schema: 
        type: object
        properties:
          token:
            type: string
            description: Token de acceso al sistema.
        example:
          token: pbkdf2:sha256:260000$inK2V9k7ajJzDyTo$a8794ced796c4e26d8481d3062bf2b6f8c395eb7ae230c5627162314e3c6a7ab
    400:
      description: Usuario o contraseña incorrectos.
    500:
      description: Error en el servidor.
  """
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
    return jsonify({"message": "Contraseña incorrecta."}), 400
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400

@usuario_bp.route("/")
@token_required
def get_all_usuarios(usuario_actual):
  """
  Obtener todos los usuario
  Obtener todos los usuario registrados en la base de datos
  ---
  tags:
  - Usuario
  parameters:
    - name: x-access-token
      in: header
      type: string
      required: true
      description: Token de autentificación.
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
@token_required
def get_usuario(usuario_actual, id):
  """
  Obtener un usuario especifico
  Obtener un usuario especifico registrados en la base de datos
  ---
  tags:
  - Usuario
  parameters:
    - name: x-access-token
      in: header
      type: string
      required: true
      description: Token de autentificación.
    - name: id
      in: path
      type: integer
      required: true
      description: Id del usuario.
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
    usuario = UsuarioModel.query.get(id)
    if usuario == None:
      return jsonify({"message": "Elemento no encontrado."}), 400
    return for_him.jsonify(usuario)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400


@usuario_bp.route("/add", methods=["POST"])
def add_usuario():
  """
  Agregar un usuario
  Agregar un usuario en la base de datos
  ---
  tags:
  - Usuario
  parameters:
    - name: usuario
      in: body
      required: true
      description: Usuario a agregar.
      schema:
        type: object
        properties:
          nombre:
            type: string
            description: Nombre de usuario
          usuario:
            type: string
            description: Usuario de usuario
          clave:
            type: string
            description: Clave de usuario
          tipousuario_id:
            type: integer
            description: Tipo de usuario
          estado:
            type: integer
            description: Estado de usuario
        example:
          nombre: Usuario Mayor
          usuario: UserMatch
          clave: "1234"
          tipousuario_id: 1
          estado: 1
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
    data = request.json
    nombre = data["nombre"]
    usuario = data["usuario"]
    clave = generate_password_hash(data["clave"])
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
@token_required
def update_usuario(usuario_actual, id):
  """
  Actualizar un usuario
  Actualizar un usuario en la base de datos
  ---
  tags:
  - Usuario
  parameters:
    - name: x-access-token
      in: header
      type: string
      required: true
      description: Token de autentificación.
    - name: id
      in: path
      type: integer
      required: true
      description: Id del usuario.
    - name: usuario
      in: body
      required: true
      description: Usuario a actualizar.
      schema:
        type: object
        properties:
          nombre:
            type: string
            description: Nombre de usuario
          usuario:
            type: string
            description: Usuario de usuario
          clave:
            type: string
            description: Clave de usuario
          tipousuario_id:
            type: integer
            description: Tipo de usuario
          estado:
            type: integer
            description: Estado de usuario
        example:
          nombre: Usuario Mayor
          usuario: UserMatch
          clave: "1234"
          tipousuario_id: 1
          estado: 1
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
    data = request.json
    usuario = UsuarioModel.query.get(id)
    if usuario == None:
      return jsonify({"message": "Elemento no encontrado."}), 400
    if data["nombre"]:
      usuario.nombre = data["nombre"]
    if data["usuario"]:
      usuario.usuario = data["usuario"]
    if data["clave"]:
      usuario.clave = generate_password_hash(data["clave"])
    if data["tipousuario_id"]:
      usuario.tipousuario_id = data["tipousuario_id"]
    if data["estado"]:
      usuario.estado = data["estado"]
    db.session.commit()
    return for_him.jsonify(usuario)
  except Exception as ex:
    return jsonify({"message", str(ex)}), 400
  

@usuario_bp.route("/delete/<id>", methods=["DELETE"])
@token_required
def delete_usuario(usuario_actual, id):
  """
  Eliminar un usuario
  Eliminar un usuario en la base de datos
  ---
  tags:
  - Usuario
  parameters:
    - name: x-access-token
      in: header
      type: string
      required: true
      description: Token de autentificación.
    - name: id
      in: path
      type: integer
      required: true
      description: Id del usuario.
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
    usuario = UsuarioModel.query.get(id)
    if usuario == None:
      return jsonify({"message": "Elemento no encontrado"}), 400
    db.session.delete(usuario)
    db.session.commit()
    return for_him.jsonify(usuario)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400