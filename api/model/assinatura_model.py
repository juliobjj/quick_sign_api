from ..base import db 
from sqlalchemy.orm import relationship
import datetime

class AssinaturaModel(db.Model):
    __tablename__ = 'assinatura'   

    id = db.Column("pk_assinatura", db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(40), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    id_documento = db.Column(db.Integer, db.ForeignKey("documento.pk_documento"), nullable=False)
    data_assinatura = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    documento = relationship("DocumentoModel", back_populates="assinaturas")

    __table_args__ = (db.UniqueConstraint("id_documento", name="uq_documento_assinado"),)

    def __init__(self, nome:str, cpf:str, data_assinatura:datetime, id_documento:int):
        self.nome = nome
        self.cpf = cpf
        self.data_assinatura = data_assinatura
        self.id_documento = id_documento
