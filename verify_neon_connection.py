import psycopg2
import os
import time

# Hardcoded to be absolutely sure
DB_URL = "postgresql://neondb_owner:npg_kUQWi6mv2LhK@ep-floral-surf-aiuvuoqd-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

def test_connection():
    print(f"Attempting to connect to Neon DB...")
    print(f"URL: {DB_URL.split('@')[1]}") # Print host only for privacy/safety
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt+1}/{max_retries}...")
            conn = psycopg2.connect(DB_URL)
            cur = conn.cursor()
            cur.execute("SELECT 1")
            print("✅ CONNECTION SUCCESSFUL!")
            
            cur.execute("SELECT count(*) FROM products")
            count = cur.fetchone()[0]
            print(f"✅ Found {count} products in remote DB.")
            
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            time.sleep(2) # Wait a bit before retry (scaling to zero handling)

    return False

if __name__ == "__main__":
    test_connection()
