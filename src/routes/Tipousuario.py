from flask import Blueprint, request, jsonify
# database
from database.db import db
# token_required
from token_required import token_required
# models and schemas
from models.TipousuarioModel import TipousuarioModel, TipousuarioSchema

for_him = TipousuarioSchema()
for_them = TipousuarioSchema(many=True)

tipousuario_bp = Blueprint("tipousuario", __name__)

@tipousuario_bp.route("/")
@token_required
def gell_all_tipousuarios(usuario_actual):
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
@token_required
def get_tipousuario(usuario_actual, id):
  """
  Obtener un tipo de especifico
  Obtener un tipo de especifico registrados en la base de datos
  ---
  tags:
  - Tipousuario
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
    tipousuario = TipousuarioModel.query.get(id)
    if tipousuario == None:
      return jsonify({"message": "Elemento no encontrado."}), 400
    return for_him.jsonify(tipousuario)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400
  

@tipousuario_bp.route("/add", methods=["POST"])
@token_required
def add_tipousuario(usuario_actual):
  """
  Agregar un tipo de
  Agregar un tipo de en la base de datos
  ---
  tags:
  - Tipousuario
  parameters:
    - name: usuario
      in: body
      required: true
      description: Usuario a agregar.
      schema:
        type: object
        properties:
          descripcion:
            type: string
            description: Descripción de usuario
        example:
          id: 3
          descripcion: user
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
    data = request.json
    descripcion = data["descripcion"]
    tipousuario = TipousuarioModel(descripcion)
    db.session.add(tipousuario)
    db.session.commit()
    return for_him.jsonify(tipousuario)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400
  

@tipousuario_bp.route("/update/<id>", methods=["PUT"])
@token_required
def update_tipousuario(usuario_actual, id):
  """
  Actualizar un tipo de
  Actualizar un tipo de en la base de datos
  ---
  tags:
  - Tipousuario
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
          descripcion:
            type: string
            description: Descripción de usuario
        example:
          id: 3
          descripcion: user
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
@token_required
def delete_tipousuario(usuario_actual, id):
  """
  Eliminar un tipo de
  Eliminar un tipo de en la base de datos
  ---
  tags:
  - Tipousuario
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
    tipousuario = TipousuarioModel.query.get(id)
    if tipousuario == None:
      return jsonify({"message": "Elemento no encontrado."}), 400
    db.session.delete(tipousuario)
    db.session.commit()
    return for_him.jsonify(tipousuario)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400