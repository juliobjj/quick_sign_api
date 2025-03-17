from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from .extension import ma
from .base import db 

def create_app():
  app = Flask(__name__)
 
  app.config.from_object('config.Config')

  db.init_app(app)
  api = Api(app)
  
  # Inicializa extensões
  ma.init_app(app)

  # Importa e adiciona os recursos da API
  from .views.usuario_views import UsuarioList
  api.add_resource(UsuarioList, '/usuario')

  from .views.documento_view import DocumentoView
  api.add_resource(DocumentoView, "/documento", "/documento/<int:documento_id>")

  # Cria o banco dentro do contexto
  with app.app_context():
      db.create_all()

  return app


