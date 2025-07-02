from fastapi import APIRouter, HTTPException, Depends
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

@router.get("/{id_questao}/alternativas/", response_model=list[schemas.AlternativaOut])
def listar_alternativas(id_questao: int, db: Session = Depends(get_db)):
    return db.query(models.Alternativa).filter(models.Alternativa.questao == id_questao).all()

@router.post("/{id_questao}/alternativas/", response_model=schemas.AlternativaOut)
def criar_alternativa(id_questao: int, alt: schemas.AlternativaCreate, db: Session = Depends(get_db)):
    questao = db.query(models.Questao).get(id_questao)
    if not questao:
        raise HTTPException(status_code=404, detail="Questão não encontrada")

    if alt.correto:
        corretas = db.query(models.Alternativa).filter_by(questao=id_questao, correto=True).count()
        if corretas >= questao.total_correta:
            raise HTTPException(status_code=400, detail="Já existem alternativas corretas suficientes")

    nova = models.Alternativa(questao=id_questao, **alt.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova
