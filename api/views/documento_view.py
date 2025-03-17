from flask_restful import Resource
from flask import request, make_response, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import uuid

from api.schemas.documento_schema import DocumentoSchema
from api.entidades.documento_entidade import DocumentoEntidade
from api.services.documento_service import cadastrar_documento, obter_documento_por_id, listar_todos_documentos, deletar_documento

UPLOAD_FOLDER = "uploads/"  # Define o diretório onde os PDFs serão salvos
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Garante que a pasta exista

documento_schema = DocumentoSchema()
documentos_schema = DocumentoSchema(many=True)
class DocumentoView(Resource):
  def get(self, documento_id=None, acao=None):
    if documento_id:
        documento = obter_documento_por_id(documento_id)
        if not documento:
          return make_response(jsonify({"erro": "Documento não encontrado"}), 404)
        
        if acao == "download":
          caminho_arquivo = documento.pdf_data
          if not os.path.exists(caminho_arquivo):
              return make_response(jsonify({"erro": "Arquivo não encontrado no servidor"}), 404)
          return send_file(caminho_arquivo, as_attachment=True, download_name=documento.nome_arquivo, mimetype="application/pdf")
        return make_response(jsonify({"mensagem":"Documento encontrado com sucesso", "documento":documento_schema.dump(documento)}), 200)
    
    documentos = listar_todos_documentos()
    return make_response(jsonify({"mensagem": "Documentos listados com sucesso", "documentos": documentos_schema.dump(documentos)}), 200)

  def post(self):
    documento_schema = DocumentoSchema()

    # Verifica se o arquivo foi enviado
    if 'pdf_data' not in request.files:
      return make_response(jsonify({"erro": "O arquivo PDF é obrigatório"}), 400)
    
    # Extrai os dados
    pdf_data = request.files['pdf_data']
    nome_arquivo = secure_filename(pdf_data.filename.lower())
    data_envio = request.form.get("data_envio")
    usuario_id = request.form.get("usuario_id")

    # Verifica extensão do arquivo
    if not nome_arquivo.endswith(".pdf"):
        return make_response(jsonify({"erro": "Apenas arquivos PDF são permitidos"}), 400)
    
    nome_unico = f"{uuid.uuid4().hex}_{nome_arquivo}"
    caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_unico)
    
    if hasattr(pdf_data, "save"):  # Verifica se o objeto tem o método save()
      try:
          pdf_data.save(caminho_arquivo)  # Salva o arquivo no diretório uploads
      except Exception as e:
          return make_response(jsonify({"erro": f"Erro ao salvar arquivo: {str(e)}"}), 500)
    else:
      return make_response(jsonify({"erro": "Arquivo inválido"}), 400)

    # Cria a entidade de usuário
    novo_documento = DocumentoEntidade(nome_arquivo=nome_unico, data_envio=data_envio, pdf_data=caminho_arquivo, usuario_id=usuario_id)
    # Chama o serviço para cadastrar no banco
    documento_criado = cadastrar_documento(novo_documento)

    # Retorna o documento criado serializado
    return make_response(jsonify({"mensagem": "Documento cadastrado com sucesso", "documento":documento_schema.dump(documento_criado)}), 201)
  
  def delete(self, documento_id):
    documento = obter_documento_por_id(documento_id)

    if not documento:
        return make_response(jsonify({"erro": "Documento não encontrado"}), 404)
    
    caminho_arquivo = documento.pdf_data

    # Exclui o arquivo da pasta /uploads
    if os.path.exists(caminho_arquivo):
        os.remove(caminho_arquivo)
        
    deletar_documento(documento_id)
    
    return make_response(jsonify({"mensagem": "Documento removido com sucesso", "documento": documento_schema.dump(documento)}), 200)