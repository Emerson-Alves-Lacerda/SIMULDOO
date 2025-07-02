from pydantic import BaseModel
from typing import Optional

class MateriaBase(BaseModel):
    nome: str
    ano: int
    descricao: Optional[str] = None

class MateriaCreate(MateriaBase):
    pass

class MateriaOut(MateriaBase):
    id: int
    class Config:
        orm_mode = True

class QuestaoBase(BaseModel):
    enunciado: str
    nivel: int
    materia: int
    total_correta: int

class QuestaoCreate(QuestaoBase):
    pass

class QuestaoOut(QuestaoBase):
    id: int
    status: bool
    class Config:
        orm_mode = True

class AlternativaBase(BaseModel):
    descricao: str
    correto: bool

class AlternativaCreate(AlternativaBase):
    pass

class AlternativaOut(AlternativaBase):
    id: int
    class Config:
        orm_mode = True
