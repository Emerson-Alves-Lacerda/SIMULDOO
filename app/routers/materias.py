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

@router.get("/", response_model=list[schemas.MateriaOut])
def list_materias(ano: int = Query(None), db: Session = Depends(get_db)):
    if ano:
        return db.query(models.Materia).filter(models.Materia.ano == ano).all()
    return db.query(models.Materia).all()

@router.post("/", response_model=schemas.MateriaOut)
def criar_materia(materia: schemas.MateriaCreate, db: Session = Depends(get_db)):
    existente = db.query(models.Materia).filter_by(nome=materia.nome, ano=materia.ano).first()
    if existente:
        return existente
    nova = models.Materia(**materia.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@router.put("/{id_materia}", response_model=schemas.MateriaOut)
def update_materia(id_materia: int, materia: schemas.MateriaCreate, db: Session = Depends(get_db)):
    db_materia = db.get(models.Materia, id_materia)
    if not db_materia:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")
    db_materia.nome = materia.nome
    db_materia.ano = materia.ano
    db_materia.descricao = materia.descricao
    db.commit()
    db.refresh(db_materia)
    return db_materia