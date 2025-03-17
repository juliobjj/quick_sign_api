from flask_restful import Resource
from flask import request, make_response, jsonify, send_file
from io import BytesIO
import mimetypes

from api.schemas.documento_schema import DocumentoSchema
from api.entidades.documento_entidade import DocumentoEntidade
from api.services.documento_service import cadastrar_documento
from api.services.documento_service import obter_documento_por_id 

class DocumentoView(Resource):

  def get(self, documento_id):
    documento = obter_documento_por_id(documento_id)

    if not documento:
       return make_response(jsonify({"erro": "Documento não encontrado"}), 404)
    
    if not documento.pdf_data:
            return make_response(jsonify({"erro": "Arquivo PDF não encontrado"}), 404)

    return send_file(
            BytesIO(documento.pdf_data),  # Converte os dados binários para um arquivo em memória
            mimetype="application/pdf",
            as_attachment=True,
            download_name=documento.nome_arquivo)  # Define o nome do arquivo no download

  def post(self):
    documento_schema = DocumentoSchema()

    # Verifica se o arquivo foi enviado
    if 'pdf_data' not in request.files:
      return make_response(jsonify({"erro": "O arquivo PDF é obrigatório"}), 400)
    
    # Extrai os dados
    pdf_data = request.files['pdf_data']
    nome_arquivo = pdf_data.filename.lower()
    data_envio = request.form.get("data_envio")
    usuario_id = request.form.get("usuario_id")

    # Verifica extensão do arquivo
    if not nome_arquivo.endswith(".pdf"):
        return make_response(jsonify({"erro": "Apenas arquivos PDF são permitidos"}), 400)
    
    # Verifica o MIME type do arquivo
    mime_type = mimetypes.guess_type(nome_arquivo)[0]
    if mime_type != "application/pdf":
      return make_response(jsonify({"erro": "O arquivo enviado não é um PDF válido"}), 400)

    if not nome_arquivo or not usuario_id:
           return make_response(jsonify({"erro": "Nome do arquivo e usuário são obrigatórios"}), 400)
    
    try: 
        pdf_data = pdf_data.read()
    except Exception as e:
        return make_response(jsonify({"erro": f"Erro ao processar arquivo: {str(e)}"}), 500)
    
    # Lê os dados binários do arquivo
    #pdf_data = pdf_data.read()

    # Cria a entidade de usuário
    novo_documento = DocumentoEntidade(nome_arquivo=nome_arquivo, data_envio=data_envio, pdf_data=pdf_data, usuario_id=usuario_id)

    # Chama o serviço para cadastrar no banco
    cadastrar_documento(novo_documento)

    # Retorna o documento criado serializado
    return make_response(jsonify({"sucsess": "Arquivo cadastrado"}), 201)
  



