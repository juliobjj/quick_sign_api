from ..model.documento_model import DocumentoModel
from ..schemas.documento_schema import DocumentoSchema, DocumenteResponseSchema, DocumentoListagemSchema
from ..services.storage_service import StorageService
from ..base import db 

from werkzeug.utils import secure_filename
import datetime
import os

UPLOAD_FOLDER = "uploads/documentos"

def cadastrar_documento(documento_schema: DocumentoSchema):
  """
  Cadastra um novo documento
  """
  
  novo_documento = DocumentoModel(
    nome_arquivo=documento_schema.nome_arquivo,
    data_envio=str(datetime.datetime.now()),
    pdf_data=documento_schema.pdf_data
  )

  db.session.add(novo_documento)
  db.session.commit()

  documento_serializado = DocumenteResponseSchema.from_orm(novo_documento)

  # Retorna o documento criado em formato de dicionário
  return documento_serializado

def obter_documento_por_id(documento_id):
  return DocumentoModel.query.filter_by(id=documento_id).first()

def listar_todos_documentos():
  documentos = DocumentoModel.query.all()
  return DocumentoListagemSchema.from_orm(documentos)

def deletar_documento(documento_id):
  documento = DocumentoModel.query.get(documento_id)
  if documento:
    db.session.delete(documento)
    db.session.commit()

def salvar_arquivo(arquivo, nome_arquivo):
  os.makedirs(UPLOAD_FOLDER, exist_ok=True)

  nome_arquivo_seguro = secure_filename(nome_arquivo)
  caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_arquivo_seguro)

  arquivo.save(caminho_arquivo)

  return caminho_arquivo

