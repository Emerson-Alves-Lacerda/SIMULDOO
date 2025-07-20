from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.connection.database import SessionLocal
from app.models import *
from app.models.models import AlunoSimulado, AlunoQuestao, AlunoAlternativa, Questao, Usuario
from app.schemas.schemas import RespostaCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/")
def registrar_resposta(payload: RespostaCreate, db: Session = Depends(get_db)):
    aluno = db.query(Usuario).get(payload.id_aluno)
    questao = db.query(Questao).get(payload.questao_id)

    if not aluno or not questao:
        raise HTTPException(404, "Aluno ou questão não encontrados.")

    # Determinar simulado associado à questão (por enquanto hardcoded se não houver)
    simulado_id = 1  # TODO: definir por relação no futuro

    # Verifica se já existe AlunoSimulado
    asim = db.query(AlunoSimulado).filter_by(alunos_id=aluno.id, simulado_id=simulado_id).first()
    if not asim:
        asim = AlunoSimulado(alunos_id=aluno.id, simulado_id=simulado_id, total_acertos=0)
        db.add(asim)
        db.commit()

    # Verifica se já respondeu essa questão
    if db.query(AlunoQuestao).filter_by(alunos_id=aluno.id, questao_id=questao.id).first():
        raise HTTPException(400, "Questão já respondida.")

    # Verifica se está correta
    corretas = set(a.id for a in questao.alternativas if a.correto)
    marcadas = set(payload.alternativas)

    correta = corretas == marcadas

    # Registra AlunoQuestao
    q = AlunoQuestao(alunos_id=aluno.id, questao_id=questao.id, correto=correta)
    db.add(q)

    # Registra AlunoAlternativas
    for alt_id in marcadas:
        db.add(AlunoAlternativa(alunos_id=aluno.id, alternativa_id=alt_id))

    # Se correta, incrementa total_acertos
    if correta:
        asim.total_acertos += 1

    db.commit()
    return {"status": "Resposta registrada", "correta": correta}
