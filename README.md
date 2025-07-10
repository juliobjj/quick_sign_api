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

```
git clone https://github.com/juliobjj/quick_sign_api.git
```

```
cd api
```

É necessário criar um arquivo .env na past api e gerar uma chave secreta para assinar os tokens.

Exemplo (.env):

```
JWT_SECRET_KEY=sua_chave

```

2. **Criando ambiente virtual:**

```
python3 -m venv .venv
```

Linux/Mac

```
source .venv/bin/activate
```

Windows

```
.venv\Scripts\activate
```

3. **Instale as dependências:**

```
pip install -r requirements.txt
```

4. **Execute a aplicações:**

Modo padrão:

```
flask run
```

Modo desenvolvimento:

```
(env)$ flask run --debug
```

## ✅ Verificando a API

- Abra o navegador e acesse:

  http://localhost:5000/health

## 🧪 Testes unitários

- 1. Cadastre um usuário de teste pelo Swagger: /usuario/cadastrar
- 2. Altere o arquivo de teste e insira as informações cadastradas
- 3. Execute o comando: pytest

## 📄 Documentação

- Todos os endpoints seguem padrão REST e retornam dados em formato JSON.
  A documentação interativa estará disponível automaticamente via Swagger em:

  http://localhost:5000/openapi/swagger#/
