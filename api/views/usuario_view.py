from flask import jsonify
from flask_openapi3 import Tag, APIBlueprint
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.schemas.usuario_schema import UsuarioSchema, UsuarioValidacao, UsuarioResponse
from api.services.usuario_service import cadastrar_usuario
from api.schemas.error import ErrorSchema

usuario_tag = Tag(name="Usuarios", description="Crud de usuários")

usuario_bp = APIBlueprint(
    "usuarios",
    __name__,
    url_prefix="/usuario",
    abp_tags=[usuario_tag]
)

class UsuarioView:
  @usuario_bp.post(
      "/cadastrar",
      tags=[usuario_tag],
      responses={
          "201": UsuarioResponse,
          "400": ErrorSchema,
          "422": UsuarioValidacao
      }
  )
  def cadastrar(body: UsuarioSchema):
      """
      Cadastra um novo usuário. Requer autenticação JWT.
      """
      try:
          # Identidade extraída do JWT
          usuario_autenticado = get_jwt_identity()
          print(f"Usuário autenticado: {usuario_autenticado}")

          # Cadastra novo usuário
          usuario_cadastrado = cadastrar_usuario(body)

          return jsonify(usuario_cadastrado.model_dump()), 201

      except ValidationError as e:
          return jsonify({
              "erro": "Dados inválidos",
              "mensagem": e.errors()
          }), 422

      except ValueError as e:
          return jsonify({
              "erro": "Erro de validação",
              "mensagem": str(e)
          }), 400

      except Exception as e:
          return jsonify({
              "erro": "Erro interno no servidor",
              "mensagem": str(e)
          }), 500
