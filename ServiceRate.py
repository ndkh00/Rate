import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Service Calculator", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
        .element-container:has(.stButton) {
            padding-top: 1rem;
        }
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stTextArea textarea {
            font-size: 14px;
        }
        .stSelectbox>div>div>div>div {
            font-size: 12px;
        }
        div[data-baseweb="select"] div {
            font-size: 12px !important;
            max-width: 100%;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .stDataFrameContainer {
            max-width: 700px;
        }
        .stSelectbox {
            width: 100% !important;
        }
        .input-label {
            font-size: 11px !important;
            margin-top: 1.5rem;
            margin-bottom: 0.2rem;
        }
        .small-note {
            font-size: 11px;
            color: gray;
        }
    </style>
""", unsafe_allow_html=True)

# --- RATE TABLE ---
remote_rates = {
    "System Eng. - NT": 258,
    "System Eng. - OT": 333,
    "System Specialist - NT": 290,
    "System Specialist - OT": 378,
}

service_rates = {
    "Service Eng. - Inhouse (NT)": 207,
    "Service Eng. - Inhouse (OT)": 260,
    "Service Eng. - Inhouse (Travel)": 164,
    "System Eng. - Inhouse (NT)": 228,
    "System Eng. - Inhouse (OT)": 287,
    "System Eng. - Inhouse (Travel)": 180,
    "Service Eng. - Onboard (Day)": 3104,
    "Service Eng. - Onboard (OT)": 297,
    "System Eng. - Onboard (Day)": 3428,
    "System Eng. - Onboard (OT)": 329,
    "Service Eng. - Onboard (Travel)": 164,
    "System Eng. - Onboard (Travel)": 180,
}

# --- SIDEBAR ---
st.title("💻 Service Calculator")

# --- Service Type ---
service_type = st.radio("Choose Service Type", ["Remote Support", "Service Rate"], horizontal=True)

# --- Reference Links ---
st.markdown("### 📄 Reference Rate Documents")
st.markdown("""
- [KM-KD Connected Remote Service Rates (Valid 1 Jan 2025 v1.3)](https://masterx.sharepoint.com/sites/Konnect/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FKonnect%2FShared%20Documents%2FKM%20KD%20Service%20Rates%2FKM%2DKD%2DConnected%2DRemote%2DService%2DRates%2DValid%201Jan%2D2025%2DV1%2E3%2Epdf&parent=%2Fsites%2FKonnect%2FShared%20Documents%2FKM%20KD%20Service%20Rates)
- [KM-KD Korea System and Integration Service Rates (Valid 1 Jan 2025 v1.3)](https://masterx.sharepoint.com/sites/Konnect/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FKonnect%2FShared%20Documents%2FKM%20KD%20Service%20Rates%2FKM%2DKD%2DKorea%2DSystem%2Dand%2DIntegration%2DService%2DRates%2DValid%2D1Jan%2D2025%2DV1%2E3%2Epdf&parent=%2Fsites%2FKonnect%2FShared%20Documents%2FKM%20KD%20Service%20Rates)
""")

# --- Scope of Work ---
st.markdown("### 📝 Scope of Work")
scope = st.text_area("Write a summary or notes regarding the job scope...", placeholder="e.g., Remote radar tuning")

# --- Number of lines ---
num_lines = st.number_input("How many work lines do you want to input?", min_value=1, max_value=10, value=3, step=1)

# --- Work Inputs ---
st.markdown("### 🧾 Work Input <span class='small-note'>(add soft80 in description if hours is preferred to be unseen)</span>", unsafe_allow_html=True)
data = []

rate_options = remote_rates if service_type == "Remote Support" else service_rates

# Determine unit label based on type
def get_unit_label(type_str):
    return "Days" if "(Day)" in type_str else "Hours"

for i in range(num_lines):
    cols = st.columns([4, 3.5, 2.2])
    with cols[0]:
        st.markdown(f"<div class='input-label'>Pos {i+1}</div>", unsafe_allow_html=True)
        pos = st.selectbox(f"Pos {i+1} Label", options=list(rate_options.keys()), key=f"pos_{i}", label_visibility="collapsed")
    with cols[1]:
        st.markdown(f"<div class='input-label'>Description {i+1}</div>", unsafe_allow_html=True)
        description = st.text_input(f"Description {i+1} Label", placeholder="e.g., Remote tuning", key=f"desc_{i}", label_visibility="collapsed")
    with cols[2]:
        st.markdown(f"<div class='input-label'>Hour {i+1}</div>", unsafe_allow_html=True)
        time = st.number_input(f"Time {i+1} Label", min_value=0, step=1, key=f"time_{i}", format="%d", label_visibility="collapsed")

    data.append({"Pos": pos, "Description": description, "Unit": get_unit_label(pos), "Time": time})

# --- Calculate ---
if st.button("🔍 Calculate Total Cost"):
    df = pd.DataFrame(data)
    df["Unit Rate"] = df["Pos"].apply(lambda x: rate_options.get(x, 0))
    df["Cost (USD)"] = df["Time"] * df["Unit Rate"]

    st.markdown("#### 📊 Calculation Result")
    st.dataframe(df[["Pos", "Description", "Unit", "Time", "Unit Rate", "Cost (USD)"]])

    st.markdown("---")
    st.markdown(f"**📝 Scope of Work Summary:** {scope if scope else 'No scope provided.'}")
