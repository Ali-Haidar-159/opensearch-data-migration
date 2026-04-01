from config.db.connection import get_postgres_engine
from config.db.models import metadata

def create_tables():
    engine = get_postgres_engine()
    metadata.create_all(engine)
    print("Tables created")

if __name__ == "__main__":
    create_tables()
