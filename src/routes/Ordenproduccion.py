from flask import Blueprint, request, jsonify
# database
from database.db import db
# token_required
from token_required import token_required
# models and schemas
from models.OrdenproduccionModel import OrdenproduccionModel, OrdenproduccionSchema

for_him = OrdenproduccionSchema()
for_them = OrdenproduccionSchema(many=True)

ordenproduccion_bp = Blueprint("ordenproduccion", __name__)


@ordenproduccion_bp.route("/")
def gell_all_ordenproduccion():
  try:
    ordenproducciones = OrdenproduccionModel.query.all()
    result = for_them.dump(ordenproducciones)
    return jsonify(result)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400