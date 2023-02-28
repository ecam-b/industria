from flask import Blueprint, request, jsonify

# models and schemas
from models.TipousuarioModel import TipousuarioModel, TipousuarioSchema

for_him = TipousuarioSchema()
for_them = TipousuarioSchema(many=True)

tipousuario_bp = Blueprint("tipousuario", __name__)

@tipousuario_bp.route("/")
def gell_all_tipousuario():
  try:
    tipousuarios = TipousuarioModel.query.all()
    result = for_them.dump(tipousuarios)
    return jsonify(result)
  except Exception as ex:
    return jsonify({"message": str(ex)})