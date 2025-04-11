from ..schemas.assinatura_schema import AssinaturaSchema, AssinaturaResponse
from ..model.assinatura_model import AssinaturaModel
from ..base import db 
import fitz
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import re

def cadastrar_assinatura(assinatura_schema: AssinaturaSchema):
    """
    Cadastra uma nova assinatura no banco de dados
    """
    cpf_limpo = limpar_cpf(assinatura_schema.cpf)

    nova_assinatura = AssinaturaModel(
        nome=assinatura_schema.nome.strip(),
        cpf=cpf_limpo,
        data_assinatura= datetime.now(),
        id_documento=assinatura_schema.id_documento
    )
    try:
         # Salva no banco de dados
        db.session.add(nova_assinatura)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise RuntimeError("Erro ao salvar assinatura no banco de dados")

    # Retorna o usuário criado em formato de dicionário
    return AssinaturaResponse.from_orm(nova_assinatura)

def pode_assinar(id_documento: int):
    """
    Verifica se o documento já foi assinado.
    """
    resultado = AssinaturaModel.query.get(id_documento)

    if resultado:
        return False
    return True

def assinar_pdf(pdf_caminho: str, nome: str, cpf: str):
    """
    Adiciona assinatura visual no rodapé do PDF.
    """ 
    # Abrir o PDF
    doc = fitz.open(pdf_caminho)

    # Dados para assinatura
    cpf_formatado = formatar_cpf(cpf)
    texto_assinatura = f"Assinado por: {nome.strip()} - CPF: {cpf_formatado} em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    
    for pagina in doc:
        altura = pagina.rect.height  # Apenas pegamos a altura, já que a largura não é necessária

        # Adicionar assinatura no rodapé
        pagina.insert_text((50, altura - 50), texto_assinatura, fontsize=10, color=(0, 0, 0))

    # Salvar o PDF assinado
    doc.save(pdf_caminho, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()

def limpar_cpf(cpf: str) -> str:
    """
    Remove qualquer caractere não numérico do CPF.
    """
    return re.sub(r'\D', '', cpf)

def formatar_cpf(cpf: str) -> str:
    """
    Formata o CPF para o padrão xxx.xxx.xxx-xx.
    """
    cpf_numerico = re.sub(r'\D', '', cpf)
    if len(cpf_numerico) != 11:
        raise ValueError("CPF inválido para formatação")
    return f"{cpf_numerico[:3]}.{cpf_numerico[3:6]}.{cpf_numerico[6:9]}-{cpf_numerico[9:]}"
