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
(env)$ git clone https://github.com/juliobjj/quick_sign_api.git
```

2. **Criando ambiente virtual:**

```
(env)$ python3 -m venv env
```
Linux/Mac
```
(env)$ source env/bin/activate
```
Windows
```
(env)$ env\Scripts\activate 
```

3. **Instale as dependências:**

Acesse o diretório api
```
(env)$ cd api 
```

```
(env)$ pip install -r requiriments.txt
```

4. **Execute a aplicações:**

Modo padrão:
```
(env)$ flask run 
```
Modo desenvolvimento: 
```
(env)$ flask run --debug
```

## ✅ Verificando a API

- Abra o navegador e acesse:

  http://localhost:5000/health

## 📄 Documentação

- Todos os endpoints seguem padrão REST e retornam dados em formato JSON.
  A documentação interativa estará disponível automaticamente via Swagger em:

  http://localhost:5000/openapi/swagger#/
