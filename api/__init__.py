from flask_openapi3 import OpenAPI, Info

from .base import db 


info = Info(title="API de Quick Sign", version="1.0.0")

def create_app():
    app = OpenAPI(__name__, info=info)  # Inicializando o OpenAPI

    app.config.from_object("config.Config")
    db.init_app(app)

    # Importando os Blueprints para registrar a rota /usuario
    from api.views.usuario_views import usuario_bp
    app.register_api(usuario_bp) 

    #from .views.documento_view import DocumentoView
    #app.register_api(DocumentoView)  

    # Criar o banco dentro do contexto
    with app.app_context():
        db.create_all()

    return app