from app.connection.database import Base, engine
from app.models import models

Base.metadata.create_all(bind=engine)

print("✅ Banco de dados recriado com sucesso.")
