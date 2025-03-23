from flask_openapi3 import OpenAPI, Info
from flask import Flask
from .base import db 
from flask_cors import CORS

def create_app():
    info = Info(title="API de Quick Sign", version="1.0.0")
    app = OpenAPI(__name__, info=info)  # Inicializando o OpenAPI
    CORS(app)

    app.config.from_object("config.Config")
    db.init_app(app)

    # Importando os Blueprints para registrar as rotas
    from api.views.usuario_views import usuario_bp
    app.register_api(usuario_bp) 

    from .views.documento_view import documento_bp
    app.register_api(documento_bp)  

    # Criar o banco dentro do contexto
    with app.app_context():
        db.create_all()

    return app