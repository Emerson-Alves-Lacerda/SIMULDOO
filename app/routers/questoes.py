from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from app.connection.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.QuestaoOut])
def list_questoes(nivel: int = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.Questao)
    if nivel:
        query = query.filter(models.Questao.nivel == nivel)
    return query.all()

@router.get("/materias/{id_materia}/", response_model=list[schemas.QuestaoOut])
def questoes_por_materia(id_materia: int, db: Session = Depends(get_db)):
    return db.query(models.Questao).filter(models.Questao.materia == id_materia).all()

@router.post("/", response_model=schemas.QuestaoOut)
def create_questao(questao: schemas.QuestaoCreate, db: Session = Depends(get_db)):
    if questao.nivel not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Nível inválido (deve ser 1, 2 ou 3)")

    existente = db.query(models.Questao).filter(
        models.Questao.enunciado == questao.enunciado,
        models.Questao.materia == questao.materia
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="Questão já existe para essa matéria")

    nova = models.Questao(**questao.dict(), status=False)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova