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
def create_materia(materia: schemas.MateriaCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Materia).filter(
        models.Materia.nome == materia.nome,
        models.Materia.ano == materia.ano
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Matéria com esse nome e ano já existe")
    nova = models.Materia(**materia.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@router.put("/{id_materia}", response_model=schemas.MateriaOut)
def update_materia(id_materia: int, materia: schemas.MateriaCreate, db: Session = Depends(get_db)):
    db_materia = db.query(models.Materia).get(id_materia)
    if not db_materia:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")
    db_materia.nome = materia.nome
    db_materia.ano = materia.ano
    db_materia.descricao = materia.descricao
    db.commit()
    db.refresh(db_materia)
    return db_materia
