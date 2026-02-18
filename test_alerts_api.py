
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_alerts_api():
    print("Testing Alerts API...")
    
    # 1. Create Alert
    print("\n1. Creating Alert...")
    payload = {
        "email": "test_verification@example.com",
        "query": "test product",
        "target_price": 50000,
        "notify_method": "email"
    }
    try:
        res = requests.post(f"{BASE_URL}/alerts", json=payload, timeout=5)
        if res.status_code != 200:
            print(f"❌ Failed to create alert: {res.text}")
            return
        data = res.json()
        alert_id = data["alert"]["id"]
        print(f"✅ Alert created. ID: {alert_id}")
    except Exception as e:
        print(f"❌ Exception creating alert: {e}")
        return

    # 2. Get Alerts
    print("\n2. Fetching Alerts...")
    try:
        res = requests.get(f"{BASE_URL}/alerts", timeout=5)
        alerts = res.json()
        found = any(a["id"] == alert_id for a in alerts)
        if found:
            print(f"✅ Created alert found in list.")
        else:
            print(f"❌ Created alert NOT found in list.")
    except Exception as e:
        print(f"❌ Exception fetching alerts: {e}")

    # 3. Update Alert Status
    print("\n3. Updating Alert Status...")
    try:
        res = requests.patch(f"{BASE_URL}/alerts/{alert_id}/status?is_active=false", timeout=5)
        if res.status_code == 200 and res.json()["alert"]["is_active"] == False:
            print(f"✅ Alert status updated to False.")
        else:
            print(f"❌ Failed to update status: {res.text}")
    except Exception as e:
        print(f"❌ Exception updating alert: {e}")

    # 4. Delete Alert
    print("\n4. Deleting Alert...")
    try:
        res = requests.delete(f"{BASE_URL}/alerts/{alert_id}", timeout=5)
        if res.status_code == 200:
            print(f"✅ Alert deleted.")
        else:
            print(f"❌ Failed to delete alert: {res.text}")
    except Exception as e:
        print(f"❌ Exception deleting alert: {e}")

    # 5. Verify Deletion
    print("\n5. Verifying Deletion...")
    try:
        res = requests.get(f"{BASE_URL}/alerts", timeout=5)
        alerts = res.json()
        found = any(a["id"] == alert_id for a in alerts)
        if not found:
            print(f"✅ Alert successfully removed from list.")
        else:
            print(f"❌ Alert still present in list after deletion.")
    except Exception as e:
        print(f"❌ Exception verifying deletion: {e}")

if __name__ == "__main__":
    test_alerts_api()
