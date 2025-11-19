from fastapi import FastAPI
from app.core.legends_engine import LegendsEngine
from app.core.live_data import fetch_live_nifty_data

app = FastAPI(title="GripInvest+3 Real-Time API")
engine = LegendsEngine()

@app.get("/")
def home():
    return {"status": "GripInvest+3 connected to NSE Live"}

@app.get("/api/legends")
def get_legend_picks():
    """
    1. Fetches live data for Reliance, TCS, ITC, etc.
    2. Filters them using Buffett/Jhunjhunwala Logic.
    3. Returns the winners.
    """
    # 1. Get Real Data
    real_data = fetch_live_nifty_data()
    
    # 2. Apply the Logic
    results = engine.screen_stocks(real_data)
    
    return {
        "count": len(results), 
        "analyzed_stocks": len(real_data),
        "top_picks": results
    }