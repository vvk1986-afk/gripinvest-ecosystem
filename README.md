# 🚀 GripInvest+3: The Holistic Wealth Ecosystem

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gripinvest-ecosystem.streamlit.app/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Status](https://img.shields.io/badge/Status-Production-green)]()

**GripInvest+3** is an automated Fintech ecosystem designed to solve the asset allocation dilemma for retail investors. It combines the aggressive compounding of **Value Investing** with the stability of **Fixed Income**, orchestrated by a dynamic volatility logic.

---

## 📊 System Architecture

The system operates on a dual-engine architecture triggered by live market data and automated via serverless cron jobs.

```mermaid
graph TD
    A[Time Trigger / User Input] --> B{Orchestrator}
    B -->|Streamlit Dashboard| C[Visual Interface]
    B -->|GitHub Actions| D[Headless Bot]
    
    C --> E[Live Nifty 50 Data]
    D --> E
    
    E --> F{Logic Core}
    F -->|Engine A| G[Legends Equity Scanner]
    F -->|Engine B| H[Stability Debt Scanner]
    F -->|Engine C| I[Portfolio Manager VIX]
    
    G --> J[Output Layer]
    H --> J
    I --> J
    
    J -->|Dashboard| K[Charts & Tables]
    J -->|Bot| L[Email Alerts SMTP]
