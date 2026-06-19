# src/dashboard.py
import streamlit as st
import requests

# 1. Configure the browser tab layout
st.set_page_config(page_title="Factory Control Room", layout="wide")

st.title("🏭 Industrial Predictive Maintenance Mission Control")
st.markdown("Enter real-time machinery telemetry numbers directly below to evaluate the active operational risk layer.")
st.markdown("---")

# 2. Setup structural columns for direct numerical inputs
control_column_left, control_column_right = st.columns(2)

# Left Column: User can manually type identifying and thermal metrics
with control_column_left:
    st.subheader(" Asset Identity & Thermal State")
    
    machine_id = st.number_input("Registered Machine ID (1 - 10000)", min_value=1, max_value=10000, value=1, step=1)
    
    air_temp = st.number_input("Ambient Air Temperature (Kelvin)", min_value=1.0, value=298.1, step=0.1, format="%.1f")
    
    proc_temp = st.number_input("Process Core Temperature (Kelvin)", min_value=1.0, value=308.6, step=0.1, format="%.1f")

# Right Column: User can manually type performance data 
with control_column_right:
    st.subheader(" Kinematic Performance & Mechanical Wear")
    
    rotational_speed = st.number_input("Spindle Rotational Speed (RPM)", min_value=0.0, value=1500.0, step=10.0, format="%.1f")
    
    torque = st.number_input("Drive Assembly Torque (Nm)", min_value=0.0, value=40.0, step=0.5, format="%.1f")
    
    tool_wear = st.number_input("Accumulated Tool Wear Time (Minutes)", min_value=0.0, max_value=300.0, value=50.0, step=1.0, format="%.1f")

st.markdown("---")

# 3. Dynamic diagnostics pipeline transmission button
if st.button(" Run Real-Time Diagnostics Pipeline", use_container_width=True):
    
    # Package parameters into JSON mapping structure
    telemetry_packet = {
        "machine_id": int(machine_id),
        "air_temperature": float(air_temp),
        "process_temperature": float(proc_temp),
        "rotational_speed": float(rotational_speed),
        "torque": float(torque),
        "tool_wear": float(tool_wear)
    }
    
    st.markdown("### 🔍 Live Diagnostic Telemetry Analysis")
    
    try:
        # Shoot data to our FastAPI engine port
        api_url = "http://127.0.0.1:8000/predict"
        server_response = requests.post(api_url, json=telemetry_packet)
        
        if server_response.status_code == 200:
            result_data = server_response.json()
            
            prediction = result_data["failure_prediction"]
            probability = result_data["failure_probability"] * 100
            resolved_type = result_data["machine_type_resolved"]
            alert_status = result_data["status_alert"]
            
            # UI Alert configuration logic
            if prediction == 1:
                st.error(f" CRITICAL EMERGENCE DETECTED: {alert_status}")
                st.metric(label="Calculated Breakdown Risk Probability", value=f"{probability:.2f}%", delta="CRITICAL DANGER")
            else:
                st.success(f" MECHANICAL INTEGRITY SECURE: {alert_status}")
                st.metric(label="Calculated Breakdown Risk Probability", value=f"{probability:.2f}%", delta="SAFE OPERATIONAL LIMITS")
            
            st.info(f" **Database Sync:** SQLite asset registry verified Machine #{machine_id} as a **Grade Class '{resolved_type}'** asset profile.")
            
        else:
            st.error(f"FastAPI Server rejected payload: {server_response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error(" Transmission Link Broken. Your Streamlit dashboard cannot communicate with the AI model. Ensure your FastAPI server is running on port 8000 in your other terminal panel!")