import smtplib
import os
import sys

# Fix path so we can import from 'app'
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.legends_engine import LegendsEngine
from app.core.live_data import fetch_live_nifty_data

# SECRETS (Loaded from GitHub Actions)
SENDER_EMAIL = os.environ.get("EMAIL_USER")
SENDER_PASSWORD = os.environ.get("EMAIL_PASS")
RECEIVER_EMAIL = os.environ.get("EMAIL_RECEIVER")

def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("✅ Email Sent!")
    except Exception as e:
        print(f"❌ Failed: {e}")

def run_scan():
    print("🕵️ Running Daily Scan...")
    raw = fetch_live_nifty_data()
    engine = LegendsEngine()
    results = engine.screen_stocks(raw)
    
    # Strict Filter for Alerts: ROE > 20% and Low Debt
    gems = [s for s in results if s['roe'] > 20.0 and s['debt_to_equity'] < 0.5]
    
    if gems:
        body = f"🚀 GripInvest Found {len(gems)} Opportunities:\n\n"
        for g in gems:
            body += f"• {g['ticker']} (ROE: {g['roe']:.1f}%)\n"
        body += "\nCheck Dashboard: https://gripinvest.streamlit.app/"
        
        send_email(f"🚨 Market Alert: {len(gems)} Stocks Found", body)
    else:
        print("No alerts today.")

if __name__ == "__main__":
    run_scan()
