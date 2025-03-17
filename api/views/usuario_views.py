from flask_restful import Resource
from flask import request, make_response, jsonify

from api.schemas.usuario_schema import UsuarioSchema
from api.entidades.usuario_entidade import UsuarioEntidade
from api.services.usuario_service import cadastrar_usuario

class UsuarioList(Resource):
  def get(self):
    return jsonify({"mensagem": "Olá, mundo!"})

  def post(self):
    usuario_schema = UsuarioSchema()

    # Valida os dados recebidos
    erros = usuario_schema.validate(request.json)
    if erros:
        return make_response(jsonify(erros), 400)

    # Extrai os dados
    nome = request.json.get("nome")
    email = request.json.get("email")
    senha = request.json.get("senha")

    # Cria a entidade de usuário
    novo_usuario = UsuarioEntidade(nome=nome, email=email, senha=senha)

    print(novo_usuario)
    # Chama o serviço para cadastrar no banco
    usuario_criado = cadastrar_usuario(novo_usuario)
    print(usuario_schema.jsonify(usuario_criado))

    # Retorna o usuário criado serializado
    return make_response(usuario_schema.jsonify(usuario_criado), 201)



