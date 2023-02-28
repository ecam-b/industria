from flask import Blueprint, request, jsonify
# model and schema
from models.UsuarioModel import UsuarioModel, UsuarioSchema

for_him = UsuarioSchema()
for_them = UsuarioSchema(many=True)


usuario_bp = Blueprint("usuario", __name__)


@usuario_bp.route("/")
def get_all_usuarios():
  try:
    usuarios = UsuarioModel.query.all()
    result = for_him.dump(usuarios)
    return jsonify(result)
  except Exception as ex:
    return jsonify({"message": str(ex)})