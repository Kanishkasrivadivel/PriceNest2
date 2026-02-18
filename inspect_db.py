
import os
from sqlalchemy import create_engine, text, inspect
from backend.models import Base
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ DATABASE_URL missing")
    exit(1)

print(f"Connecting to: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("✅ Connected to database")

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables: {tables}")

    if "alerts" in tables:
        columns = [c["name"] for c in inspector.get_columns("alerts")]
        print(f"Alerts columns: {columns}")
        
        if "is_active" not in columns:
            print("⚠️ 'is_active' column missing. Adding it...")
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE alerts ADD COLUMN is_active BOOLEAN DEFAULT TRUE"))
            print("✅ 'is_active' column added.")
        else:
            print("✅ 'is_active' column present.")
    else:
        print("⚠️ 'alerts' table missing. Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created.")

    connection.close()

except Exception as e:
    print(f"❌ Error: {e}")
