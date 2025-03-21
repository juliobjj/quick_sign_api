from pydantic import BaseModel, Field
from typing import List

class DocumentoSchema(BaseModel):
  nome_arquivo: str = Field(..., title="Nome", description="Nome do arquivo" )
  data_envio: str = Field(..., title="Data", description="Data que o arquivo foi enviado")
  pdf_data: str = Field(..., title="Path", description="Caminho do arquivo salvo")

class DocumenteResponseSchema(BaseModel):
  id: int
  nome_arquivo: str
  data_envio: str
  pdf_data: str

  class Config:
        from_attributes = True

class DocumentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    nome: str = "Teste"

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
  



  
