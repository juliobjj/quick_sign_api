from flask import request, jsonify, send_file
from flask_openapi3 import Tag, APIBlueprint
from pydantic import ValidationError
from flask_jwt_extended import jwt_required
import os

from api.schemas.documento_schema import DocumentoSchema, DocumentoResponseSchema, DocumentoBuscaSchema
from api.services.documento_service import (
    cadastrar_documento,
    obter_documento_por_id,
    editar_documento,
    listar_todos_documentos,
    deletar_documento,
    salvar_arquivo,
    obter_documento_por_id,
    DocumentoNaoEncontradoError
)
from api.schemas.error import ErrorSchema

# Tag de documentação
documento_tag = Tag(name="Documentos", description="Gerenciamento de documento")
documento_bp = APIBlueprint("documento", __name__, url_prefix="/documento" ,abp_tags=[documento_tag])

class DocumentoView:
  @documento_bp.post("/cadastrar", tags=[documento_tag], security=[{"BearerAuth": []}], responses={"201": DocumentoResponseSchema,"400": ErrorSchema})
  @jwt_required()
  def cadastrar(form: DocumentoSchema):
    """
    Cadastra um novo documento
    """
    try: 
      pdf_data = request.files.get("pdf_data")

      if not pdf_data or not pdf_data.filename.lower().endswith(".pdf"):
        return {"erro": "Apenas arquivos PDF são permitidos"}, 400

      caminho_arquivo = salvar_arquivo(pdf_data)

      documento_schema = DocumentoSchema(nome_arquivo=form.nome_arquivo, pdf_data=caminho_arquivo, status_assinatura=form.status_assinatura) 
      documento_cadastrado = cadastrar_documento(documento_schema)  

      return jsonify(documento_cadastrado.model_dump()), 201
    
    except ValidationError as e:
      return jsonify({"erro": "Dados inválidos", "mensagem": str(e)}), 400
    
    except Exception as e: 
       return jsonify({"erro": "Erro interno no servidor", "mensagem": str(e)}), 500

  @documento_bp.put("/editar", tags=[documento_tag], security=[{"BearerAuth": []}], responses={"201": DocumentoResponseSchema, "400": ErrorSchema})
  def editar(form: DocumentoSchema, query: DocumentoBuscaSchema):
    """
    Edita um documento a partir de um id
    """
    try:
      pdf_data = request.files.get("pdf_data")
     
      caminho_arquivo = salvar_arquivo(pdf_data)
      print(caminho_arquivo)
       
      documento_schema = DocumentoSchema(nome_arquivo=form.nome_arquivo, pdf_data=caminho_arquivo, status_assinatura=form.status_assinatura) 
      documento = editar_documento(query.documento_id, documento_schema)

      return jsonify(documento.model_dump()), 201
    
    except Exception as e: 
        return jsonify({"erro": "Erro interno no servidor", "mensagem": str(e)}), 500 
     
  @documento_bp.get("/listar", tags=[documento_tag], security=[{"BearerAuth": []}], responses={"200": DocumentoResponseSchema, "400": ErrorSchema})
  @jwt_required()
  def listar_documentos():
    """Faz a busca por todos os Documentos cadastrados

    Retorna uma representação da listagem de documentos
    """
    documentos = listar_todos_documentos()

    if not documentos: 
      return {"documentos": []}, 200
    else: 
      return jsonify({"documentos": [doc.model_dump() for doc in documentos]}), 200
  
  @documento_bp.get("/obter", tags=[documento_tag], security=[{"BearerAuth": []}],  responses={"200": DocumentoResponseSchema, "400": ErrorSchema})
  @jwt_required()
  def obter_documento(query: DocumentoBuscaSchema):
    """Faz a busca por um Documento a partir do id do documento

    Retorna uma representação do documento
    """
    try:
      documento = obter_documento_por_id(query.documento_id)
      documento_serializado = DocumentoResponseSchema.from_orm(documento)
      
      return jsonify(documento_serializado.model_dump()), 200 
    
    except Exception as e:
      return jsonify({"mensagem": str(e)}), 404
    

  @documento_bp.delete("/deletar", tags=[documento_tag], security=[{"BearerAuth": []}], responses={"200": DocumentoResponseSchema, "400": ErrorSchema})
  @jwt_required()
  def deletar_documento(query: DocumentoBuscaSchema): 
    """
    Deleta um documento
    """
    try:
      documento = deletar_documento(query.documento_id)
      documento_serializado = DocumentoResponseSchema.from_orm(documento)
      return jsonify({"documento": documento_serializado.model_dump()}), 200
    
    except Exception as e:
      return jsonify({"mensagem": str(e)}), 404
    
  @documento_bp.get("/download", tags=[documento_tag], security=[{"BearerAuth": []}])
  @jwt_required()
  def download_documento(query: DocumentoBuscaSchema):
    """Faz a busca por um Documento a partir do id do documento

    Retorna uma representação do documento
    """
    try:
      documento = obter_documento_por_id(query.documento_id)
      caminho_arquivo = documento.pdf_data

      if not os.path.exists(caminho_arquivo):
        return jsonify({"mensagem": "Arquivo não encontrado"}), 404
      
      return send_file(caminho_arquivo, as_attachment=True, mimetype="application/pdf")
    except DocumentoNaoEncontradoError as e:
      return jsonify({"mensagem": str(e)}), 404
    except Exception as e:
      return jsonify({"mensagem": str(e)}), 404
    
  


    
  