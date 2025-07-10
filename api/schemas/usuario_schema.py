from pydantic import BaseModel, Field
from api.model.assinatura_model import AssinaturaModel
from typing import List
from datetime import datetime

class UsuarioSchema(BaseModel):
    email: str = Field(..., title="Email", description="Email do usuário")
    password_hash: str = Field(..., title="Senha", description="Senha do usuário")

class UsuarioResponse(BaseModel):
    id: int
    email: str 
    password_hash: str 
    created_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class UsuarioValidacao(BaseModel):
    """
        Retorna mensagem caso assinatura cadastre sem o nome
    """
    mesage: UsuarioSchema
