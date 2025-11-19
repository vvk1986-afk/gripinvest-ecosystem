import pandas as pd

class StabilityEngine:
    def __init__(self):
        # Mock Database of Fixed Income Assets
        # In a real app, this would query a SQL Database or Grip Invest API
        self.bond_repository = [
            {"asset": "Grip SDI - Lease X", "type": "SDI", "yield_pct": 12.5, "rating": "CRISIL A", "min_investment": 100000, "tenure_months": 24},
            {"asset": "Navi Fin Bond", "type": "Corp Bond", "yield_pct": 10.8, "rating": "IND A", "min_investment": 10000, "tenure_months": 18},
            {"asset": "BluSmart EV Lease", "type": "Lease Finance", "yield_pct": 14.2, "rating": "Unrated (Secured)", "min_investment": 250000, "tenure_months": 36},
            {"asset": "Shriram Finance FD", "type": "Corp FD", "yield_pct": 8.9, "rating": "CRISIL AA+", "min_investment": 5000, "tenure_months": 60},
            {"asset": "Govt G-Sec 2030", "type": "G-Sec", "yield_pct": 7.1, "rating": "Sovereign", "min_investment": 10000, "tenure_months": 72},
        ]

    def get_safe_assets(self, min_yield=10.0):
        """
        Filters assets that offer high yield but have decent safety ratings.
        """
        df = pd.DataFrame(self.bond_repository)
        
        # Filter 1: Yield must be attractive (default > 10%)
        df_filtered = df[df['yield_pct'] >= min_yield].copy()
        
        # Filter 2: Risk Adjustment (We prefer shorter tenure for high risk)
        # If unrated/secured, tenure must be < 48 months to be "safe-ish"
        df_filtered['is_safe'] = df_filtered.apply(
            lambda x: True if "AA" in x['rating'] or "Sovereign" in x['rating'] or x['tenure_months'] < 40 else False, axis=1
        )
        
        return df_filtered[df_filtered['is_safe']].sort_values(by='yield_pct', ascending=False).to_dict(orient='records')