from ..model.usuario_model import Usuario
from api.base import db  # Agora usamos o db do Flask-SQLAlchemy

def cadastrar_usuario(usuario):
    # Cria a instância do usuário para salvar no banco
    usuario_bd = Usuario(nome=usuario.nome, email=usuario.email, senha=usuario.senha)

    # Adiciona e confirma a transação no banco
    db.session.add(usuario_bd)
    db.session.commit()

    # Retorna o usuário criado em formato de dicionário
    return usuario_bd
