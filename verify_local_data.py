import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add root directory to path
sys.path.append(os.getcwd())

from backend.models import Product, Alert, PriceHistory

# Connect to LOCAL SQLite DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def verify_data():
    db = SessionLocal()
    try:
        print("-" * 50)
        print("VERIFYING LOCAL DATABASE (sql_app.db)")
        print("-" * 50)

        # 1. Check Products
        products = db.query(Product).all()
        print(f"\n[PRODUCTS] Found {len(products)} products:")
        for p in products:
            print(f" - {p.title} (${p.price})")

        # 2. Check Alerts
        alerts = db.query(Alert).all()
        print(f"\n[ALERTS] Found {len(alerts)} alerts:")
        for a in alerts:
            print(f" - Email: {a.email}, Query: {a.query}, Target: {a.target_price}")

        # 3. Check History
        history = db.query(PriceHistory).limit(5).all()
        print(f"\n[HISTORY] Found {db.query(PriceHistory).count()} price history records. Last 5:")
        for h in history:
            print(f" - {h.timestamp}: {h.query} - {h.price}")

    except Exception as e:
        print(f"Error reading database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_data()
