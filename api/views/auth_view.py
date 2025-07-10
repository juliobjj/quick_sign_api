from flask import Blueprint, request, jsonify
from flask_pydantic import validate
from flask_openapi3 import Tag, APIBlueprint
from sqlalchemy.orm import Session
from api.schemas.auth_schema import LoginRequest, TokenResponse
from api.services.auth_service import AuthService
from ..base import db 

# Definição da tag de documentação
auth_tag = Tag(name="Autenticação", description="Gerenciamento de assinaturas")
# Criando o APIBlueprint
auth_bp = APIBlueprint("autenticação", __name__, url_prefix="/auth", abp_tags=[auth_tag])

@auth_bp.post("/login", tags=[auth_tag], responses={"200": TokenResponse, "401": {"description": "Credenciais inválidas"}})
@validate()
def login(body: LoginRequest):
    service = AuthService(db.session)
    token = service.authenticate_user(body.email, body.password)
    db.session.close()

    if not token:
        return jsonify({"error": "Credenciais inválidas"}), 401

    return TokenResponse(access_token=token).model_dump(), 200
