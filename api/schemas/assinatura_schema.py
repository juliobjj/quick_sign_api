from pydantic import BaseModel, Field
from api.model.assinatura_model import AssinaturaModel
from typing import List
from datetime import datetime

class AssinaturaSchema(BaseModel):
    nome: str = Field(..., title="Nome", description="Nome do usuário")
    cpf: str = Field(..., title="CPF", description="CPF do usuário", min_length=11)
    id_documento: int = Field(..., title="CPF", description="Id do documento")

class AssinaturaResponse(BaseModel):
    id: int
    nome: str 
    cpf: str 
    data_assinatura: datetime
    id_documento: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class AssinaturaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    nome: str = "Teste"

class ValidacaoAssinatura(BaseModel):
    """
        Retorna mensagem caso assinatura cadastre sem o nome
    """
    mesage: AssinaturaSchema
