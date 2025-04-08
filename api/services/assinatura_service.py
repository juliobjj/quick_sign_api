from ..schemas.assinatura_schema import AssinaturaSchema, AssinaturaResponse
from ..model.assinatura_model import AssinaturaModel
from ..base import db 
import fitz
from datetime import datetime
import re

def cadastrar_assinatura(assinatura_schema: AssinaturaSchema):
    """
    Cadastra uma nova assinatura
    """
    cpf_limpo = limpar_cpf(assinatura_schema.cpf)

    nova_assinatura = AssinaturaModel(
        nome=assinatura_schema.nome,
        cpf=cpf_limpo,
        data_assinatura= datetime.now(),
        id_documento=assinatura_schema.id_documento
    )
    
     # Salva no banco de dados
    db.session.add(nova_assinatura)
    db.session.commit()

    assinatura_serializado = AssinaturaResponse.from_orm(nova_assinatura)

    # Retorna o usuário criado em formato de dicionário
    return assinatura_serializado

def pode_assinar(id_documento):
    resultado = AssinaturaModel.query.get(id_documento)

    if resultado:
        return False
    return True

def limpar_cpf(cpf):
    return re.sub(r'\D', '', cpf)

def assinar_pdf(pdf_caminho, nome, cpf):
    limpar_cpf(cpf)

    # Abrir o PDF
    doc = fitz.open(pdf_caminho)
    # Dados para assinatura
    texto_assinatura = f"Assinado por: {nome} - CPF: {cpf} em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    
    for pagina in doc:
        altura = pagina.rect.height  # Apenas pegamos a altura, já que a largura não é necessária
        # Adicionar assinatura no rodapé
        pagina.insert_text((50, altura - 50), texto_assinatura, fontsize=10, color=(0, 0, 0))

    # Salvar o PDF assinado
    doc.save(pdf_caminho, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()
