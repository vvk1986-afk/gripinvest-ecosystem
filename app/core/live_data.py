import yfinance as yf

# NIFTY 50 List
NIFTY_50 = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS', 'BHARTIARTL.NS', 
    'ITC.NS', 'SBIN.NS', 'LICI.NS', 'HINDUNILVR.NS', 'LT.NS', 'BAJFINANCE.NS', 
    'HCLTECH.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'SUNPHARMA.NS', 'TITAN.NS', 
    'ADANIENT.NS', 'ULTRACEMCO.NS', 'ASIANPAINT.NS', 'NTPC.NS', 'MARUTI.NS', 
    'POWERGRID.NS', 'BAJAJFINSV.NS', 'TATAMOTORS.NS', 'COALINDIA.NS', 'ONGC.NS', 
    'M&M.NS', 'WIPRO.NS', 'ADANIPORTS.NS', 'JSWSTEEL.NS', 'NESTLEIND.NS', 
    'TATASTEEL.NS', 'HDFCLIFE.NS', 'SBILIFE.NS', 'GRASIM.NS', 'TECHM.NS', 
    'HINDALCO.NS', 'CIPLA.NS', 'BRITANNIA.NS', 'TATACONSUM.NS', 'EICHERMOT.NS', 
    'DRREDDY.NS', 'DIVISLAB.NS', 'APOLLOHOSP.NS', 'BAJAJ-AUTO.NS', 'HEROMOTOCO.NS', 
    'UPL.NS', 'INDUSINDBK.NS', 'BPCL.NS'
]

def fetch_live_nifty_data(progress_callback=None):
    live_data = []
    total_stocks = len(NIFTY_50)
    
    for i, ticker in enumerate(NIFTY_50):
        try:
            if progress_callback:
                progress_callback(i / total_stocks, f"Scanning {ticker}...")

            stock = yf.Ticker(ticker)
            info = stock.info
            
            # --- NEW DATA POINTS FOR V2 ---
            stock_data = {
                "ticker": ticker.replace('.NS', ''),
                "sector": info.get('sector', 'Unknown').upper(),
                "current_price": info.get('currentPrice', 0),
                "roe": (info.get('returnOnEquity', 0) or 0) * 100,
                "debt_to_equity": info.get('debtToEquity', 0) / 100,
                "pe_ratio": info.get('trailingPE', 0) or 0,            # New: P/E
                "sales_growth": (info.get('revenueGrowth', 0) or 0) * 100  # New: Growth
            }
            
            # Sector Cleanup
            if "BANK" in stock_data['sector']: stock_data['sector'] = "BANKING"
            if "TECH" in stock_data['sector']: stock_data['sector'] = "IT"
            if "FINANCIAL" in stock_data['sector']: stock_data['sector'] = "FINANCE"
            
            live_data.append(stock_data)
            
        except Exception:
            pass
            
    return live_data
