import streamlit as st
import pandas as pd

# 📌 와이드 화면 설정
st.set_page_config(page_title="Kongsberg Service Calculator", layout="wide")

# 📌 요율 정의
remote_rates = {
    "System Engineer - NT": 258,
    "System Engineer - OT": 333,
    "System Specialist - NT": 290,
    "System Specialist - OT": 378
}

service_rates = {
    "Service Engineer - Inhouse - NT": 207,
    "Service Engineer - Inhouse - OT": 260,
    "Service Engineer - Inhouse - Travel": 164,
    "System Engineer - Inhouse - NT": 228,
    "System Engineer - Inhouse - OT": 287,
    "System Engineer - Inhouse - Travel": 180,
    "Service Engineer - Onboard - Day": 3104,
    "Service Engineer - Onboard - OT": 297,
    "System Engineer - Onboard - Day": 3428,
    "System Engineer - Onboard - OT": 329,
    "Service Engineer - Onboard - Travel": 164,
    "System Engineer - Onboard - Travel": 180
}

# 📌 제목
st.title("🛠️ Kongsberg Service Calculator")

# 📌 서비스 종류 선택
service_type = st.radio("Choose Service Type", ["Remote Support", "Service Rate"])

# 📌 Scope of Work 입력
with st.expander("📝 Scope of Work", expanded=True):
    scope = st.text_area("Write a summary or notes regarding the job scope...", placeholder="e.g., Remote radar tuning")

# 📌 작업 라인 수 선택
num_lines = st.number_input("How many work lines do you want to input?", min_value=1, max_value=20, value=3, step=1)

# 📌 타입 리스트와 요율
if service_type == "Remote Support":
    type_options = list(remote_rates.keys())
    rate_table = remote_rates
else:
    type_options = list(service_rates.keys())
    rate_table = service_rates

st.subheader("🔧 Work Input")

# 📌 사용자 입력 받기
work_data = []
for i in range(num_lines):
    cols = st.columns([3, 5, 2])
    with cols[0]:
        work_type = st.selectbox(f"Type {i+1}", type_options, key=f"type_{i}")
    with cols[1]:
        description = st.text_input(f"Description {i+1}", placeholder="e.g., Remote radar tuning", key=f"desc_{i}")
    with cols[2]:
        hours = st.number_input(f"{'Hours' if service_type == 'Remote Support' else 'Days'} {i+1}", min_value=0, value=0, step=1, key=f"hour_{i}")

    work_data.append({
        "Type": work_type,
        "Description": description,
        "Hours" if service_type == "Remote Support" else "Days": hours
    })

# 📌 계산 버튼
if st.button("🔍 Calculate Total Cost"):
    df = pd.DataFrame(work_data)
    df["Unit Rate (USD)"] = df["Type"].map(rate_table)
    
    time_column = "Hours" if service_type == "Remote Support" else "Days"
    df["Cost (USD)"] = df["Unit Rate (USD)"] * df[time_column]

    st.subheader("💲 Cost Breakdown")
    st.table(df)  # 복사 가능 정적 테이블

    total = df["Cost (USD)"].sum()
    st.success(f"✅ **Total Cost: ${total:,.2f} USD**")

    if scope.strip():
        st.subheader("📋 Scope of Work")
        st.markdown(f"> {scope}")
