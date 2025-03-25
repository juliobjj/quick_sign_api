from ..schemas.assinatura_schema import AssinaturaSchema, AssinaturaResponse
from ..model.assinatura_model import AssinaturaModel
from ..base import db 
import fitz
import datetime

def listar_assinaturas():
    """
    Retorna uma lista de usuários cadastrados
    """
    assinaturas = AssinaturaModel.query.all()
    return [AssinaturaSchema.from_orm(assinatura).dict() for assinatura in assinaturas]

def cadastrar_assinatura(assinatura_schema: AssinaturaSchema):
    """
    Cadastra uma nova assinatura
    """
    nova_assinatura = AssinaturaModel(
        nome=assinatura_schema.nome,
        cpf=assinatura_schema.cpf,
        id_documento=assinatura_schema.id_documento
    )
    
     # Salva no banco de dados
    db.session.add(nova_assinatura)
    db.session.commit()

    assinatura_serializado = AssinaturaResponse.from_orm(nova_assinatura)

    # Retorna o usuário criado em formato de dicionário
    return assinatura_serializado

def assinar_pdf(pdf_caminho, nome, cpf):
    # Abrir o PDF
    doc = fitz.open(pdf_caminho)
    
    # Dados para assinatura
    texto_assinatura = f"Assinado por: {nome} - CPF: {cpf} em {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}"
    
    for pagina in doc:
        altura = pagina.rect.height  # Apenas pegamos a altura, já que a largura não é necessária
        # Adicionar assinatura no rodapé
        pagina.insert_text((50, altura - 50), texto_assinatura, fontsize=10, color=(0, 0, 0))

    # Salvar o PDF assinado
    doc.save(pdf_caminho, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()
    print(f"Documento assinado salvo em: {pdf_caminho}")
