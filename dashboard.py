import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from scraper.web_scraper import scrape_competitors


st.set_page_config(page_title="Advanced Competitor Dashboard", layout="wide")

st.title("🚀 Advanced Competitor Benchmarking Dashboard")

DATA_PATH = "data/raw_data.csv"

# ---------- LOAD DATA ----------
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame(columns=["name", "service", "price", "engagement"])

# ---------- SIDEBAR CONTROLS ----------
st.sidebar.header("⚙ Controls")

if st.sidebar.button("🔄 Run Scraper"):
    scrape_competitors()
    st.sidebar.success("Scraper executed. Refresh page.")
    st.stop()

# ---------- ADD NEW DATA (FORM INPUT) ----------
st.sidebar.subheader("➕ Add New Competitor")

with st.sidebar.form("add_competitor_form"):
    name = st.text_input("Competitor Name")
    service = st.text_input("Service / Product")
    price = st.number_input("Price (£)", min_value=0.0, step=1.0)
    engagement = st.number_input("Engagement", min_value=0, step=100)

    submitted = st.form_submit_button("Add Data")

    if submitted:
        if name and service:
            new_row = {
                "name": name,
                "service": service,
                "price": price,
                "engagement": engagement
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_PATH, index=False)
            st.sidebar.success("✅ Data added successfully")
        else:
            st.sidebar.error("❌ Name and Service are required")

# ---------- FILE UPLOAD INPUT ----------
st.sidebar.subheader("📤 Upload CSV")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    uploaded_df = pd.read_csv(uploaded_file)
    df = pd.concat([df, uploaded_df], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    st.sidebar.success("📁 File uploaded and merged")

# ---------- FILTERS ----------
st.subheader("🔎 Filters")

col1, col2 = st.columns(2)

with col1:
    selected_competitor = st.selectbox(
        "Select Competitor",
        ["All"] + df["name"].unique().tolist()
    )

with col2:
    max_price = st.slider(
        "Max Price (£)",
        min_value=int(df["price"].min()) if not df.empty else 0,
        max_value=int(df["price"].max()) if not df.empty else 100,
        value=int(df["price"].max()) if not df.empty else 100
    )

if selected_competitor != "All":
    df = df[df["name"] == selected_competitor]

df = df[df["price"] <= max_price]

# ---------- KPIs ----------
st.subheader("📊 Key Metrics")

k1, k2, k3 = st.columns(3)

k1.metric("Average Price", f"£{df['price'].mean():.2f}" if not df.empty else "N/A")
k2.metric("Max Engagement", int(df["engagement"].max()) if not df.empty else "N/A")
k3.metric("Total Competitors", df["name"].nunique())

# ---------- DATA TABLE ----------
st.subheader("📋 Data Table")
st.dataframe(df, use_container_width=True)

# ---------- CHARTS ----------
st.subheader("📈 Visual Analysis")

st.bar_chart(df.set_index("name")["price"])
st.line_chart(df.set_index("name")["engagement"])

# ---------- DOWNLOAD ----------
st.subheader("⬇ Download Data")

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "competitor_data.csv", "text/csv")

