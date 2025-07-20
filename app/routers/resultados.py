from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.connection.database import SessionLocal
from app.models.models import Usuario, Simulado, AlunoSimulado, AlunoQuestao, Alternativa, AlunoAlternativa, Questao
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/resultados")
def listar_resultados(db: Session = Depends(get_db)):
    alunos = db.query(Usuario).all()
    resposta = []

    for aluno in alunos:
        simulados = []
        relacoes = db.query(AlunoSimulado).filter_by(alunos_id=aluno.id).all()

        for rel in relacoes:
            simulado = db.query(Simulado).get(rel.simulado_id)
            questoes_rel = db.query(AlunoQuestao).filter_by(alunos_id=aluno.id).all()
            questoes_json = []

            for qrel in questoes_rel:
                questao = db.query(Questao).get(qrel.questao_id)
                alternativas = db.query(Alternativa).filter_by(questao_id=questao.id).all()
                marcadas = db.query(AlunoAlternativa).join(Alternativa).filter(
                    AlunoAlternativa.alunos_id == aluno.id,
                    Alternativa.questao_id == questao.id
                ).all()

                questoes_json.append({
                    "enunciado": questao.enunciado,
                    "alternativas": [{"id": a.id, "descricao": a.descricao, "correta": a.correto} for a in alternativas],
                    "resposta": [{"id": a.alternativa_id} for a in marcadas],
                    "correto": qrel.correto
                })

            simulados.append({
                "id": simulado.id,
                "nome": simulado.nome,
                "total_acertos": rel.total_acertos,
                "questoes": questoes_json
            })

        resposta.append({
            "aluno": {"nome": aluno.nome, "matricula": aluno.matricula},
            "simulados": simulados
        })

    return resposta

@router.get("/resultados/aluno/{id}")
def resultado_por_aluno(id: int, db: Session = Depends(get_db)):
    aluno = db.query(Usuario).get(id)
    if not aluno:
        return {"erro": "Aluno não encontrado"}

    simulados = []
    relacoes = db.query(AlunoSimulado).filter_by(alunos_id=aluno.id).all()

    for rel in relacoes:
        simulado = db.query(Simulado).get(rel.simulado_id)
        questoes_rel = db.query(AlunoQuestao).filter_by(alunos_id=aluno.id).all()
        questoes_json = []

        for qrel in questoes_rel:
            questao = db.query(Questao).get(qrel.questao_id)
            alternativas = db.query(Alternativa).filter_by(questao_id=questao.id).all()
            marcadas = db.query(AlunoAlternativa).join(Alternativa).filter(
                AlunoAlternativa.alunos_id == aluno.id,
                Alternativa.questao_id == questao.id
            ).all()

            questoes_json.append({
                "enunciado": questao.enunciado,
                "alternativas": [{"id": a.id, "descricao": a.descricao, "correta": a.correto} for a in alternativas],
                "resposta": [{"id": a.alternativa_id} for a in marcadas],
                "correto": qrel.correto
            })

        simulados.append({
            "id": simulado.id,
            "nome": simulado.nome,
            "total_acertos": rel.total_acertos,
            "questoes": questoes_json
        })

    return {
        "aluno": {"nome": aluno.nome, "matricula": aluno.matricula},
        "simulados": simulados
    }

