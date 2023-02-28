from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# config
from config import DATABASE_URI_CONNECTION, SECRET_KEY

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLAlchemy(app)
Marshmallow(app)




if __name__ == "__main__":
  app.run(debug=True)