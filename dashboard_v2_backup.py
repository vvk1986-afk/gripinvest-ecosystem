import sys
import os
# Path fix for Cloud
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

import streamlit as st
import pandas as pd
import plotly.express as px

from core.legends_engine import LegendsEngine
from core.live_data import fetch_live_nifty_data
from core.stability_engine import StabilityEngine

# 1. Page Config
st.set_page_config(page_title="GripInvest+3 v2.0", layout="wide")
st.title("🚀 GripInvest+3: Intelligent Wealth Ecosystem")

# 2. Main Tabs
tab1, tab2, tab3 = st.tabs(["📈 Legends (Stocks)", "🛡️ Stability (Bonds)", "⚖️ Portfolio Strategy"])

# --- TAB 1: LEGENDS (Equity) ---
with tab1:
    st.markdown("### NIFTY 50 Smart Scanner")
    
    if st.button("🔄 Scan Market (Live)", key="scan_btn"):
        # Progress Bar
        bar = st.progress(0); txt = st.empty()
        raw = fetch_live_nifty_data(lambda p, m: (bar.progress(p), txt.text(m)))
        bar.empty(); txt.empty()
        
        # Logic
        engine = LegendsEngine()
        results = engine.screen_stocks(raw)
        df = pd.DataFrame(results)
        
        if not df.empty:
            # 3 Quick Wins: Metric Cards
            top_pick = df.iloc[0]
            col1, col2, col3 = st.columns(3)
            col1.metric("🏆 #1 Legend", top_pick['ticker'], f"Score: {top_pick['legend_score']}")
            col2.metric("📊 Avg Portfolio ROE", f"{df.head(10)['roe'].mean():.1f}%")
            col3.metric("📉 Lowest Debt Pick", df.sort_values('debt_to_equity').iloc[0]['ticker'])

            # Detailed Dataframe with Gradient
            st.subheader("The Shortlist (Weighted Score)")
            
            # Gradient Coloring: Green for High Score, Red for Low
            # We use a try-except block to prevent styling crashes if data is empty
            try:
                st.dataframe(
                    df[['ticker', 'sector', 'current_price', 'roe', 'debt_to_equity', 'pe_ratio', 'sales_growth', 'legend_score']]
                    .style.background_gradient(subset=['legend_score'], cmap='RdYlGn', vmin=50, vmax=90),
                    use_container_width=True
                )
            except:
                st.dataframe(df) # Fallback if styling fails
        else:
            st.warning("No data returned from scanner.")

# --- TAB 2: STABILITY (Bonds) ---
with tab2:
    st.markdown("### Fixed Income Opportunities")
    
    # Sidebar Filter for this tab
    col_filter, col_disp = st.columns([1, 3])
    with col_filter:
        min_yield = st.slider("Min Yield Target (%)", 8.0, 15.0, 10.0)
    
    with col_disp:
        engine = StabilityEngine()
        assets = engine.get_safe_assets(min_yield)
        
        if assets:
            st.success(f"Found {len(assets)} assets matching your yield target.")
            st.table(pd.DataFrame(assets))
        else:
            st.warning("No assets found. Try lowering your yield expectation.")

# --- TAB 3: PORTFOLIO STRATEGY (Allocator) ---
with tab3:
    st.markdown("### ⚖️ Capital Allocator")
    
    col_input, col_chart = st.columns([1, 1])
    
    with col_input:
        st.write("Enter your investment capital to get a recommended split based on Market Valuation (P/E).")
        capital = st.number_input("Total Investment (₹)", value=500000, step=10000)
        
        # Calculate Market P/E (Mock logic using Nifty avg if available, else static for demo)
        market_pe = 24.5 # In a real app, we calculate this from the scanned data
        st.metric("Current Nifty 50 P/E", f"{market_pe}")

        # Allocation Logic
        if market_pe > 25:
            rec_equity = 40
            rec_debt = 60
            mood = "Defensive (Market Expensive)"
        elif market_pe < 20:
            rec_equity = 70
            rec_debt = 30
            mood = "Aggressive (Market Cheap)"
        else:
            rec_equity = 50
            rec_debt = 50
            mood = "Balanced (Market Fair)"
            
        equity_amt = capital * (rec_equity/100)
        debt_amt = capital * (rec_debt/100)
        
        st.info(f"**Strategy:** {mood}")
        st.write(f"🟢 **Equity:** ₹{equity_amt:,.0f}")
        st.write(f"🔵 **Fixed Income:** ₹{debt_amt:,.0f}")

    with col_chart:
        # Plotly Pie Chart
        df_alloc = pd.DataFrame({
            "Asset": ["Equity", "Fixed Income"],
            "Amount": [equity_amt, debt_amt]
        })
        fig = px.pie(df_alloc, values='Amount', names='Asset', 
                     color='Asset', color_discrete_map={'Equity':'#00CC96', 'Fixed Income':'#636EFA'},
                     title="Recommended Split")
        st.plotly_chart(fig)
