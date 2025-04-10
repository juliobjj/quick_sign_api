from ..model.documento_model import DocumentoModel
from ..schemas.documento_schema import DocumentoSchema, DocumentoResponseSchema
from ..base import db 

from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError
import datetime
import os
import uuid

UPLOAD_FOLDER = "uploads/"

class DocumentoNaoEncontradoError(Exception):
    pass

def cadastrar_documento(documento_schema: DocumentoSchema):
  """
  Cadastra um novo documento
  """
  novo_documento = DocumentoModel(
    nome_arquivo=documento_schema.nome_arquivo,
    data_envio=datetime.datetime.now(),
    pdf_data=documento_schema.pdf_data,
    status_assinatura=documento_schema.status_assinatura
  )

  try:
    db.session.add(novo_documento)
    db.session.commit()
  except SQLAlchemyError:
    db.session.rollback()
    raise

  return DocumentoResponseSchema.from_orm(novo_documento)

def editar_documento(documento_id: int, documento_schema: DocumentoSchema):
  """
  Edita um documento
  """
  documento = obter_documento_por_id(documento_id)
  if not documento: 
    raise ValueError("Documento não encontrado")
  
  documento.nome_arquivo = documento_schema.nome_arquivo
  documento.pdf_data = documento_schema.pdf_data
  documento.data_envio = datetime.datetime.now()
  documento.status_assinatura = documento_schema.status_assinatura

  try:
    db.session.commit()
  except SQLAlchemyError:
    db.session.rollback()
    raise

  return DocumentoResponseSchema.from_orm(documento)

def obter_documento_por_id(documento_id: int):
  documento = DocumentoModel.query.get(documento_id)
  if not documento:
    raise DocumentoNaoEncontradoError("Documento não encontrado")
  return documento


def listar_todos_documentos():
  documentos = DocumentoModel.query.all()
  documentos_serializados = [DocumentoResponseSchema.from_orm(doc) for doc in documentos]

  return documentos_serializados

def deletar_documento(documento_id: int):
  documento = obter_documento_por_id(documento_id)
  try:
      db.session.delete(documento)
      db.session.commit()
  except SQLAlchemyError:
      db.session.rollback()
      raise
  return documento

def salvar_arquivo(arquivo):
  """
  Salva um arquivo na pasta local definida.

  :param arquivo: Arquivo enviado pelo usuário (objeto FileStorage)
  :param nome_arquivo: Nome do arquivo a ser salvo
  :return: Caminho completo do arquivo salvo
  """

  # Garante que o diretório de destino existe
  os.makedirs(UPLOAD_FOLDER, exist_ok=True)

  # Assegura um nome seguro para o arquivo
  nome_arquivo_seguro = secure_filename(arquivo.filename.lower())
  nome_unico = f"{uuid.uuid4().hex}_{nome_arquivo_seguro}"
  caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_unico)

  # Salva o arquivo no diretório
  arquivo.save(caminho_arquivo)

  return caminho_arquivo

def download_arquivo(documento_id):
  documento = obter_documento_por_id(documento_id)

  caminho_arquivo = documento.pdf_data

  return caminho_arquivo
