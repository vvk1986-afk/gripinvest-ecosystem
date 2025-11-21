***************Add Project Blueprint.**************

# 📘 GripInvest+3: Project Blueprint & Architecture

**Version:** 2.0 (Production)
**Status:** Live & Automated
**Tech Stack:** Python, Streamlit, GitHub Actions, Plotly

---

## 1. Executive Summary
GripInvest+3 is an automated wealth ecosystem designed to solve the asset allocation dilemma. It combines:
1.  **Equity Engine:** Finds high-growth stocks using a weighted "Legend Score" (ROE + Growth + Valuation).
2.  **Stability Engine:** Finds high-yield fixed-income assets (10-14% Yield).
3.  **Portfolio Brain:** Dynamically adjusts Asset Allocation based on Market Volatility (India VIX).
4.  **Automation:** "Night Watchman" bot scans the market 5 times daily and emails alerts.

---

## 2. Functional Modules

### A. The "Legends" Equity Engine
* **Input:** Nifty 50 Live Data (Yahoo Finance).
* **Logic (Weighted Score):**
    * **ROE (30%):** Target > 20%.
    * **Debt (30%):** Target < 0.5 D/E.
    * **Growth (20%):** Sales Growth.
    * **Value (20%):** P/E Ratio.
* **Visuals:** Green-to-Red gradient heatmap in Dashboard.

### B. The "Stability" Fixed Income Engine
* **Input:** Repository of Bonds/SDIs/Leases.
* **Logic:**
    * Yield Filter (10-14%).
    * Safety Rating Filter (CRISIL A/AA).
* **Goal:** Provide safe parking spots for capital during high volatility.

### C. The "Barbell" Portfolio Manager
* **Input:** Live India VIX.
* **Logic:**
    * **VIX < 12 (Greed):** 70% Equity / 30% Debt.
    * **VIX 12-16 (Neutral):** 60% Equity / 40% Debt.
    * **VIX > 16 (Fear):** 40% Equity / 60% Debt.

### D. Automated Alerts (GitHub Actions)
* **Schedule:** 9:30 AM, 11:00 AM, 12:30 PM, 2:00 PM, 3:30 PM (IST).
* **Triggers:**
    * **Investment Alert:** If a stock hits "Legend" status (ROE > 20, Low Debt).
    * **Trading Alert:** If a stock moves > 3.5% in one day.

---

## 3. Database & Data Flow

* **Data Source:** `yfinance` (Real-time).
* **Processing:** Python (Pandas).
* **Storage:** Stateless (Calculated on-the-fly).
* **Secrets:** Encrypted via GitHub Secrets (`EMAIL_USER`, `EMAIL_PASS`).

---

## 4. Future Roadmap (Phase 3)
* Integration with **AI (LLM)** for Sentiment Analysis.
* Expansion to **Nifty 500** universe.
* User Login & Portfolio Persistence (Supabase).
