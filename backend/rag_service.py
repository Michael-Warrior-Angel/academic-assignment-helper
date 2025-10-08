import os
import psycopg2
from psycopg2.extras import RealDictCursor
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Database credentials from environment
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", 5432)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str):
    """Generate embedding using OpenAI API."""
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding


def search_rag_sources(query: str, top_k: int = 5):
    """Retrieve top-k similar academic sources using pgvector similarity search."""
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

    # pgvector cosine distance operator (<#>)
    cur.execute("""
        SELECT title, url, summary,
               1 - (content_embedding <#> %s::vector) AS similarity
        FROM academic_sources
        ORDER BY content_embedding <#> %s::vector
        LIMIT %s;
    """, (query_embedding, query_embedding, top_k))

    results = cur.fetchall()
    cur.close()
    conn.close()

    # Optional: return a cleaner text block for LLM use
    formatted_results = [
        f"{r['title']}: {r['summary']} (Source: {r['url']})"
        for r in results
    ]

    return formatted_results
