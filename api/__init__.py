from flask_openapi3 import OpenAPI, Info
from flask import jsonify
from flask_jwt_extended import JWTManager
from .base import db, jwt
from flask_cors import CORS

def create_app():
    info = Info(title="API de Quick Sign", version="1.0.0")
    app = OpenAPI(__name__, info=info)  # Inicializando o OpenAPI
    CORS(app)

    app.config.from_object("config.Config")
    db.init_app(app)
    jwt.init_app(app)

    @jwt.unauthorized_loader
    def unauthorized_callback(msg):
        return jsonify({"erro": "Token não fornecido ou malformado", "mensagem": msg}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(msg):
        return jsonify({"erro": "Token inválido", "mensagem": msg}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"erro": "Token expirado", "mensagem": "Faça login novamente"}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"erro": "Token revogado", "mensagem": "Este token não é mais válido"}), 401

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(jwt_header, jwt_payload):
        return jsonify({"erro": "Token precisa ser atualizado", "mensagem": "Envie um token fresco"}), 401


    # Importando os Blueprints para registrar as rotas
    from api.views.assinatura_views import assinatura_bp
    app.register_api(assinatura_bp) 

    from .views.documento_view import documento_bp
    app.register_api(documento_bp)  

    from .views.health_view import health_bp
    app.register_api(health_bp)

    from .views.usuario_view import usuario_bp
    app.register_api(usuario_bp)

    from .views.auth_view import auth_bp
    app.register_api(auth_bp)

    # Criar o banco dentro do contexto
    with app.app_context():
        db.create_all()

    return app