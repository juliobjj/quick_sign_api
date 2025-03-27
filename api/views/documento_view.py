from flask import request, jsonify, send_file
from flask_openapi3 import Tag, APIBlueprint
from pydantic import ValidationError

from api.schemas.documento_schema import DocumentoSchema, DocumentoResponseSchema, DocumentoBuscaSchema
from api.services.documento_service import cadastrar_documento, obter_documento_por_id, editar_documento, listar_todos_documentos, deletar_documento, salvar_arquivo, download_arquivo
from api.schemas.error import ErrorSchema

# Definição da tag de documentação
documento_tag = Tag(name="Documentos", description="Gerenciamento de documento")
documento_bp = APIBlueprint("documento", __name__, url_prefix="/documento" ,abp_tags=[documento_tag])

class DocumentoView:
  @documento_bp.put("/editar", summary="Cadastra um novo documento", description="hgskdjh",
                     tags=[documento_tag], responses={"201": DocumentoResponseSchema, "400": ErrorSchema})
  def editar(form: DocumentoSchema):
    try:
      pdf_data = request.files.get("pdf_data")
      id_documento = request.args.get("id_documento")
     
      caminho_arquivo = salvar_arquivo(pdf_data)
       
      documento_schema = DocumentoSchema(nome_arquivo=form.nome_arquivo, pdf_data=caminho_arquivo, status_assinatura=form.status_assinatura) 
      documento = editar_documento(id_documento, documento_schema)

      return jsonify(documento.model_dump()), 201
    
    except Exception as e: 
        return jsonify({"erro": "Erro interno no servidor", "mensagem": str(e)}), 500 
          
  @documento_bp.post("/cadastrar", summary="Cadastra um novo documento", description="hgskdjh",
                     tags=[documento_tag], responses={"201": DocumentoResponseSchema, "400": ErrorSchema})
  def cadastrar(form: DocumentoSchema):
    """
    Cadastra um novo documento
    """
    try: 
      pdf_data = request.files.get("pdf_data")

      if not pdf_data:
                return jsonify({"erro": "Arquivo PDF é obrigatórios"}), 400

      caminho_arquivo = salvar_arquivo(pdf_data)

      documento_schema = DocumentoSchema(nome_arquivo=form.nome_arquivo, pdf_data=caminho_arquivo, status_assinatura=form.status_assinatura) 
      documento_cadastrado = cadastrar_documento(documento_schema)  

      return jsonify(documento_cadastrado.model_dump()), 201
    
    except ValidationError as e:
      return jsonify({"erro": "Dados inválidos", "mensage": str(e)}), 400
    
    except Exception as e: 
       return jsonify({"erro": "Erro interno no servidor", "mensagem": str(e)}), 500
     
  @documento_bp.get("/listar", tags=[documento_tag], responses={"200": DocumentoResponseSchema, "400": ErrorSchema})
  def listar_documentos():
    """Faz a busca por todos os Documentos cadastrados

    Retorna uma representação da listagem de documentos
    """
    documentos = listar_todos_documentos()

    if not documentos: 
      return {"documentos": []}, 200
    else: 
      return jsonify({"documentos": [doc.dict() for doc in documentos]}), 200
  
  @documento_bp.get("/", tags=[documento_tag], responses={"200": DocumentoResponseSchema, "400": ErrorSchema})
  def obter_documento(query: DocumentoBuscaSchema):
    """Faz a busca por um Documento a partir do id do documento

    Retorna uma representação do documento
    """
    try:
      documento = obter_documento_por_id(query.documento_id)
      documento_serializado = DocumentoResponseSchema.from_orm(documento)
      
      return jsonify(documento_serializado.dict()), 200 
    
    except Exception as e:
      return jsonify({"mensagem": str(e)}), 404
    

  @documento_bp.delete("/deletar", tags=[documento_tag], responses={"200": DocumentoResponseSchema, "400": ErrorSchema})
  def deletar_documento(query: DocumentoBuscaSchema): 

    try:
      documento = deletar_documento(query.documento_id)
      documento_serializado = DocumentoResponseSchema.from_orm(documento)
      return jsonify({"documento": documento_serializado.dict()}), 200
    
    except Exception as e:
      return jsonify({"mensagem": str(e)}), 404
    
  @documento_bp.get("/download", tags=[documento_tag])
  def download_documento(query: DocumentoBuscaSchema):
    """Faz a busca por um Documento a partir do id do documento

    Retorna uma representação do documento
    """
    try:
      caminho_arquivo = download_arquivo(query.documento_id)
      
      return send_file(caminho_arquivo, as_attachment=True, mimetype="application/pdf")
    
    except Exception as e:
      return jsonify({"mensagem": str(e)}), 404
    
  


    
  