import psycopg2
from psycopg2.extras import RealDictCursor
import openai

# Neon database credentials
DB_HOST = "ep-aged-water-adbp7t8k-pooler.c-2.us-east-1.aws.neon.tech"
DB_NAME = "neondb"
DB_USER = "neondb_owner"
DB_PASSWORD = "npg_hv3FTfGu5oVm"
DB_PORT = 5432

# OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

def get_embedding(text: str):
    response = openai.Embedding.create(
        model="text-embedding-3-large",
        input=text
    )
    return response['data'][0]['embedding']

def search_rag_sources(query: str, top_k: int = 5):
    query_embedding = get_embedding(query)

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        sslmode="require"
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT title, url, summary
        FROM academic_sources
        ORDER BY content_embedding <#> %s
        LIMIT %s;
    """, (query_embedding, top_k))

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
