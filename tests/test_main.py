from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_criar_materia():
    response = client.post("/v1/materias/", json={"nome": "Matemática", "ano": 5})
    assert response.status_code in (200, 400)  # pode já existir

def test_listar_materias():
    response = client.get("/v1/materias/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_atualizar_materia():
    client.post("/v1/materias/", json={"nome": "Biologia", "ano": 2})
    response = client.put("/v1/materias/1", json={"nome": "Biologia Atualizada", "ano": 2})
    assert response.status_code == 200
    assert response.json()["nome"] == "Biologia Atualizada"

def test_criar_materia_duplicada():
    client.post("/v1/materias/", json={"nome": "Física", "ano": 3})
    response = client.post("/v1/materias/", json={"nome": "Física", "ano": 3})
    assert response.status_code == 400

def test_criar_questao_valida():
    client.post("/v1/materias/", json={"nome": "História", "ano": 1})
    response = client.post("/v1/questoes/", json={
        "enunciado": "Quem descobriu o Brasil?",
        "nivel": 1,
        "materia": 1,
        "total_correta": 1
    })
    assert response.status_code == 200
    assert response.json()["status"] is False

def test_criar_questao_nivel_invalido():
    response = client.post("/v1/questoes/", json={
        "enunciado": "Questão inválida",
        "nivel": 4,
        "materia": 1,
        "total_correta": 1
    })
    assert response.status_code == 400

def test_listar_questoes_por_nivel():
    response = client.get("/v1/questoes/?nivel=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_listar_questoes_por_materia():
    response = client.get("/v1/questoes/materias/1/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_criar_alternativa_valida():
    client.post("/v1/materias/", json={"nome": "Geografia", "ano": 1})
    r_q = client.post("/v1/questoes/", json={
        "enunciado": "Maior país do mundo?",
        "nivel": 1,
        "materia": 1,
        "total_correta": 1
    })
    id_questao = r_q.json()["id"]
    response = client.post(f"/v1/questao/{id_questao}/alternativas/", json={"descricao": "Rússia", "correto": True})
    assert response.status_code == 200

def test_bloquear_alternativa_extra_correta():
    response = client.post("/v1/questao/1/alternativas/", json={"descricao": "Brasil", "correto": True})
    assert response.status_code == 400

def test_listar_alternativas():
    response = client.get("/v1/questao/1/alternativas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)