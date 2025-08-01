from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.connection.database import SessionLocal
from app.models.models import (
    Usuario,
    Questao,
    AlunoSimulado,
    AlunoQuestao,
    AlunoAlternativa,
)
from app.schemas.schemas import RespostaCreate, RespostaOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RespostaOut)
def registrar_resposta(payload: RespostaCreate, db: Session = Depends(get_db)):
    aluno = db.query(Usuario).get(payload.id_aluno)
    questao = db.query(Questao).get(payload.questao_id)
    simulado_id = payload.simulado_id

    if not aluno or not questao:
        raise HTTPException(status_code=404, detail="Aluno ou questão não encontrados.")

    asim = (
        db.query(AlunoSimulado)
          .filter_by(alunos_id=aluno.id, simulado_id=simulado_id)
          .first()
    )
    if not asim:
        asim = AlunoSimulado(
            alunos_id=aluno.id,
            simulado_id=simulado_id,
            total_acertos=0
        )
        db.add(asim)
        db.commit()
        db.refresh(asim)

    ja_respondida = db.query(AlunoQuestao).filter_by(
        alunos_id=aluno.id, questao_id=questao.id, simulado_id=simulado_id
    ).first()
    if ja_respondida:
        raise HTTPException(status_code=400, detail="Questão já respondida neste simulado.")

    corretas = {a.id for a in questao.alternativas if a.correto}
    marcadas = set(payload.alternativas)
    correta = (corretas == marcadas)

    aq = AlunoQuestao(
        alunos_id=aluno.id,
        questao_id=questao.id,
        simulado_id=simulado_id,
        correto=correta
    )
    db.add(aq)

    for alt_id in payload.alternativas:
        db.add(AlunoAlternativa(alunos_id=aluno.id, alternativa_id=alt_id))

    if correta:
        asim.total_acertos += 1

    db.commit()

    return {
        "aluno": {"id": aluno.id, "nome": aluno.nome},
        "simulado_id": simulado_id,
        "questao_id": questao.id,
        "correta": correta
    }
