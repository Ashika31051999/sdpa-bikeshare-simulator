import streamlit as st
import copy
from rules import pence_to_pounds
from bikeshare import BikeShare

st.set_page_config(page_title="Bike-Share Operations Dashboard", layout="wide", page_icon="🚲")

# Header section
st.title("🚲 City Bike-Share Logistics Dashboard")
st.write("An interactive web utility designed to optimize fleet rebalancing and workshop repairs.")
st.markdown("---")

# Maintain the running simulation engine state across button clicks safely
if "sim" not in st.session_state:
    st.session_state.sim = BikeShare()
    st.session_state.logs = []

sim = st.session_state.sim

# Top-level key metrics bar
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric(label="💳 Active Bank Balance", value=pence_to_pounds(sim.get_cash()))
with m_col2:
    st.metric(label="📅 Current Simulation Day", value=f"Day {sim.get_day()}")
with m_col3:
    st.metric(label="🛠️ Workshop Repair Queue", value=f"{sim.get_workshop()} Bikes")

# Input interactive panel splits
st.subheader("⚙️ Plan Daily Fleet Allocations")
col_left, col_right = st.columns([1, 2])

with col_left:
    st.write("**Maintenance & Logistics Constraints**")
    # Repairs slider locked dynamically to available inventory
        # Secure validation fix for empty workshop queues
    if sim.get_workshop() > 0:
        repairs = st.slider("Select bikes to repair today:", 0, sim.get_workshop(), 0)
    else:
        st.caption("ℹ️ No bikes currently in the workshop to repair.")
        repairs = 0
    # Van move step slider capped at assignment constraint
    m_count = st.slider("Select number of van moves planned (0-3):", 0, 3, 0)

moves = []
with col_right:
    if m_count > 0:
        st.write("**Configure Van Transport Routing Directions**")
        for i in range(m_count):
            r_col1, r_col2, r_col3 = st.columns(3)
            with r_col1:
                orig = r_col1.selectbox(f"Move #{i+1} Origin", ["A", "B", "C"], key=f"o_{i}")
            with r_col2:
                dest = r_col2.selectbox(f"Move #{i+1} Destination", ["A", "B", "C"], key=f"d_{i}")
            with r_col3:
                count = r_col3.number_input(f"Move #{i+1} Bike Volume", 1, 10, 1, key=f"c_{i}")
            moves.append((orig, dest, count))
    else:
        st.info("💡 Adjust the slider on the left if you need to schedule van rebalancing steps for today.")

st.markdown("---")

# Execution action button
if st.button("🚀 Process Operations Turn Step", type="primary", use_container_width=True):
    try:
        # Provide a generic basic trip mapping for demo visualization frames
        mock_trips = [("A", "B", 5), ("B", "C", 3), ("C", "A", 2)]
        
        # Step through the real back-end engine you built
        record = sim.step({"moves": moves, "repairs": repairs}, mock_trips)
        st.session_state.logs.append(record)
        st.success(f"Day processed successfully! Day Closing Balance: {pence_to_pounds(record['closing_cash'])}")
        st.rerun()
    except ValueError as e:
        st.error(f"❌ Fleet Action Rejected: {e}")

# Live active station trackers
st.subheader("📍 Real-Time Station Status")
s_cols = st.columns(3)
current_bikes = sim.get_bikes()

for idx, (station_id, bike_count) in enumerate(current_bikes.items()):
    with s_cols[idx]:
        st.metric(label=f"Station {station_id} Inventory", value=f"{bike_count} Bikes Docked")
        st.progress(min(1.0, max(0.0, bike_count / 20.0)))

# Summary history reports tracking panel
if st.session_state.logs:
    st.subheader("📊 Financial and Commuter History Logs")
    st.dataframe(st.session_state.logs, use_container_width=True)
