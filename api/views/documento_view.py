from flask import request, make_response, jsonify, send_file
from flask_openapi3 import Tag, APIBlueprint
from pydantic import ValidationError
from werkzeug.utils import secure_filename
import os
import uuid

from api.schemas.documento_schema import DocumentoSchema, ValidacaoDocumento, DocumenteResponseSchema, DocumentoListagemSchema
from api.services.documento_service import cadastrar_documento, obter_documento_por_id, listar_todos_documentos, deletar_documento
from api.services.documento_service import StorageService
from api.schemas.error import ErrorSchema

UPLOAD_FOLDER = "uploads/"  # Define o diretório onde os PDFs serão salvos
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Garante que a pasta exista

# Definição da tag de documentação
documento_tag = Tag(name="Documentos", description="Gerenciamento de documento")
documento_bp = APIBlueprint("documento", __name__, url_prefix="/documento", abp_tags=[documento_tag])

class DocumentoView:
  @documento_bp.post("/cadastrar", tags=[documento_tag], responses={"201": DocumenteResponseSchema, "400": ErrorSchema})
  def cadastrar():
    """
    Cadastra um novo documento
    """
    try: 
      pdf_data = request.files["pdf_data"]
      nome_arquivo = request.form.get("nome_arquivo")
      data_envio = request.form.get("data_envio")

      caminho_arquivo = StorageService.salvar_arquivo(pdf_data)

      documento_schema = DocumentoSchema(nome_arquivo=nome_arquivo, data_envio=data_envio, pdf_data=caminho_arquivo) 
      documento_cadastrado = cadastrar_documento(documento_schema)  

      return jsonify(documento_cadastrado.dict()), 201
    
    except ValidationError as e:
      return jsonify({"erro": "Dados inválidos", "mensage": str(e)}), 400
  
    except ValueError as e:
      # Erro documento já existe
      return jsonify({"erro": str(e)}), 400
     
    except Exception as e: 
      # Erro genérico
      return jsonify({"erro": "Erro interno no servidor", "mensagem": str(e)}), 500
     
  @documento_bp.get("/listar", tags=[documento_tag], responses={"200": DocumentoListagemSchema, "400": ErrorSchema})
  def listar():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos
    """
    documentos = listar_todos_documentos()

    return jsonify(documentos.dict()), 200


    
  