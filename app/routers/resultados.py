from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.connection.database import SessionLocal
from app.models.models import Usuario, Simulado, AlunoSimulado, AlunoQuestao, Alternativa, AlunoAlternativa, Questao

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET /v1/simulados/resultados
@router.get("/resultados", summary="Listar resultados de todos os alunos e seus simulados")
def listar_resultados(db: Session = Depends(get_db)):
    output = []
    for aluno in db.query(Usuario).all():
        simulados_data = []
        # Busca por cada simulado que o aluno participou
        sim_rels = db.query(AlunoSimulado).filter_by(alunos_id=aluno.id).all()
        for sim_rel in sim_rels:
            sim = db.query(Simulado).get(sim_rel.simulado_id)
            if not sim:
                continue
            # Busca questões respondidas neste simulado
            q_rels = db.query(AlunoQuestao).filter_by(
                alunos_id=aluno.id,
                simulado_id=sim.id
            ).all()
            questoes_list = []
            for qrel in q_rels:
                quest = db.query(Questao).get(qrel.questao_id)
                if not quest:
                    continue
                alts = db.query(Alternativa).filter_by(questao_id=quest.id).all()
                marcadas = db.query(AlunoAlternativa).filter_by(
                    alunos_id=aluno.id
                ).join(Alternativa).filter(Alternativa.questao_id == quest.id).all()
                questoes_list.append({
                    "nome": quest.enunciado,
                    "alternativas": [
                        {"id": a.id, "descricao": a.descricao, "correta": a.correta}
                        for a in alts
                    ],
                    "resposta": [
                        {"id": ma.alternativa_id}
                        for ma in marcadas
                    ],
                    "correto": qrel.correto
                })
            simulados_data.append({
                "id": sim.id,
                "nome": sim.nome,
                "total_acertos": sim_rel.total_acertos,
                "total_questoes": len(questoes_list),
                "percentual": (sim_rel.total_acertos / len(questoes_list) * 100) if questoes_list else 0,
                "questoes": questoes_list
            })
        output.append({
            "aluno": {"nome": aluno.nome, "matricula": aluno.matricula},
            "simulados": simulados_data
        })
    return output

# GET /v1/simulados/resultados/aluno/{id_aluno}
@router.get("/resultados/aluno/{id_aluno}", summary="Listar resultados de um aluno específico")
def resultado_por_aluno(id_aluno: int, db: Session = Depends(get_db)):
    aluno = db.query(Usuario).get(id_aluno)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    simulados_data = []
    sim_rels = db.query(AlunoSimulado).filter_by(alunos_id=aluno.id).all()
    for sim_rel in sim_rels:
        sim = db.query(Simulado).get(sim_rel.simulado_id)
        if not sim:
            continue
        q_rels = db.query(AlunoQuestao).filter_by(
            alunos_id=aluno.id,
            simulado_id=sim.id
        ).all()
        questoes_list = []
        for qrel in q_rels:
            quest = db.query(Questao).get(qrel.questao_id)
            alts = db.query(Alternativa).filter_by(questao_id=quest.id).all()
            marcadas = db.query(AlunoAlternativa).filter_by(
                alunos_id=aluno.id
            ).join(Alternativa).filter(Alternativa.questao_id == quest.id).all()
            questoes_list.append({
                "nome": quest.enunciado,
                "alternativas": [
                    {"id": a.id, "descricao": a.descricao, "correta": a.correta}
                    for a in alts
                ],
                "resposta": [
                    {"id": ma.alternativa_id}
                    for ma in marcadas
                ],
                "correto": qrel.correto
            })
        simulados_data.append({
            "id": sim.id,
            "nome": sim.nome,
            "total_acertos": sim_rel.total_acertos,
            "total_questoes": len(questoes_list),
            "percentual": (sim_rel.total_acertos / len(questoes_list) * 100) if questoes_list else 0,
            "questoes": questoes_list
        })
    return {
        "aluno": {"nome": aluno.nome, "matricula": aluno.matricula},
        "simulados": simulados_data
    }
