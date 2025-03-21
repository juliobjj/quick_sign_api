from flask import request, jsonify, redirect
from flask_openapi3 import Tag, APIBlueprint
from pydantic import ValidationError

from api.schemas.usuario_schema import UsuarioSchema, ValidacaoUsuario, UsuarioResponse
from api.services.usuario_service import cadastrar_usuario
from api.schemas.error import ErrorSchema

# Definição da tag de documentação
usuario_tag = Tag(name="Usuários", description="Gerenciamento de usuários")

# Criando o APIBlueprint
usuario_bp = APIBlueprint("usuarios", __name__, url_prefix="/usuario", abp_tags=[usuario_tag])

class UsuarioView:
  # Rota para redirecionar à documentação
  def home():
      """
        Redireciona para a documentação OpenAPI.
      """
      return redirect("/openapi")
  
  @usuario_bp.post("/cadastrar", tags=[usuario_tag], responses={"201": UsuarioResponse, "400": ErrorSchema, "422": ValidacaoUsuario})
  def cadastrar(body: UsuarioSchema):
     """
     Cadastra um novo usuário
     """
     try: 
        # Valida os dados de entrada
        dados = request.get_json(force=True)
        usuario_schema = UsuarioSchema(**dados)

        # Chama o serviço para cadastrar o usuário
        usuario_cadastrado = cadastrar_usuario(usuario_schema)

        # Objeto serializado
        return jsonify(usuario_cadastrado.dict()), 201
     except ValidationError as e:
        #Retorna erro de validação do Schema
        return jsonify({"erro": "Dados inválidos", "mensage": str(e)}), 400
     
     except ValueError as e:
        # Erro usuáriojá existe
        return jsonify({"erro": str(e)}), 400
     
     except Exception as e: 
        #Erro genérico
        return jsonify({"erro": "Erro interno no servidor", "mensagem": str(e)}), 500

