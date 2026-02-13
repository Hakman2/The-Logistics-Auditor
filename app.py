import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Veridi Logistics Audit",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Veridi Logistics - Delivery Performance Audit")
st.markdown("An executive dashboard analyzing delivery accuracy and customer sentiment.")

# ---------------- Load Data ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("master_dataset.csv")
    return df

df = load_data()

# ---------------- Sidebar Filter ----------------
st.sidebar.header("Filters")

selected_state = st.sidebar.selectbox(
    "Select State",
    ["All"] + sorted(df["customer_state"].dropna().unique())
)

if selected_state != "All":
    df = df[df["customer_state"] == selected_state]

# ---------------- KPIs ----------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

total_orders = len(df)
late_orders = len(df[df["delivery_status"] == "Late"])
late_percentage = (late_orders / total_orders) * 100 if total_orders > 0 else 0
avg_delay = df["days_difference"].mean()

col1.metric("Total Orders", total_orders)
col2.metric("Late Orders (%)", f"{late_percentage:.2f}%")
col3.metric("Average Delay (Days)", f"{avg_delay:.2f}")

st.divider()

# ---------------- Late Deliveries by State ----------------
st.subheader("🚨 Late Deliveries by State")

state_late = (
    df[df["delivery_status"] == "Late"]
    .groupby("customer_state")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

fig1 = plt.figure()
state_late.plot(kind="bar")
plt.ylabel("Number of Late Orders")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.divider()

# ---------------- Delay vs Review ----------------
st.subheader("⭐ Delivery Delay vs Review Score")

clean_df = df.dropna(subset=["days_difference", "review_score"])

fig2 = plt.figure()
plt.scatter(clean_df["days_difference"], clean_df["review_score"])
plt.xlabel("Delay (Days)")
plt.ylabel("Review Score")
plt.title("Delay Impact on Customer Satisfaction")
st.pyplot(fig2)

st.divider()

# ---------------- Candidate's Choice ----------------
st.subheader("🎯 Delivery Promise Accuracy (Candidate’s Choice)")

df["absolute_delay"] = df["days_difference"].abs()

accuracy_state = (
    df.dropna(subset=["absolute_delay"])
    .groupby("customer_state")["absolute_delay"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig3 = plt.figure()
accuracy_state.plot(kind="bar")
plt.ylabel("Average Absolute Delay (Days)")
plt.xticks(rotation=45)
plt.title("Top States by Delivery Estimate Error")
st.pyplot(fig3)
