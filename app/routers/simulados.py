from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.connection.database import SessionLocal
from app.models.models import Simulado
from app.schemas.schemas import SimuladoCreate, SimuladoOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SimuladoOut)
def criar_simulado(sim: SimuladoCreate, db: Session = Depends(get_db)):
    nova = Simulado(**sim.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova
