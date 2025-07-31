from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.connection.database import SessionLocal
from app.models.models import AlunoSimulado, AlunoQuestao, AlunoAlternativa, Questao, Usuario
from app.schemas.schemas import RespostaCreate, RespostaOut


router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/", response_model=RespostaOut)
def registrar_resposta(payload: RespostaCreate, db: Session = Depends(get_db)):
    aluno = db.query(Usuario).get(payload.id_aluno)
    questao = db.query(Questao).get(payload.questao_id)
    simulado_id = payload.simulado_id   # <-- agora vem do usuário

    if not aluno or not questao:
        raise HTTPException(404, "Aluno ou questão não encontrados.")

    # Verifica (ou cria) registro de simulado para esse aluno
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
    # ... resto da lógica permanece ...
    # no final, devolva algo como:
    return {
        "aluno": {"id": aluno.id, "nome": aluno.nome},
        "simulado_id": simulado_id,
        "questao_id": questao.id,
        "corretas": correta
    }