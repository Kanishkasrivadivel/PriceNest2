from backend.database import SessionLocal
from backend.models import Alert

def cleanup_invalid_alerts():
    db = SessionLocal()
    try:
        # Find alerts with empty or whitespace-only query
        invalid_alerts = db.query(Alert).filter((Alert.query == '') | (Alert.query == None)).all()
        if invalid_alerts:
            print(f"Found {len(invalid_alerts)} invalid blank alerts. Deleting...")
            for alert in invalid_alerts:
                print(f"Deleting alert ID: {alert.id} (Email: {alert.email})")
                db.delete(alert)
            db.commit()
            print("Cleanup complete.")
        else:
            print("No invalid alerts found.")
    except Exception as e:
        print(f"Error during cleanup: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_invalid_alerts()
