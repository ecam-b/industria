from flask import request, jsonify
from functools import wraps
import jwt
# config 
from config import SECRET_KEY
# model 
from models.UsuarioModel import UsuarioModel

def token_required(func):
    @wraps(func)
    def decorador(*args,**kwargs):
      token = None

      if "x-access-token" in request.headers:
        token = request.headers["x-access-token"]

      if not token: 
         return jsonify({"message": "Token no encontrado. Inicie sesión para obtener un nuevo token."}), 400
      
      try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        usuario_actual = UsuarioModel.query.filter_by(id_privado = data["id_privado"]).first()
      except:
        return jsonify({"message": "Token no valido. Inicie sesión nuevamente."}), 400
      return func(usuario_actual, *args, **kwargs)
    return decorador
