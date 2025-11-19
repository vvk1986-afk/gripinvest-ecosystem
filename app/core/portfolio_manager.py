import yfinance as yf

class PortfolioManager:
    def __init__(self):
        # India VIX Ticker on Yahoo Finance
        self.vix_ticker = "^INDIAVIX"

    def get_allocation_strategy(self):
        try:
            # Fetch live India VIX
            vix = yf.Ticker(self.vix_ticker)
            current_vix = vix.history(period="1d")['Close'].iloc[-1]
        except:
            # Fallback if API fails
            current_vix = 13.5 
            
        # The "Barbell" Logic
        if current_vix < 12.0:
            # Market is very complacent -> Max Aggression
            return {
                "vix": current_vix,
                "mood": "Extreme Greed 🤑",
                "equity_pct": 80,
                "debt_pct": 20,
                "advice": "Volatility is ultra-low. Go heavy on Legends (Stocks)."
            }
        elif 12.0 <= current_vix < 16.0:
            # Normal Market -> Balanced Growth
            return {
                "vix": current_vix,
                "mood": "Neutral / Stable 😐",
                "equity_pct": 60,
                "debt_pct": 40,
                "advice": "Market is stable. Maintain a standard 60/40 growth portfolio."
            }
        else:
            # High Fear -> Safety First
            return {
                "vix": current_vix,
                "mood": "High Fear 😨",
                "equity_pct": 30,
                "debt_pct": 70,
                "advice": "Market is risky! Shift capital to Stability (Bonds/SDIs) immediately."
            }