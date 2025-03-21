from pydantic import BaseModel, EmailStr, Field
from api.model.usuario_model import Usuario
from typing import List

from pydantic import BaseModel, EmailStr, Field

class UsuarioSchema(BaseModel):
    nome: str = Field(..., title="Nome", description="Nome do usuário")
    email: EmailStr = Field(..., title="Email", description="E-mail do usuário")
    senha: str = Field(..., title="Senha", description="Senha do usuário", min_length=6)

class UsuarioResponse(BaseModel):
    id: int
    nome: str 
    email: EmailStr 
    senha: str

    class Config:
        from_attributes = True

class UsuarioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    nome: str = "Teste"

class ValidacaoUsuario(BaseModel):
    """
        Retorna mensagem caso usuário cadastre sem o nome
    """
    mesage: UsuarioSchema


def apresenta_produtos(usuario: List[Usuario]):
    """ Retorna uma representação do usuário seguindo o schema definido em
        UsuarioSchema.
    """
    result = []
    for usuario in usuario:
        result.append({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "senha": usuario.senha,
        })

    return {"usuario": result}