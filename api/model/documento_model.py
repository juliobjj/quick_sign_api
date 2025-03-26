from ..base import db 
from sqlalchemy.orm import relationship
from .assinatura_model import AssinaturaModel

class DocumentoModel(db.Model):
    __tablename__ = 'documento'   

    id = db.Column("pk_documento", db.Integer, primary_key=True, autoincrement=True)
    nome_arquivo = db.Column(db.String(40), nullable=False)
    data_envio = db.Column(db.DateTime, nullable=False)
    pdf_data = db.Column(db.String, nullable=False)

    assinaturas = relationship("AssinaturaModel", back_populates="documento", cascade="all, delete-orphan")

    def __init__(self, nome_arquivo:str, data_envio:str, pdf_data:str):
        self.nome_arquivo = nome_arquivo
        self.data_envio = data_envio
        self.pdf_data = pdf_data 

    def adiciona_assinatura(self, assinatura:AssinaturaModel):
        """ Adiciona um novo comentário ao Produto
        """
        self.assinatura.append(assinatura)




