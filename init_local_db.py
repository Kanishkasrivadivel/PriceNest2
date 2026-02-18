import sys
import os

# Add root directory to path
sys.path.append(os.getcwd())

try:
    from backend.database import engine
    from backend.models import Base

    def init():
        print("Creating tables in local SQLite database...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully! ✅")
        print(f"Database file should be at: {os.path.join(os.getcwd(), 'sql_app.db')}")

    if __name__ == "__main__":
        init()

except Exception as e:
    print(f"Error initializing DB: {e}")
    import traceback
    traceback.print_exc()
