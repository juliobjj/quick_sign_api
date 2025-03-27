from flask import request, jsonify, redirect
from flask_openapi3 import Tag, APIBlueprint
from pydantic import ValidationError

from api.schemas.assinatura_schema import AssinaturaSchema, ValidacaoAssinatura, AssinaturaResponse
from api.schemas.documento_schema import DocumentoSchema
from api.services.assinatura_service import cadastrar_assinatura, assinar_pdf, pode_assinar
from api.services.documento_service import obter_documento_por_id, editar_documento
from api.schemas.error import ErrorSchema

# Definição da tag de documentação
assinatura_tag = Tag(name="Assinaturas", description="Gerenciamento de assinaturas")
# Criando o APIBlueprint
assinatura_bp = APIBlueprint("assinaturas", __name__, url_prefix="/assinatura", abp_tags=[assinatura_tag])

class AssinaturaView:
  @assinatura_bp.post("/cadastrar", tags=[assinatura_tag], responses={"201": AssinaturaResponse, "400": ErrorSchema, "422": ValidacaoAssinatura})
  def cadastrar(body: AssinaturaSchema):
     """
     Cadastra um novo assinatura
     """
     try: 
        # Valida os dados de entrada
        dados = request.get_json(force=True)
        assinatura_schema = AssinaturaSchema(**dados)

        if pode_assinar(body.id_documento):
         # Chama o serviço para cadastrar o assinatura
         assinatura_cadastrado = cadastrar_assinatura(assinatura_schema)

         buscar_documento = obter_documento_por_id(body.id_documento)

         assinar_pdf(buscar_documento.pdf_data, body.nome, body.cpf)

         documento_schema = DocumentoSchema(
            nome_arquivo=buscar_documento.nome_arquivo,
            pdf_data=buscar_documento.pdf_data,
            status_assinatura=True
         ) 

         editar_documento(body.id_documento, documento_schema)

         # Objeto serializado
         return jsonify(assinatura_cadastrado.dict()), 201
        else:
           return jsonify({"mesage": "PDF já assinado"}), 400
     except ValidationError as e:
        #Retorna erro de validação do Schema
        return jsonify({"erro": "Dados inválidos", "mensage": str(e)}), 400
     
     except ValueError as e:
        # Erro usuáriojá existe
        return jsonify({"erro": str(e)}), 400
     
     except Exception as e: 
        #Erro genérico
        return jsonify({"erro": "Erro interno no servidor", "mensagem": str(e)}), 500

