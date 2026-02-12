import time
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler
import os

from backend.backend_scrapper import compare_product
from backend import storage



# =========================
# EMAIL CONFIG (GMAIL)
# =========================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_SENDER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

# ⚠️ NO SPACES (App Password)
# NOTE: Receiver will be taken from alert email field


# =========================
# SEND EMAIL FUNCTION
# =========================
def send_email_alert(receiver_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"[EMAIL SENT] to {receiver_email}")

    except Exception as e:
        print("[EMAIL ERROR]", e)


# =========================
# ALERT CHECK JOB
# =========================
def check_alerts_job():
    print("\n[Scheduler] Checking alerts...")
    alerts = storage.list_alerts()

    if not alerts:
        print("No alerts found.")
        return

    for a in alerts:
        if not a.get("is_active", True):
            continue

        query = a["query"]
        target_price = int(a["target_price"])
        receiver_email = a["email"]

        print(f"Checking Alert ID {a['id']} | {query} | Target ₹{target_price}")

        result = compare_product(query)

        if not result.get("results"):
            print("No prices found.")
            continue

        best = result["results"][0]
        best_price = int(best["price_numeric"])

        print(f"Best Price Found: ₹{best_price}")

        # =========================
        # ALERT CONDITION
        # =========================
        if best_price <= target_price:
            subject = f"🎉 Price Drop Alert: {query}"

            body = (
                f"Price Alert Triggered!\n\n"
                f"Product: {query}\n"
                f"Target Price: ₹{target_price:,}\n"
                f"Current Price: ₹{best_price:,}\n"
                f"Store: {best['source']}\n"
                f"Link: {best['link']}\n\n"
                f"Alert ID: {a['id']}"
            )

            print("[ALERT TRIGGERED] Sending email...")
            send_email_alert(receiver_email, subject, body)

            storage.deactivate_alert(a["id"])
            print(f"Alert {a['id']} deactivated.")


# =========================
# MAIN RUNNER
# =========================
if __name__ == "__main__":
    print("Running alert check (GitHub Actions mode)...")
    check_alerts_job()
    print("Finished alert check.")
