import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Compressor Health Dashboard",
    page_icon="⚙️",
    layout="wide"
)

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("⚙️ Compressor Health Dashboard")
st.write("Monitor compressor parameters and health status.")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("compressor_data.csv")

# Convert Timestamp to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# -----------------------------
# Dataset Overview
# -----------------------------
st.subheader("Dataset Overview")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Records", len(df))

with col2:
    st.metric("Compressors", df["Compressor_ID"].nunique())

# -----------------------------
# Compressor Selector
# -----------------------------
st.subheader("Select Compressor")

selected_compressor = st.selectbox(
    "Choose Compressor",
    df["Compressor_ID"].unique()
)

# -----------------------------
# Filter Data
# -----------------------------
filtered_df = df[df["Compressor_ID"] == selected_compressor]

# -----------------------------
# Get Latest Reading
# -----------------------------
latest = filtered_df.iloc[-1]

pressure = latest["Pressure_bar"]
temperature = latest["Temperature_C"]
vibration = latest["Vibration_mm_s"]
running_hours = latest["Running_Hours"]

# -----------------------------
# Health Score Calculation
# -----------------------------
health_score = 100
alerts = []
recommendation = "No action required."

# Temperature Check
if temperature > 80:
    health_score -= 20
    alerts.append("High Temperature")
    recommendation = "Check cooling system."

# Vibration Check
if vibration > 4:
    health_score -= 30
    alerts.append("High Vibration")
    recommendation = "Inspect bearings."

# Pressure Check
if pressure < 10 or pressure > 15:
    health_score -= 20
    alerts.append("Pressure Abnormal")
    recommendation = "Inspect pressure system."

# Running Hours Check
if running_hours > 2000:
    health_score -= 10
    alerts.append("Maintenance Due")
    recommendation = "Schedule preventive maintenance."

# -----------------------------
# Determine Health Status
# -----------------------------
if health_score >= 90:
    status = "Healthy"
elif health_score >= 70:
    status = "Monitor"
elif health_score >= 50:
    status = "Warning"
else:
    status = "Critical"

# -----------------------------
# Health Metrics
# -----------------------------
st.subheader("🏥 Compressor Health")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Health Score", f"{health_score}%")

with col2:
    st.metric("Status", status)

with col3:
    st.metric("Running Hours", int(running_hours))

# -----------------------------
# Alerts Section
# -----------------------------
st.subheader("🚨 Alerts")

if alerts:
    for alert in alerts:
        st.warning(alert)

    st.info(f"Recommended Action: {recommendation}")
else:
    st.success("No alerts. Compressor operating normally.")

# -----------------------------
# Display Latest Values
# -----------------------------
st.subheader("📋 Latest Sensor Readings")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Pressure (bar)", pressure)

with col2:
    st.metric("Temperature (°C)", temperature)

with col3:
    st.metric("Vibration (mm/s)", vibration)

# -----------------------------
# Data Table
# -----------------------------
st.subheader(f"Data for {selected_compressor}")

st.dataframe(filtered_df)

# -----------------------------
# Pressure Trend
# -----------------------------
st.subheader("📈 Pressure Trend")

pressure_fig = px.line(
    filtered_df,
    x="Timestamp",
    y="Pressure_bar",
    title=f"{selected_compressor} Pressure Over Time"
)

st.plotly_chart(pressure_fig, use_container_width=True)

# -----------------------------
# Temperature Trend
# -----------------------------
st.subheader("🌡️ Temperature Trend")

temp_fig = px.line(
    filtered_df,
    x="Timestamp",
    y="Temperature_C",
    title=f"{selected_compressor} Temperature Over Time"
)

st.plotly_chart(temp_fig, use_container_width=True)

# -----------------------------
# Vibration Trend
# -----------------------------
st.subheader("🔧 Vibration Trend")

vibration_fig = px.line(
    filtered_df,
    x="Timestamp",
    y="Vibration_mm_s",
    title=f"{selected_compressor} Vibration Over Time"
)

st.plotly_chart(vibration_fig, use_container_width=True)