import pandas as pd

class LegendsEngine:
    def screen_stocks(self, raw_data: list):
        df = pd.DataFrame(raw_data)
        if df.empty: return []

        # --- NEW SCORING LOGIC (The 100 Point Scale) ---
        
        # 1. ROE Score (30% Weight): Capped at 30 points
        df['score_roe'] = df['roe'].clip(upper=30)
        
        # 2. Debt Score (30% Weight): Lower is better
        # If Debt is 0, score is 30. If Debt is > 2, score is 0.
        df['score_debt'] = 30 * (1 - (df['debt_to_equity'] / 2))
        df['score_debt'] = df['score_debt'].clip(lower=0)
        
        # 3. Growth Score (20% Weight): Sales Growth
        df['score_growth'] = df['sales_growth'].clip(upper=20)
        
        # 4. Valuation Score (20% Weight): P/E Ratio
        # Ideal P/E is < 25. If P/E > 50, score drops.
        df['score_val'] = 20 - (df['pe_ratio'] / 50 * 20)
        df['score_val'] = df['score_val'].clip(lower=0)
        
        # --- FINAL COMPOSITE SCORE ---
        df['legend_score'] = (
            df['score_roe'] + 
            df['score_debt'] + 
            df['score_growth'] + 
            df['score_val']
        ).round(1)

        # Clean up Formatting for UI
        df['roe'] = df['roe'].round(2)
        df['debt_to_equity'] = df['debt_to_equity'].round(2)
        df['pe_ratio'] = df['pe_ratio'].round(2)
        
        return df.sort_values(by='legend_score', ascending=False).to_dict(orient='records')
