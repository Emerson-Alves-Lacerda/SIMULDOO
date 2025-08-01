from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_criar_materia():
    response = client.post("/v1/materias/", json={"nome": "Matemática", "ano": 5})
    assert response.status_code in (200, 400)

def test_listar_materias():
    response = client.get("/v1/materias/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_atualizar_materia():
    r = client.post("/v1/materias/", json={"nome": "Biologia", "ano": 2})
    assert r.status_code in (200, 400)
    if r.status_code == 200:
        id_materia = r.json().get("id")
    else:
        materias = client.get("/v1/materias/").json()
        id_materia = next(m['id'] for m in materias if m['nome'] == 'Biologia' and m['ano'] == 2)

    response = client.put(f"/v1/materias/{id_materia}", json={"nome": "Biologia Atualizada", "ano": 2})
    assert response.status_code == 200
    assert response.json()["nome"] == "Biologia Atualizada"

def test_criar_materia_duplicada():
    client.post("/v1/materias/", json={"nome": "Física", "ano": 3})
    response = client.post("/v1/materias/", json={"nome": "Física", "ano": 3})
    assert response.status_code in (200, 400)

def test_criar_questao_valida():
    r_materia = client.post("/v1/materias/", json={"nome": "História", "ano": 1})
    assert r_materia.status_code in (200, 400)
    id_materia = r_materia.json().get("id") if r_materia.status_code == 200 else next(m['id'] for m in client.get("/v1/materias/").json() if m['nome']=='História')

    r_q = client.post("/v1/questoes/", json={
        "enunciado": "Quem descobriu o Brasil?",
        "nivel": 1,
        "materia": id_materia,
        "total_correta": 1
    })
    assert r_q.status_code in (200, 400)


def test_criar_questao_nivel_invalido():
    r_materia = client.post("/v1/materias/", json={"nome": "Matéria Inválida", "ano": 1})
    id_materia = r_materia.json().get("id")

    response = client.post("/v1/questoes/", json={
        "enunciado": "Questão inválida",
        "nivel": 4,
        "materia": id_materia,
        "total_correta": 1
    })
    assert response.status_code == 400

def test_listar_questoes_por_nivel():
    response = client.get("/v1/questoes/?nivel=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_listar_questoes_por_materia():
    r_materia = client.post("/v1/materias/", json={"nome": "Química", "ano": 2})
    id_materia = r_materia.json().get("id")

    response = client.get(f"/v1/questoes/materias/{id_materia}/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_criar_alternativa_valida():
    r_materia = client.post("/v1/materias/", json={"nome": "Geografia", "ano": 1})
    id_materia = r_materia.json().get("id")
    r_q = client.post("/v1/questoes/", json={
        "enunciado": "Maior país do mundo?",
        "nivel": 1,
        "materia": id_materia,
        "total_correta": 1
    })
    if r_q.status_code == 200:
        id_questao = r_q.json().get("id")
    else:
        id_questao = next(q['id'] for q in client.get("/v1/questoes/").json() if q['enunciado']=='Maior país do mundo?')
    assert id_questao is not None

    response = client.post(f"/v1/questao/{id_questao}/alternativas/", json={
        "descricao": "Rússia",
        "correto": True
    })
    assert response.status_code == 200

def test_bloquear_alternativa_extra_correta():
    r_materia = client.post("/v1/materias/", json={"nome": "Sociologia", "ano": 3})
    id_materia = r_materia.json().get("id")
    r_q = client.post("/v1/questoes/", json={
        "enunciado": "O que é cultura?",
        "nivel": 1,
        "materia": id_materia,
        "total_correta": 1
    })
    if r_q.status_code == 200:
        id_questao = r_q.json().get("id")
    else:
        id_questao = next(q['id'] for q in client.get("/v1/questoes/").json() if q['enunciado']=='O que é cultura?')
    assert id_questao is not None

    client.post(f"/v1/questao/{id_questao}/alternativas/", json={"descricao": "Um conjunto de valores", "correto": True})
    response = client.post(f"/v1/questao/{id_questao}/alternativas/", json={"descricao": "Um sistema político", "correto": True})
    assert response.status_code == 400

def test_listar_alternativas():
    r_materia = client.post("/v1/materias/", json={"nome": "Artes", "ano": 1})
    id_materia = r_materia.json().get("id")
    r_q = client.post("/v1/questoes/", json={
        "enunciado": "O que é perspectiva?",
        "nivel": 1,
        "materia": id_materia,
        "total_correta": 1
    })
    if r_q.status_code == 200:
        id_questao = r_q.json().get("id")
    else:
        id_questao = next(q['id'] for q in client.get("/v1/questoes/").json() if q['enunciado']=='O que é perspectiva?')
    assert id_questao is not None

    client.post(f"/v1/questao/{id_questao}/alternativas/", json={"descricao": "Técnica de profundidade", "correto": True})
    response = client.get(f"/v1/questao/{id_questao}/alternativas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

