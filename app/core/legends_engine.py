import pandas as pd
import numpy as np

class LegendsEngine:
    def __init__(self):
        # Rakesh Jhunjhunwala's Sector Weights
        self.sector_weights = {
            'BANKING': 1.2,
            'INFRASTRUCTURE': 1.15,
            'CONSUMPTION': 1.1,
            'IT': 1.0
        }

    def calculate_graham_number(self, eps: float, bvps: float) -> float:
        if eps < 0 or bvps < 0: return 0.0
        return np.sqrt(22.5 * eps * bvps)

    def screen_stocks(self, raw_data: list):
        df = pd.DataFrame(raw_data)
        if df.empty: return []

        # 1. Buffett Filter: ROE > 15% and Debt/Equity < 0.5
        df_filtered = df[
            (df['roe'] > 15.0) & (df['debt_to_equity'] < 0.5)
        ].copy()

        # 2. Big Bull Sector Boost
        df_filtered['sector_multiplier'] = df_filtered['sector'].map(self.sector_weights).fillna(1.0)

        # 3. Calculate Graham Number
        df_filtered['graham_num'] = df_filtered.apply(
            lambda x: self.calculate_graham_number(x['eps'], x['bvps']), axis=1
        )

        # 4. Final Score
        df_filtered['legend_score'] = df_filtered['roe'] * df_filtered['sector_multiplier']
        
        return df_filtered.sort_values(by='legend_score', ascending=False).to_dict(orient='records')