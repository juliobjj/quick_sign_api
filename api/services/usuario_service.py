from ..schemas.usuario_schema import UsuarioSchema, UsuarioResponse
from .. model.usuario_model import Usuario
from ..base import db 

def listar_usuarios():
    """
    Retorna uma lista de usuários cadastrados
    """
    usuarios = Usuario.query.all()
    return [UsuarioSchema.from_orm(usuario).dict() for usuario in usuarios]

def cadastrar_usuario(usuario_schema: UsuarioSchema):

    """
    Cadastra um novo usuário
    """

    # Verifica se o usuário já existe
    usuario_existente = Usuario.query.filter_by(email=usuario_schema.email).first()
    if usuario_existente:
        raise ValueError("Usuário já cadastrado com este e-mail")
    
    novo_usuario = Usuario(
        nome=usuario_schema.nome,
        email=usuario_schema.email,
        senha=usuario_schema.senha
    )

     # Salva no banco de dados
    db.session.add(novo_usuario)
    db.session.commit()

    usuario_serializado = UsuarioResponse.from_orm(novo_usuario)

    # Retorna o usuário criado em formato de dicionário
    return usuario_serializado
