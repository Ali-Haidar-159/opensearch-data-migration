import os
from opensearchpy import OpenSearch
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_opensearch_client():
    return OpenSearch(
        hosts=[{
            "host": os.getenv("OPENSEARCH_HOST"),
            "port": int(os.getenv("OPENSEARCH_PORT"))
        }],
        http_auth=(
            os.getenv("OPENSEARCH_USER"),
            os.getenv("OPENSEARCH_PASSWORD")
        ),
        use_ssl=True,
        verify_certs=False,       
        ssl_show_warn=False
    )

def get_postgres_engine():
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db   = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    pwd  = os.getenv("POSTGRES_PASSWORD")

    url = f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{db}"
    return create_engine(url, pool_pre_ping=True)
