from flask import Blueprint, request, jsonify
# database
from database.db import db
# token_required
from token_required import token_required
# models and schemas
from models.ChorroModel import ChorroModel, ChorroSchema

for_him = ChorroSchema()
for_them = ChorroSchema(many=True)

chorro_bp = Blueprint("chorro", __name__)


@chorro_bp.route("/")
def gell_all_chorro():
  try:
    chorros = ChorroModel.query.all()
    result = for_them.dump(chorros)
    return jsonify(result)
  except Exception as ex:
    return jsonify({"message": str(ex)}), 400