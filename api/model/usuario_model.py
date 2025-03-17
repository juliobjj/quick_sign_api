from passlib.hash import pbkdf2_sha256
from sqlalchemy import Column, Integer, String

from ..base import db 

class Usuario(db.Model):
    __tablename__ = 'usuario'   

    id = db.Column("pk_usuario", db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(90), nullable=False)
    senha = db.Column(db.String(255), nullable=False)   

    # documento = db.relationship("DocumentoModel", back_populates="usuario")
    
    def __init__(self, nome:str, email:str, senha:str):
        self.nome = nome
        self.email = email
        self.senha = senha  

    def cripto_senha(self):
        self.senha = pbkdf2_sha256(self.senha)