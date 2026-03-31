import os
from opensearchpy import OpenSearch
import psycopg2
from dotenv import load_dotenv

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

def get_postgres_conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )