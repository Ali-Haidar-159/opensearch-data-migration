from create_tables  import create_tables
from migrate        import migrate

if __name__ == "__main__":

    print("Create PostgreSQL tables")
    create_tables()

    print("Migrate OpenSearch")
    migrate()
