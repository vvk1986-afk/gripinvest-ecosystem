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
    try:
        if "," in RECEIVER_EMAIL:
            recipients = [e.strip() for e in RECEIVER_EMAIL.split(",")]
        else:
            recipients = [RECEIVER_EMAIL]

        msg = MIMEMultipart()
        msg['From'] = f"GripInvest Bot <{SENDER_EMAIL}>"
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
        server.quit()
        print(f"✅ Email Sent to {len(recipients)} recipients!")
    except Exception as e:
        print(f"❌ Email Error: {e}")

def run_scan():
    print("🕵️ Running Production Market Scan...")
    
    raw_data = fetch_live_nifty_data()
    engine = LegendsEngine()
    results = engine.screen_stocks(raw_data)
    
    # --- TRIGGER 1: The Legends (Investments) ---
    # Strict Filter: High ROE + Low Debt
    legends = [s for s in results if s['roe'] > 20.0 and s['debt_to_equity'] < 0.5]
    
    # --- TRIGGER 2: The Movers (Trading) ---
    # Absolute price change > 3.5%
    movers = [s for s in results if abs(s.get('change_p', 0)) >= 3.5]
    
    # Combine unique alerts
    all_alerts = {s['ticker']: s for s in legends + movers}.values()
    
    if all_alerts:
        ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
        time_str = ist_now.strftime("%I:%M %p")
        
        print(f"🚀 Found {len(all_alerts)} relevant alerts.")
        
        body = f"GripInvest+3 Market Pulse [{time_str}]\n\n"
        
        if movers:
            body += "🚨 HIGH VOLATILITY (>3.5%):\n"
            for m in movers:
                icon = "📈" if m['change_p'] > 0 else "📉"
                body += f"{icon} {m['ticker']}: {m['change_p']:.2f}% (Price: {m['current_price']})\n"
            body += "\n"
            
        if legends:
            body += "💎 QUALITY PICKS (ROE > 20%):\n"
            for l in legends:
                body += f"• {l['ticker']} | ROE: {l['roe']:.1f}% | Debt: {l['debt_to_equity']}\n"

        body += "\nAnalyze Dashboard: https://gripinvest.streamlit.app/"
        
        if SENDER_EMAIL and SENDER_PASSWORD:
            send_email(f"🚨 Market Alert ({time_str})", body)
        else:
            print("⚠️ No secrets found.")
    else:
        print("😴 Market is quiet. No alerts met the strict criteria.")

if __name__ == "__main__":
    run_scan()
