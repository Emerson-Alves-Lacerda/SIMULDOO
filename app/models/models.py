from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.connection.database import Base

class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    ano = Column(Integer)
    descricao = Column(String, nullable=True)

    __table_args__ = (
        # Restrição única: nome + ano
        {'sqlite_autoincrement': True},
    )

class Questao(Base):
    __tablename__ = "questoes"

    id = Column(Integer, primary_key=True, index=True)
    enunciado = Column(String)
    nivel = Column(Integer)
    materia = Column(Integer, ForeignKey("materias.id"))
    total_correta = Column(Integer)
    status = Column(Boolean, default=False)

class Alternativa(Base):
    __tablename__ = "alternativas"

    id = Column(Integer, primary_key=True, index=True)
    questao = Column(Integer, ForeignKey("questoes.id"))
    descricao = Column(String)
    correto = Column(Boolean, default=False)
