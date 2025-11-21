import pandas as pd

class StabilityEngine:
    def __init__(self):
        # MOCK DATA as requested in requirements
        self.bond_repository = [
            {"asset": "LeaseX E-Mobility", "type": "Lease", "yield_pct": 14.2, "rating": "Unrated (Secured)", "min_investment": 90000},
            {"asset": "Navi Fin Bond Series II", "type": "Corp Bond", "yield_pct": 10.8, "rating": "IND A", "min_investment": 10000},
            {"asset": "Grip SDI - Warehousing", "type": "SDI", "yield_pct": 12.5, "rating": "CRISIL A", "min_investment": 100000},
            {"asset": "Shriram Finance FD", "type": "Corp FD", "yield_pct": 8.9, "rating": "CRISIL AA+", "min_investment": 5000},
            {"asset": "InCred Financial Bond", "type": "Corp Bond", "yield_pct": 11.5, "rating": "CRISIL A+", "min_investment": 10000},
            {"asset": "Vivriti Capital SDI", "type": "SDI", "yield_pct": 13.1, "rating": "ICRA A", "min_investment": 50000},
        ]

    def get_safe_assets(self, min_yield):
        df = pd.DataFrame(self.bond_repository)
        
        # Filter Logic based on User Slider
        df_filtered = df[df['yield_pct'] >= min_yield].copy()
        
        return df_filtered.sort_values(by='yield_pct', ascending=False).to_dict(orient='records')
