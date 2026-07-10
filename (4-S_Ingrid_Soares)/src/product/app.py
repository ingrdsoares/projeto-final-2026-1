import streamlit as st
import requests
import pandas as pd
import time

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Purple Team AI Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Purple Team AI Orchestrator")
st.markdown("### Automated Security Validation for Linux")

# Sidebar for control
st.sidebar.header("Control Panel")
auto_fix_enabled = st.sidebar.checkbox("Enable Auto-Remediation (Closed-Loop)", value=False)

if st.sidebar.button("🚀 Run Full Validation Cycle"):
    with st.spinner("Agent is orchestrating attacks and verifying detections..."):
        try:
            # Use the auto_fix parameter
            params = {"auto_fix": auto_fix_enabled}
            response = requests.post(f"{API_URL}/validate-all", params=params)
            if response.status_code == 200:
                st.success("Validation cycle complete!")
                st.session_state['coverage'] = response.json()
            else:
                st.error("API Error occurred during validation.")
        except Exception as e:
            st.error(f"Connection failed: {e}")

# Main Area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ MITRE ATT&CK Coverage Map")
    
    # Get current coverage
    try:
        response = requests.get(f"{API_URL}/coverage")
        if response.status_code == 200:
            coverage = response.json()
        else:
            coverage = {}
    except:
        coverage = {}

    if not coverage:
        st.info("No data available. Run the validation cycle to populate the map.")
    else:
        # Prepare data for the heatmap
        data = []
        for ttp, status in coverage.items():
            data.append({
                "TTP": ttp, 
                "Status": status, 
                "Color": "🟢" if status == "DETECTED" else "🔴"
            })
        
        df = pd.DataFrame(data)
        
        # Custom rendering for the heatmap
        for index, row in df.iterrows():
            st.markdown(f"**{row['TTP']}**: {row['Color']} {row['Status']}")

    st.divider()
    st.subheader("🧠 Agent Reasoning Log")
    try:
        res_log = requests.get(f"{API_URL}/reasoning")
        if res_log.status_code == 200:
            logs = res_log.json().get("logs", [])
            if logs:
                st.text_area("Thought Process", value="\n".join(logs), height=300)
            else:
                st.info("No reasoning logs available. Run a cycle first.")
        else:
            st.error("Could not retrieve logs.")
    except:
        st.error("API connection failed.")

with col2:
    st.subheader("🛠️ Quick Actions")
    ttp_to_sim = st.selectbox("Select TTP to Simulate", ["T1543.002", "T1548.001", "T1070.004", "T1082", "T1041"])
    
    if st.button("Simulate Attack"):
        with st.spinner("Simulating..."):
            try:
                res = requests.post(f"{API_URL}/simulate", json={"ttp_id": ttp_to_sim})
                st.write(res.json().get("result", "Unknown result"))
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("Check Detection"):
        with st.spinner("Checking..."):
            try:
                res = requests.get(f"{API_URL}/check/{ttp_to_sim}")
                status = res.json()
                if status.get("detected"):
                    st.success(f"Detected! Alert ID: {status.get('alert_id')}")
                else:
                    st.warning("Not detected by SIEM.")
            except Exception as e:
                st.error(f"Error: {e}")

    st.divider()
    st.subheader("🔊 Noise Analysis")
    if st.button("Test False Positives"):
        with st.spinner("Analyzing noise..."):
            try:
                res = requests.post(f"{API_URL}/test-noise")
                noise_data = res.json()
                for action, status in noise_data.items():
                    color = "🔴" if status == "FALSE POSITIVE" else "🟢"
                    st.write(f"{color} {action}: {status}")
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.caption("Purple Team AI Orchestrator - Final Project 2026-1")
