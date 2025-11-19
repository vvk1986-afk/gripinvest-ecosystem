import streamlit as st
import pandas as pd
import plotly.express as px
from app.core.legends_engine import LegendsEngine
from app.core.live_data import fetch_live_nifty_data
from app.core.stability_engine import StabilityEngine
from app.core.portfolio_manager import PortfolioManager # New Import

st.set_page_config(page_title="GripInvest+3 Pro", layout="wide")
st.title("🚀 GripInvest+3: The Holistic Wealth Ecosystem")

# Create 3 Tabs
tab1, tab2, tab3 = st.tabs(["📊 Portfolio Strategy", "📈 Legends (Stocks)", "🛡️ Stability (Bonds)"])

# --- TAB 1: PORTFOLIO STRATEGY (THE BRAIN) ---
with tab1:
    st.markdown("### 🧠 The Barbell Allocator")
    if st.button("🤖 Analyze Market Regime (India VIX)"):
        manager = PortfolioManager()
        strategy = manager.get_allocation_strategy()
        
        # Display VIX Gauge
        c1, c2, c3 = st.columns(3)
        c1.metric("India VIX", f"{strategy['vix']:.2f}")
        c2.metric("Market Mood", strategy['mood'])
        c3.metric("Recommended Split", f"{strategy['equity_pct']}% Equity / {strategy['debt_pct']}% Debt")
        
        st.info(f"**Advisor Note:** {strategy['advice']}")
        
        # Pie Chart of Allocation
        alloc_df = pd.DataFrame({
            "Asset Class": ["Legends (Stocks)", "Stability (Bonds)"],
            "Allocation": [strategy['equity_pct'], strategy['debt_pct']]
        })
        fig = px.pie(alloc_df, values='Allocation', names='Asset Class', title="Target Portfolio Allocation", color_discrete_sequence=['#00CC96', '#636EFA'])
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: EQUITY ---
with tab2:
    st.markdown("### NIFTY 50 Scanner")
    with st.expander("⚙️ Settings"):
        min_roe = st.slider("Min ROE", 10.0, 30.0, 15.0)
    
    if st.button("Scan Stocks"):
        progress = st.progress(0); status = st.empty()
        raw = fetch_live_nifty_data(lambda p, m: (progress.progress(p), status.text(m)))
        status.empty(); progress.empty()
        
        df = pd.DataFrame(LegendsEngine().screen_stocks(raw))
        df_final = df[df['roe'] >= min_roe]
        
        if not df_final.empty:
            st.success(f"Found {len(df_final)} Stocks")
            st.dataframe(df_final[['ticker', 'sector', 'current_price', 'roe', 'legend_score']], use_container_width=True)

# --- TAB 3: FIXED INCOME ---
with tab3:
    st.markdown("### High-Yield Fixed Income")
    if st.button("Find Bonds"):
        assets = StabilityEngine().get_safe_assets(min_yield=10.0)
        st.table(pd.DataFrame(assets))