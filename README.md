# 3-Year Revenue Forecasting & Profitability Dashboard

**EFOS Global Finance Hackathon 2026 — Case 2: Revenue Forecasting & Profitability**

An interactive FP&A tool that forecasts Revenue, Gross Profit, EBITDA, Net Income,
and Operating Cash Flow for the next 3 years, based on a company's historical
financials.

## Companies covered
Built and tested on **Amazon (AMZN)** and **NVIDIA (NVDA)**, but works for any of
the 12 companies in the dataset (Apple, Google, Microsoft, Intel, PayPal, McDonald's,
AIG, Barclays, PG&E, Sears).

## How the model works
1. **Revenue** is projected using historical CAGR (Compound Annual Growth Rate),
   adjustable via a Best/Base/Worst case scenario multiplier, or a manual override slider.
2. **Gross Profit, EBITDA, and Net Income** are forecasted by applying the company's
   historical average margins (as a % of revenue) to the forecasted revenue.
3. **Operating Cash Flow** is forecasted the same way, using the historical
   Cash-Flow-to-Revenue ratio.

This is a standard, transparent FP&A approach — every number in the forecast can be
traced back to a historical average or growth rate, which is a deliberate design choice
over an unexplainable "black box" model.

## Tech stack
- Python
- Streamlit (dashboard + deployment)
- Pandas / NumPy (data processing & forecasting logic)

## Data source
[Financial Statements dataset, Kaggle](https://www.kaggle.com/) — 12 companies,
2009–2023 historical financials.

## Running locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Live demo
[Add your Streamlit Cloud link here after deployment]
