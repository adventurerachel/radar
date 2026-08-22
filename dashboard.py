import json
from pathlib import Path

import pandas as pd
import streamlit as st

import plotly.express as px

DATA_FILE = Path("storage/history/dog_food_prices.jsonl")


st.set_page_config(
    page_title="Scrumbles Price Monitor",
    page_icon="🐕",
    layout="wide",
)


@st.cache_data
def load_data():
    records = []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                records.append(json.loads(line))

    return pd.DataFrame(records)


df = load_data()

df["date"] = pd.to_datetime(df["date"])

col_title, col_filter = st.columns([3, 1])

with col_title:
    st.title("🐕 Scrumbles Price Monitor")
    st.caption("Turkey Adult & Senior Dry Dog Food • 2kg")

with col_filter:
    date_range = st.selectbox(
        "Date range",
        ["Last 7 days", "Last 30 days", "Last 90 days", "All data"],
        index=0,
    )

latest_date = df["date"].max()

if date_range == "Last 7 days":
    start_date = latest_date - pd.Timedelta(days=6)
elif date_range == "Last 30 days":
    start_date = latest_date - pd.Timedelta(days=29)
elif date_range == "Last 90 days":
    start_date = latest_date - pd.Timedelta(days=89)
else:
    start_date = df["date"].min()

filtered_df = df[
    (df["date"] >= start_date)
    & (df["date"] <= latest_date)
].copy()

st.write(f"Loaded **{len(df)} observations**.")


# Make sure dates are treated as dates
latest = (
    df[df["date"] == latest_date]
    .sort_values("retailer")
)

st.header("Current Prices")
st.caption(f"Latest observations: {latest_date.strftime('%d %B %Y')}")

available_prices = latest.loc[
    latest["found"] == True,
    "effective_price"
].dropna()

best_price = available_prices.min() if not available_prices.empty else None

available_prices = latest.loc[
    latest["found"] == True,
    "effective_price"
].dropna()

best_price = available_prices.min() if not available_prices.empty else None

cols = st.columns(len(latest))

for col, (_, row) in zip(cols, latest.iterrows()):
    with col:
        retailer = row["retailer"]

        if row["found"]:
            price = row["effective_price"]

            if pd.notna(price):
                value = f"£{price:.2f}"
            else:
                value = "No price"

            availability = str(row["availability"]).lower()

            if availability == "in_stock":
                status = "✅ In stock"
            elif availability == "out_of_stock":
                status = "⚠️ Out of stock"
            elif availability == "unknown":
                status = "❓ Availability unknown"
            else:
                status = "❓ Unknown status"

        else:
            value = "Unavailable"
            status = "⚠️ No data"


        st.markdown(f"### {retailer.title()}")

        if row["found"]:
            price = row["effective_price"]
            
            if pd.notna(price):
                st.markdown(f"## £{price:.2f}")

                if price == best_price:
                    st.write("🏆 Best price")
            else:
                st.markdown("## No price")

            availability = str(row["availability"]).lower()

            if availability == "in_stock":
                st.write("✅ In stock")
            elif availability == "out_of_stock":
                st.write("⚠️ Out of stock")
            else:
                st.write("❓ Availability unknown")

            if row["promotion_active"]:
                promo_type = row["promo_type"]

                if pd.notna(promo_type):
                    st.write(f"🏷️ {promo_type}")
                else:
                    st.write("🏷️ Promotion")

        else:
            st.markdown("## Unavailable")
            st.write("⚠️ No data")

st.header("Price History")

st.caption("Effective price over time")


chart_data = (
    filtered_df[filtered_df["found"] == True]
    .copy()
)

chart_data = chart_data[
    ["date", "retailer", "effective_price"]
].dropna()

chart_data = chart_data.pivot_table(
    index="date",
    columns="retailer",
    values="effective_price",
    aggfunc="last",
)

st.line_chart(chart_data)

st.header("Promotion Summary")

st.caption("Promotional pricing across the monitoring period")


# One observation per retailer/day
promo_daily = (
    filtered_df.groupby(["retailer", "date"])
    .agg(
        found=("found", "max"),
        promotion_active=("promotion_active", "max"),
        effective_price=("effective_price", "last"),
        regular_price=("regular_price", "last"),
        promo_type=("promo_type", "last"),
    )
    .reset_index()
)


# Only consider days where we successfully found a price
promo_daily = promo_daily[promo_daily["found"] == True].copy()


# Calculate saving
promo_daily["saving_pct"] = (
    (promo_daily["regular_price"] - promo_daily["effective_price"])
    / promo_daily["regular_price"]
    * 100
)


promotion_summary = (
    promo_daily.groupby("retailer")
    .agg(
        days_with_price=("date", "count"),
        promo_days=("promotion_active", "sum"),
        average_saving_pct=("saving_pct", "mean"),
        biggest_saving_pct=("saving_pct", "max"),
    )
    .reset_index()
)


