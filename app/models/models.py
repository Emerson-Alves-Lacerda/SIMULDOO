from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.connection.database import Base

class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    ano = Column(Integer)
    descricao = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint("nome", "ano", name="uq_materia_nome_ano"),
        {'sqlite_autoincrement': True},
    )

class Questao(Base):
    __tablename__ = "questoes"


    id = Column(Integer, primary_key=True, index=True)
    enunciado = Column(String, nullable=False)
    nivel = Column(Integer, nullable=False)
    materia = Column(Integer, ForeignKey("materias.id"))
    total_correta = Column(Integer, nullable=False)
    status = Column(Boolean, default=False)

    alternativas = relationship("Alternativa", back_populates="questao", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('enunciado', 'materia', name='uq_questao_enunciado_materia'),
    )

class Alternativa(Base):
    __tablename__ = "alternativas"
    id = Column(Integer, primary_key=True, index=True)
    questao_id = Column(Integer, ForeignKey("questoes.id"))
    descricao = Column(String, nullable=False)
    correto = Column(Boolean, default=False)

    questao = relationship("Questao", back_populates="alternativas")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    matricula = Column(String, unique=True, nullable=False)

    simulados = relationship("AlunoSimulado", back_populates="aluno")

class Simulado(Base):
    __tablename__ = "simulados"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

class AlunoSimulado(Base):
    __tablename__ = "aluno_simulado"
    alunos_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    simulado_id = Column(Integer, ForeignKey("simulados.id"), primary_key=True)
    total_acertos = Column(Integer, default=0)

    aluno = relationship("Usuario", back_populates="simulados")

class AlunoQuestao(Base):
    __tablename__ = "aluno_questao"
    alunos_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    questao_id = Column(Integer, ForeignKey("questoes.id"), primary_key=True)
    simulado_id = Column(Integer, ForeignKey("simulados.id"), primary_key=True)
    correto = Column(Boolean)

class AlunoAlternativa(Base):
    __tablename__ = "aluno_alternativa"
    alunos_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    alternativa_id = Column(Integer, ForeignKey("alternativas.id"), primary_key=True)
