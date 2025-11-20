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
    print("🕵️ Running Daily Market Scan...")
    
    # 1. Fetch Data
    raw_data = fetch_live_nifty_data()
    engine = LegendsEngine()
    results = engine.screen_stocks(raw_data)
    
    # --- ALERT LOGIC ---
    
    # Trigger 1: The Legends (Fundamentals)
    legends = [s for s in results if s['roe'] > 20.0 and s['debt_to_equity'] < 0.5]
    
    # Trigger 2: The Movers (Abnormal Variance)
    # We look for absolute change > 3.5% (Up or Down)
    movers = [s for s in results if abs(s['change_p']) >= 3.5]
    
    # Combine them (avoid duplicates)
    all_alerts = {s['ticker']: s for s in legends + movers}.values()
    
    if all_alerts:
        # Get IST Time
        ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
        time_str = ist_now.strftime("%I:%M %p")
        
        print(f"🚀 Found {len(all_alerts)} alerts!")
        
        # Build Email Body
        body = f"GripInvest+3 Market Pulse [{time_str}]\n\n"
        
        if movers:
            body += "🚨 ABNORMAL PRICE MOVEMENT (>3.5%):\n"
            for m in movers:
                icon = "📈" if m['change_p'] > 0 else "📉"
                body += f"{icon} {m['ticker']}: {m['change_p']:.2f}% (Price: {m['current_price']})\n"
            body += "\n" + "-"*20 + "\n\n"
            
        if legends:
            body += "💎 LEGENDARY FUNDAMENTALS (ROE > 20%):\n"
            for l in legends:
                body += f"• {l['ticker']} | ROE: {l['roe']:.1f}% | Debt: {l['debt_to_equity']}\n"

        body += "\nAnalyze Dashboard: https://gripinvest.streamlit.app/"
        
        # Send Email
        subject = f"🚨 Market Alert ({time_str}): {len(movers)} Movers & {len(legends)} Legends"
        
        if SENDER_EMAIL and SENDER_PASSWORD:
            send_email(subject, body)
        else:
            print("⚠️ Secrets not found. Skipping email.")
    else:
        print("😴 Market is quiet. No alerts today.")
