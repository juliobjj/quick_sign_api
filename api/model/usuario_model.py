from ..base import db 

class Usuario(db.Model):
    __tablename__ = 'usuario'   

    id = db.Column("pk_usuario", db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(90), nullable=False)
    senha = db.Column(db.String(255), nullable=False)   

    def __init__(self, nome:str, email:str, senha:str):
        self.nome = nome
        self.email = email
        self.senha = senha  
