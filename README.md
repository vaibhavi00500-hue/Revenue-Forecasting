# Revenue Forecasting & Profitability Dashboard

Built for the EFOS Global Finance Hackathon 2026 — Case 2 (Revenue Forecasting & Profitability).

## What this is

We built a small FP&A tool that takes a company's past financials and projects
Revenue, Gross Profit, EBITDA, Net Income and Operating Cash Flow three years
into the future. We tested it mainly on Amazon and NVIDIA since they represent
two very different growth stories, but it works for any of the 12 companies in
our dataset (Apple, Google, Microsoft, Intel, PayPal, McDonald's, AIG, Barclays,
PG&E, Sears are also included).

## The logic behind the numbers

We kept the forecasting method simple on purpose — the goal was something a
finance person could actually check by hand and trust, not a black box.

- Revenue for the next 3 years is projected off the company's own historical
  growth rate (CAGR), and you can shift between a Worst/Base/Best case, or type
  in your own growth assumption if you want to test something specific.
- Gross Profit, EBITDA and Net Income are worked out by applying the company's
  historical average margins to the revenue we just projected.
- Operating Cash Flow follows the same idea, using the company's own
  cash-flow-to-revenue ratio from its history.

Every number the tool shows can be traced back to something that actually
happened in the company's past — we didn't want to hand judges a number we
couldn't explain the origin of.

## Tools used

Python, pandas and Streamlit. We picked Streamlit specifically because it let
us go from a raw CSV to a working, deployable dashboard without building a
separate front end.

## Data

Kaggle's "Financial Statements" dataset — company financials from 2009 to 2023.

## Running it yourself

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Live version

[link goes here once deployed]
