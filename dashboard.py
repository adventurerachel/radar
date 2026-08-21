import json
from pathlib import Path

import pandas as pd
import streamlit as st


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


st.title("🐕 Scrumbles Price Monitor")
st.caption("Turkey Adult & Senior Dry Dog Food • 2kg")

st.write(f"Loaded **{len(df)} observations**.")


# Make sure dates are treated as dates
df["source_date"] = pd.to_datetime(df["source_date"])


# Get the latest observation for each retailer
latest_date = df["source_date"].max()

latest = (
    df[df["source_date"] == latest_date]
    .sort_values("retailer")
)


st.header("Current Prices")
st.caption(f"Latest observations: {latest_date.strftime('%d %B %Y')}")


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
            else:
                st.markdown("## No price")

            availability = str(row["availability"]).lower()

            if availability == "in_stock":
                st.write("✅ In stock")
            elif availability == "out_of_stock":
                st.write("⚠️ Out of stock")
            else:
                st.write("❓ Availability unknown")

        else:
            st.markdown("## Unavailable")
            st.write("⚠️ No data")

st.header("Price History")

st.caption("Effective price over time")


chart_data = (
    df[df["found"] == True]
    .copy()
)

chart_data["date"] = pd.to_datetime(chart_data["date"])

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

st.header("Underlying Data")

st.dataframe(
    df,
    use_container_width=True,
)