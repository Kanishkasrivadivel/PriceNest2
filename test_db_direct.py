import psycopg2
import os
from urllib.parse import urlparse

# Hardcoded from .env I saw earlier to be sure
DB_URL = "postgresql://neondb_owner:npg_kUQWi6mv2LhK@ep-floral-surf-aiuvuoqd-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

try:
    print(f"Connecting to: {DB_URL}")
    conn = psycopg2.connect(DB_URL)
    print("Connected!")
    cur = conn.cursor()
    cur.execute("SELECT 1")
    print("Query executed!")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
