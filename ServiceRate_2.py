import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Kongsberg Service Calculator", layout="centered")

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
    </style>
""", unsafe_allow_html=True)

# --- RATE TABLE ---
remote_rates = {
    "System Engineer - NT": 258,
    "System Engineer - OT": 333,
    "System Specialist - NT": 290,
    "System Specialist - OT": 378,
}

service_rates = {
    "Service Engineer - Inhouse (NT)": 207,
    "Service Engineer - Inhouse (OT)": 260,
    "Service Engineer - Inhouse (Travel)": 164,
    "System Engineer - Inhouse (NT)": 228,
    "System Engineer - Inhouse (OT)": 287,
    "System Engineer - Inhouse (Travel)": 180,
    "Service Engineer - Onboard (Day)": 3104,
    "Service Engineer - Onboard (OT)": 297,
    "System Engineer - Onboard (Day)": 3428,
    "System Engineer - Onboard (OT)": 329,
    "Service Engineer - Onboard (Travel)": 164,
    "System Engineer - Onboard (Travel)": 180,
}

# --- SIDEBAR ---
st.title("💻 Kongsberg Service Calculator")

# --- Service Type ---
service_type = st.radio("Choose Service Type", ["Remote Support", "Service Rate"], horizontal=False)

# --- Scope of Work ---
st.markdown("### 📝 Scope of Work")
scope = st.text_area("Write a summary or notes regarding the job scope...", placeholder="e.g., Remote radar tuning")

# --- Number of lines ---
num_lines = st.number_input("How many work lines do you want to input?", min_value=1, max_value=10, value=3, step=1)

# --- Work Inputs ---
st.markdown("### 🛠️ Work Input")
data = []

rate_options = remote_rates if service_type == "Remote Support" else service_rates

def get_unit_label(type_str):
    return "Days" if "(Day)" in type_str else "Hours"

for i in range(num_lines):
    cols = st.columns([4, 4, 1])
    with cols[0]:
        type_ = st.selectbox(f"Type {i+1}", options=list(rate_options.keys()), key=f"type_{i}")
    with cols[1]:
        description = st.text_input(f"Description {i+1}", placeholder="e.g., Remote tuning", key=f"desc_{i}")
    with cols[2]:
        unit_label = get_unit_label(type_)
        time = st.number_input(f"{unit_label} {i+1}", min_value=0, step=1, key=f"time_{i}")

    data.append({"Type": type_, "Description": description, "Unit": unit_label, "Time": time})

# --- Calculate ---
if st.button("🔍 Calculate Total Cost"):
    df = pd.DataFrame(data)
    df["Unit Rate"] = df["Type"].apply(lambda x: rate_options.get(x, 0))
    df["Cost (USD)"] = df["Time"] * df["Unit Rate"]

    st.markdown("#### 📊 Calculation Result")
    st.dataframe(df[["Type", "Description", "Unit", "Time", "Unit Rate", "Cost (USD)"]], use_container_width=False)

    st.markdown("---")
    st.markdown(f"**📝 Scope of Work Summary:** {scope if scope else 'No scope provided.'}")