from ..schemas.usuario_schema import UsuarioSchema, UsuarioResponse
from ..model.usuario_model import UsuarioModel
from ..base import db 
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

def cadastrar_usuario(usuario_schema: UsuarioSchema):
    """
    Cadastra um novo usuário no banco de dados
    """

    novo_usuario = UsuarioModel.create_with_password(
        email=usuario_schema.email.strip(),
        password=usuario_schema.password_hash.strip(),
    )

    try:
         # Salva no banco de dados
        db.session.add(novo_usuario)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise RuntimeError("Erro ao salvar assinatura no banco de dados")

    # Retorna o usuário criado em formato de dicionário
    return UsuarioResponse.from_orm(novo_usuario)
