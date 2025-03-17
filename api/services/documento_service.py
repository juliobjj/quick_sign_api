from ..model.documento_model import DocumentoModel
from api.base import db  # Agora usamos o db do Flask-SQLAlchemy

import datetime

def cadastrar_documento(documento):
  # Cria a instância do usuário para salvar no banco
  documento_bd = DocumentoModel( nome_arquivo=documento.nome_arquivo,
      data_envio=str(datetime.datetime.now()),
      pdf_data=documento.pdf_data,
      usuario_id=documento.usuario_id)

  # Adiciona e confirma a transação no banco
  db.session.add(documento_bd)
  db.session.commit()

  # Retorna o usuário criado em formato de dicionário
  return documento_bd

def obter_documento_por_id(documento_id):
  return DocumentoModel.query.filter_by(id=documento_id).first()

def listar_todos_documentos():
  return DocumentoModel.query.all()

def deletar_documento(documento_id):
  documento = DocumentoModel.query.get(documento_id)
  if documento:
    db.session.delete(documento)
    db.session.commit()
