from backend.database import SessionLocal
from backend.models import Alert

def cleanup_blank_alerts():
    db = SessionLocal()
    try:
        # Find alerts with empty or whitespace-only query
        blank_alerts = db.query(Alert).filter((Alert.query == '') | (Alert.query == None)).all()
        if blank_alerts:
            print(f"Found {len(blank_alerts)} blank alerts. Deleting...")
            for alert in blank_alerts:
                print(f"Deleting alert ID: {alert.id} (Email: {alert.email})")
                db.delete(alert)
            db.commit()
            print("Cleanup complete.")
        else:
            print("No blank alerts found.")
    except Exception as e:
        print(f"Error during cleanup: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_blank_alerts()
