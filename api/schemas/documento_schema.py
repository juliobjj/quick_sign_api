from pydantic import BaseModel, validator
from typing import List, Annotated
from flask_openapi3 import FileStorage
from datetime import datetime
from werkzeug.datastructures import FileStorage as WerkzeugFile

class DocumentoSchema(BaseModel):
  nome_arquivo: str = "Meu primeiro arquivo"
  pdf_data:  Annotated[FileStorage, "formData"] 

class DocumentoResponseSchema(BaseModel):
  id: int
  nome_arquivo: str
  data_envio: datetime
  pdf_data: str
  status_assinatura: bool

  class Config:
    from_attributes = True

class DocumentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    documento_id: int = 1

class DocumentoListagemSchema(BaseModel):
    """
    Define como uma listagem de documentos será retornada
    """
    documentos: List[DocumentoSchema]

class ValidacaoDocumento(BaseModel):
    """
    Retorna mensagem caso usuário cadastre sem o nome
    """
    mesage: DocumentoSchema
  



  
