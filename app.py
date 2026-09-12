"""
3-Year Revenue, Profitability & Cash Flow Forecasting Dashboard
Case 2: Revenue Forecasting & Profitability
Data: Financial_Statements.csv (Kaggle)

HOW THE MODEL WORKS (explain this in your PPT):
1. Revenue: projected forward using historical CAGR (Compound Annual Growth Rate),
   adjustable with a scenario multiplier (Best / Base / Worst case).
2. Costs & Profitability: Gross Margin %, EBITDA Margin %, and Net Profit Margin %
   are calculated as historical averages, then applied to forecasted revenue.
   (This is a standard, explainable FP&A technique — assume margins stay roughly
   consistent unless the user changes them.)
3. Cash Flow: Operating Cash Flow is forecasted as a % of revenue, based on the
   company's historical Cash-Flow-to-Revenue ratio.
"""

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="3-Year Financial Forecast Dashboard", layout="wide")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_csv("Financial_Statements.csv")
    df.columns = [c.strip() for c in df.columns]  # clean stray spaces in headers
    df["Company"] = df["Company"].str.strip()
    df["Year"] = df["Year"].astype(int)
    return df.sort_values(["Company", "Year"])

df = load_data()

# ---------- SIDEBAR CONTROLS ----------
st.sidebar.title("⚙️ Forecast Controls")

company = st.sidebar.selectbox("Select Company", sorted(df["Company"].unique()),
                                index=sorted(df["Company"].unique()).index("AMZN")
                                if "AMZN" in df["Company"].unique() else 0)

scenario = st.sidebar.radio("Scenario", ["Worst Case", "Base Case", "Best Case"], index=1)
scenario_multiplier = {"Worst Case": 0.5, "Base Case": 1.0, "Best Case": 1.3}[scenario]

years_of_history_for_cagr = st.sidebar.slider(
    "Years of history used to calculate growth rate", 3, 10, 5
)

manual_growth_override = st.sidebar.checkbox("Manually set growth rate instead")
if manual_growth_override:
    manual_growth = st.sidebar.slider("Custom annual revenue growth (%)", -20, 60, 10) / 100

forecast_years = 3

# ---------- FILTER COMPANY DATA ----------
company_df = df[df["Company"] == company].copy()
company_df = company_df.sort_values("Year")

latest_year = company_df["Year"].max()
history_window = company_df[company_df["Year"] > latest_year - years_of_history_for_cagr]

# ---------- CALCULATE HISTORICAL CAGR ----------
def calc_cagr(series):
    series = series.dropna()
    series = series[series > 0]  # CAGR needs positive start/end values
    if len(series) < 2:
        return 0.05  # fallback assumption: 5% growth if data insufficient
    start, end = series.iloc[0], series.iloc[-1]
    periods = len(series) - 1
    if periods == 0 or start <= 0:
        return 0.05
    return (end / start) ** (1 / periods) - 1

revenue_cagr = calc_cagr(history_window["Revenue"])
growth_rate = manual_growth if manual_growth_override else revenue_cagr * scenario_multiplier

# ---------- CALCULATE HISTORICAL MARGINS (AVERAGES) ----------
gross_margin = (company_df["Gross Profit"] / company_df["Revenue"]).mean()
ebitda_margin = (company_df["EBITDA"] / company_df["Revenue"]).mean()
net_margin = (company_df["Net Income"] / company_df["Revenue"]).mean()
ocf_margin = (company_df["Cash Flow from Operating"] / company_df["Revenue"]).mean()

# ---------- BUILD FORECAST ----------
last_actual_revenue = company_df.loc[company_df["Year"] == latest_year, "Revenue"].values[0]

forecast_rows = []
revenue = last_actual_revenue
for i in range(1, forecast_years + 1):
    year = latest_year + i
    revenue = revenue * (1 + growth_rate)
    gross_profit = revenue * gross_margin
    ebitda = revenue * ebitda_margin
    net_income = revenue * net_margin
    operating_cash_flow = revenue * ocf_margin
    forecast_rows.append({
        "Year": year, "Revenue": revenue, "Gross Profit": gross_profit,
        "EBITDA": ebitda, "Net Income": net_income,
        "Cash Flow from Operating": operating_cash_flow, "Type": "Forecast"
    })

forecast_df = pd.DataFrame(forecast_rows)
actual_df = company_df[["Year", "Revenue", "Gross Profit", "EBITDA", "Net Income",
                          "Cash Flow from Operating"]].copy()
actual_df["Type"] = "Actual"

combined = pd.concat([actual_df, forecast_df], ignore_index=True)

# ---------- HEADER ----------
st.title("📊 3-Year Revenue, Profitability & Cash Flow Forecast")
st.caption(f"Company: **{company}**  |  Scenario: **{scenario}**  |  "
           f"Assumed annual revenue growth: **{growth_rate*100:.1f}%**")

# ---------- KEY METRICS ----------
col1, col2, col3, col4 = st.columns(4)
final_forecast = forecast_df.iloc[-1]
col1.metric(f"Revenue ({int(final_forecast['Year'])})", f"${final_forecast['Revenue']:,.0f}M",
            f"{((final_forecast['Revenue']/last_actual_revenue)-1)*100:.1f}% vs last actual")
col2.metric(f"EBITDA ({int(final_forecast['Year'])})", f"${final_forecast['EBITDA']:,.0f}M")
col3.metric(f"Net Income ({int(final_forecast['Year'])})", f"${final_forecast['Net Income']:,.0f}M")
col4.metric(f"Operating Cash Flow ({int(final_forecast['Year'])})",
            f"${final_forecast['Cash Flow from Operating']:,.0f}M")

