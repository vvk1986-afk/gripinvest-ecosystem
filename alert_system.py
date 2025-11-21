import smtplib
import os
import sys
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- PATH SETUP ---
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

from core.legends_engine import LegendsEngine
from core.live_data import fetch_live_nifty_data

# --- SECRETS ---
SENDER_EMAIL = os.environ.get("EMAIL_USER")
SENDER_PASSWORD = os.environ.get("EMAIL_PASS")
RECEIVER_EMAIL = os.environ.get("EMAIL_RECEIVER")

def send_email(subject, body):
    print(f"📧 Preparing to send email to: {RECEIVER_EMAIL}")
    
    try:
        # Handle Multiple Receivers (Comma Separated)
        if "," in RECEIVER_EMAIL:
            recipients = [e.strip() for e in RECEIVER_EMAIL.split(",")]
        else:
            recipients = [RECEIVER_EMAIL]

        msg = MIMEMultipart()
        msg['From'] = f"GripInvest Robot <{SENDER_EMAIL}>"
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail
        print("🔌 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login
        print("🔑 Logging in...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send
        print("🚀 Sending message...")
        server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
        
        server.quit()
        print("✅ EMAIL SENT SUCCESSFULLY! (Check Spam/Promotions folders)")
        return True
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        return False

def run_scan():
    print("🕵️ Starting Scan...")
    
    # 1. Fetch Data
    raw_data = fetch_live_nifty_data()
    if not raw_data:
        print("❌ Error: No data fetched from NSE.")
        return

    # 2. Analyze
    engine = LegendsEngine()
    results = engine.screen_stocks(raw_data)
    
    # 3. Filter (Relaxed for testing: ROE > 10%)
    # We lower the bar to ENSURE we find stocks so the email triggers
    gems = [s for s in results if s['roe'] > 10.0]
    
    if gems:
        # Time Setup
        ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
        time_str = ist_now.strftime("%I:%M %p")
        
        print(f"💎 Found {len(gems)} stocks. Triggering email.")
        
        body = f"GripInvest Test Alert [{time_str}]\n\n"
        body += f"Found {len(gems)} stocks (Test Mode):\n"
        for g in gems[:5]: # List top 5 only
            body += f"- {g['ticker']} (ROE: {g['roe']:.1f}%)\n"
            
        subject = f"Test Alert {time_str}: {len(gems)} Stocks Found"
        
        if SENDER_EMAIL and SENDER_PASSWORD:
            send_email(subject, body)
        else:
            print("⚠️ Secrets are MISSING. Cannot send email.")
    else:
        print("😴 No stocks found (Unlikely with 10% ROE filter).")

if __name__ == "__main__":
    run_scan()
