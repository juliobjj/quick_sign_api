from ..base import db 

class DocumentoModel(db.Model):
    __tablename__ = 'documento'   

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_arquivo = db.Column(db.String(40), nullable=False)
    data_envio = db.Column(db.String(90), nullable=False)
    pdf_data = db.Column(db.String, nullable=False)  # Armazena o PDF como BLOB
    usuario_id = db.Column(db.Integer, nullable=False)
    
    def __init__(self, nome_arquivo:str, data_envio:str, pdf_data:str, usuario_id:int):
        self.nome_arquivo = nome_arquivo
        self.data_envio = data_envio
        self.pdf_data = pdf_data 
        self.usuario_id = usuario_id 



