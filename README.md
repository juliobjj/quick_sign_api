# 🚀 Minha API

Esta API faz parte do sistema **Quick Sign**, e foi desenvolvida com o objetivo de gerenciar **documentos eletrônicos** e **assinaturas digitais.**

## 📌 O que essa API faz?

Ela permite:

📄 Cadastrar e listar documentos que precisam de assinatura.

✍️ Registrar assinaturas digitais vinculadas a documentos específicos.

---

## 📦 Requisitos

Antes de executar o projeto, você precisará:

- Python 3.7+
- `virtualenv` (recomendado)
- Bibliotecas listadas em `requirements.txt`

---

## ⚙️ Como executar

1. **Clone o repositório:**

- git clone https://github.com/juliobjj/quick_doc.git
- cd api

2. **Criando ambiente virtual:**

- python -m venv env
- source env/bin/activate # Linux/Mac
- env\Scripts\activate # Windows

3. **Intale as dependências:**

- pip install -r requirements.txt

4. **Execute a aplicações:**

- flask run #Modo padrão
- flask run --debug #Modo desenvolvimento

## ✅ Verificando a API

- Abra o navegador e acesse:

- http://localhost:5000/health

## 📄 Documentação

- Todos os endpoints seguem padrão REST e retornam dados em formato JSON.
  A documentação interativa estará disponível automaticamente via Swagger em:

- http://localhost:5000/openapi/swagger#/