# ---------- CHARTS ----------
st.subheader("Revenue: Actual vs Forecast")
st.line_chart(combined.set_index("Year")[["Revenue"]])

st.subheader("Profitability: Gross Profit, EBITDA & Net Income")
st.line_chart(combined.set_index("Year")[["Gross Profit", "EBITDA", "Net Income"]])

st.subheader("Operating Cash Flow: Actual vs Forecast")
st.line_chart(combined.set_index("Year")[["Cash Flow from Operating"]])

# ---------- DATA TABLE ----------
st.subheader("Full Forecast Table")
display_df = combined.copy()
for col in ["Revenue", "Gross Profit", "EBITDA", "Net Income", "Cash Flow from Operating"]:
    display_df[col] = display_df[col].round(0)
st.dataframe(display_df.set_index("Year"), use_container_width=True)

# ---------- AUTO-GENERATED INSIGHTS ----------
def generate_insights():
    insights = []

    # 1. Growth profile
    if growth_rate > 0.15:
        insights.append(
            f"📈 **High-growth profile:** {company}'s forecasted revenue growth "
            f"({growth_rate*100:.1f}%/yr) is well above typical market growth, "
            f"driven by strong historical momentum."
        )
    elif growth_rate > 0.05:
        insights.append(
            f"📊 **Moderate, steady growth:** {company}'s forecasted revenue growth "
            f"({growth_rate*100:.1f}%/yr) reflects stable, mature-business performance "
            f"rather than explosive expansion."
        )
    else:
        insights.append(
            f"⚠️ **Slow/flat growth:** {company}'s forecasted revenue growth "
            f"({growth_rate*100:.1f}%/yr) is low — worth investigating whether this is "
            f"cyclical or a longer-term trend before committing budgets."
        )

    # 2. Profit efficiency: gap between EBITDA margin and Net margin
    margin_gap = ebitda_margin - net_margin
    if margin_gap > 0.15:
        insights.append(
            f"💡 **Large gap between EBITDA margin ({ebitda_margin*100:.1f}%) and Net "
            f"margin ({net_margin*100:.1f}%):** a significant portion of operating profit "
            f"is consumed by depreciation, interest, or taxes before it reaches the bottom "
            f"line — worth a closer look at capital structure or capex intensity."
        )
    else:
        insights.append(
            f"✅ **Efficient profit conversion:** EBITDA margin ({ebitda_margin*100:.1f}%) "
            f"and Net margin ({net_margin*100:.1f}%) are close, meaning most operating "
            f"profit flows through to actual net income."
        )

    # 3. Cash quality: OCF margin vs Net margin
    if ocf_margin > net_margin * 1.3:
        insights.append(
            f"💰 **Strong cash conversion:** Operating Cash Flow margin "
            f"({ocf_margin*100:.1f}%) is notably higher than Net Profit margin "
            f"({net_margin*100:.1f}%), suggesting high-quality, cash-backed earnings — "
            f"a positive signal for liquidity and reinvestment capacity."
        )
    elif ocf_margin < net_margin * 0.7:
        insights.append(
            f"🔍 **Cash conversion lags reported profit:** Operating Cash Flow margin "
            f"({ocf_margin*100:.1f}%) is lower than Net Profit margin "
            f"({net_margin*100:.1f}%) — worth checking working capital or non-cash "
            f"income items before relying on net income alone."
        )

    # 4. Scenario spread — show the range across Worst/Base/Best on this year's revenue
    worst_growth = revenue_cagr * 0.5
    best_growth = revenue_cagr * 1.3
    worst_rev = last_actual_revenue * (1 + worst_growth) ** forecast_years
    best_rev = last_actual_revenue * (1 + best_growth) ** forecast_years
    spread_pct = ((best_rev - worst_rev) / worst_rev) * 100 if worst_rev > 0 else 0
    insights.append(
        f"🎯 **Scenario range:** By {latest_year + forecast_years}, projected revenue "
        f"ranges from **${worst_rev:,.0f}M (Worst Case)** to **${best_rev:,.0f}M (Best Case)** "
        f"— a spread of {spread_pct:.0f}%, showing how sensitive the 3-year outlook is to "
        f"growth assumptions."
    )

    return insights

st.subheader("🧠 Auto-Generated Insights")
for insight in generate_insights():
    st.info(insight)

# ---------- ASSUMPTIONS (for judges to see your methodology) ----------
with st.expander("📌 Model Assumptions & Methodology"):
    st.write(f"""
    - **Revenue growth rate** used: {growth_rate*100:.1f}% per year
      (based on {years_of_history_for_cagr}-year historical CAGR of {revenue_cagr*100:.1f}%,
      adjusted by the **{scenario}** multiplier of {scenario_multiplier}x)
    - **Average Gross Margin**: {gross_margin*100:.1f}% of revenue
    - **Average EBITDA Margin**: {ebitda_margin*100:.1f}% of revenue
    - **Average Net Profit Margin**: {net_margin*100:.1f}% of revenue
    - **Average Operating Cash Flow Margin**: {ocf_margin*100:.1f}% of revenue
    - All margins are calculated from {company}'s full historical dataset
      ({int(company_df['Year'].min())}–{int(latest_year)}) and held constant
      into the forecast period, which is a standard simplifying assumption
      in early-stage FP&A models.
    """)

st.caption("Built for EFOS Global Finance Hackathon 2026 — Case 2: Revenue Forecasting & Profitability")
