from ..base import db 
from sqlalchemy.orm import relationship

class DocumentoModel(db.Model):
    __tablename__ = 'documento'   

    id = db.Column("pk_documento", db.Integer, primary_key=True, autoincrement=True)
    nome_arquivo = db.Column(db.String(40), nullable=False)
    data_envio = db.Column(db.DateTime, nullable=False)
    pdf_data = db.Column(db.String, nullable=False)
    status_assinatura = db.Column(db.Boolean, default=False, nullable=False)

    assinaturas = relationship("AssinaturaModel", back_populates="documento", cascade="all, delete-orphan")

    def __init__(self, nome_arquivo:str, data_envio:str, pdf_data:str, status_assinatura:bool):
        self.nome_arquivo = nome_arquivo
        self.data_envio = data_envio
        self.pdf_data = pdf_data 
        self.status_assinatura = status_assinatura 





