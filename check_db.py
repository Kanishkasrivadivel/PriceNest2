import sys
import os
from sqlalchemy import text

sys.path.append(os.getcwd())

try:
    print("Importing backend.database...")
    from backend.database import SessionLocal
    print("Successfully imported backend.database")
    
    print("Testing DB connection...")
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        print("DB Connection Successful!")
    except Exception as e:
        print(f"DB Connection Failed: {e}")
    finally:
        db.close()

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
