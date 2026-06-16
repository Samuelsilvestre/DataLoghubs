from src.infra.connection_db import engine, Base
# Importe aqui todos os seus modelos, senão o SQLAlchemy não saberá que eles existem
from src.domain.model.models import Hub, Yard, Warehouse, Product, Movement

def init_db():
    print("Criando tabelas no banco de dados...")
    
    # O comando create_all lê todos os modelos que herdam da Base
    # e cria as tabelas no banco de dados se elas não existirem.
    Base.metadata.create_all(bind=engine)
    
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    init_db()