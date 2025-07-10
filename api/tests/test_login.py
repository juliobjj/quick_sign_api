import pytest
from api.app import app 

@pytest.fixture
def client():
    #app = create_app()
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'chave_teste'
    with app.test_client() as client:
        yield client

def test_login_success(client):
    resposta = client.post('/auth/login', json={
        "email": "julio.rodrigues@hotmail.com",
        "password": "1234"
    })
    assert resposta.status_code == 200
    assert 'access_token' in resposta.json
    assert isinstance(resposta.json['access_token'], str)

def test_login_senha_incorreta(client):
    resposta = client.post("/auth/login", json={"email": "julio.rodrigues@hotmail.com", "password": "123"})
    assert resposta.status_code == 401
    assert "error" in resposta.json

def test_login_dados_incompletos(client):
    resposta = client.post("/auth/login", json={"email": "julio.rodrigues@hotmail.com"})
    assert resposta.status_code == 422
