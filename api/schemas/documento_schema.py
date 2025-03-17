from api.extension import ma
from ..model import documento_model
from marshmallow import fields

class DocumentoSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = documento_model.DocumentoModel
    load_instance = True
    fields = ("id", "nome_arquivo", "data_envio", "pdf_data", "usuario_id")

  nome_arquivo = fields.String(required=False)
  data_envio = fields.String(required=False)
  pdf_data = fields.String(required=True)
  usuario_id = fields.Integer(required=True)
  



  