promotion_summary["promo_rate"] = (
    promotion_summary["promo_days"]
    / promotion_summary["days_with_price"]
    * 100
)


promotion_summary = promotion_summary[
    [
        "retailer",
        "days_with_price",
        "promo_days",
        "promo_rate",
        "average_saving_pct",
        "biggest_saving_pct",
    ]
]


promotion_summary = promotion_summary.rename(
    columns={
        "retailer": "Retailer",
        "days_with_price": "Days with price",
        "promo_days": "Promo days",
        "promo_rate": "Promo rate %",
        "average_saving_pct": "Avg saving %",
        "biggest_saving_pct": "Biggest saving %",
    }
)


# Round percentages
for column in [
    "Promo rate %",
    "Avg saving %",
    "Biggest saving %",
]:
    promotion_summary[column] = promotion_summary[column].round(1)


st.dataframe(
    promotion_summary,
    use_container_width=True,
    hide_index=True,
)

st.header("Price Competitiveness")

st.caption("How often each retailer offered the lowest price")


# One price per retailer per day
competitive_daily = (
    filtered_df[
        (filtered_df["found"] == True)
        & (filtered_df["effective_price"].notna())
    ]
    .groupby(["date", "retailer"])["effective_price"]
    .last()
    .reset_index()
)


# Find the lowest available price on each day
daily_min = (
    competitive_daily
    .groupby("date")["effective_price"]
    .min()
    .rename("daily_min_price")
    .reset_index()
)

competitive_daily = competitive_daily.merge(
    daily_min,
    on="date",
)

# A retailer is cheapest if its price equals
# the lowest price available that day
competitive_daily["is_cheapest"] = (
    competitive_daily["effective_price"]
    == competitive_daily["daily_min_price"]
)

# Summarise competitiveness by retailer
competitiveness = (
    competitive_daily
    .groupby("retailer")
    .agg(
        days_competing=("date", "count"),
        days_cheapest=("is_cheapest", "sum"),
        average_price=("effective_price", "mean"),
        lowest_price=("effective_price", "min"),
    )
    .reset_index()
)

competitiveness["win_rate"] = (
    competitiveness["days_cheapest"]
    / competitiveness["days_competing"]
    * 100
)

# Rename columns for display
competitiveness = competitiveness.rename(
    columns={
        "retailer": "Retailer",
        "days_competing": "Days competing",
        "days_cheapest": "Days cheapest",
        "win_rate": "Win rate %",
        "average_price": "Avg price",
        "lowest_price": "Lowest price",
    }
)

# Format values
competitiveness["Win rate %"] = (
    competitiveness["Win rate %"].round(1)
)

competitiveness["Avg price"] = (
    competitiveness["Avg price"].round(2)
)

competitiveness["Lowest price"] = (
    competitiveness["Lowest price"].round(2)
)


# Display chart and table side by side
col_chart, col_table = st.columns([35, 65])

with col_chart:
    st.subheader("Days Cheapest")

    chart_data = competitiveness.sort_values(
        "Days cheapest",
        ascending=True,
    )

    fig = px.bar(
        chart_data,
        x="Days cheapest",
        y="Retailer",
        orientation="h",
        text="Days cheapest",
    )

    fig.update_layout(
        xaxis_title="Days cheapest",
        yaxis_title="",
        showlegend=False,
        height=300,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

with col_table:
    st.subheader("Competitiveness")

    st.dataframe(
        competitiveness,
        use_container_width=True,
        hide_index=True,
    )

st.header("Monitor Health")

# Total monitoring period
monitor_start = filtered_df["date"].min()
monitor_end = filtered_df["date"].max()

total_days = (monitor_end - monitor_start).days + 1

st.caption(
    f"Monitoring period: {monitor_start.strftime('%d %B %Y')} "
    f"to {monitor_end.strftime('%d %B %Y')} "
    f"({total_days} days)"
)


# Calculate coverage by retailer
health = (
    filtered_df.groupby(["retailer", "date"])["found"]
    .max()
    .reset_index()
)

health_summary = (
    health.groupby("retailer")
    .agg(
        days_with_price=("found", "sum"),
    )
    .reset_index()
)

health_summary["days_without_price"] = (
    total_days - health_summary["days_with_price"]
)

health_summary["coverage"] = (
    health_summary["days_with_price"] / total_days * 100
)

health_summary = health_summary.sort_values(
    "coverage",
    ascending=False,
)

health_summary = health_summary.rename(
    columns={
        "retailer": "Retailer",
        "days_with_price": "Days with price",
        "days_without_price": "Days without price",
        "coverage": "Coverage %",
    }
)
st.dataframe(
    health_summary,
    use_container_width=True,
    hide_index=True,
)

st.header("Underlying Data")

st.dataframe(
    df,
    use_container_width=True,
)
