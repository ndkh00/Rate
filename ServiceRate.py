import streamlit as st
import pandas as pd

# 요율 정의
rates = {
    "System Engineer - NT": 258,
    "System Engineer - OT": 333,
    "System Specialist - NT": 290,
    "System Specialist - OT": 378,
}

# 제목
st.title("💻 Kongsberg Remote Service Cost Calculator")
st.subheader("📝 Input work lines:")

# 라인 수 입력
num_rows = st.number_input("How many work lines do you want to input?", min_value=1, max_value=10, value=3)

input_data = []

# 입력 폼
for i in range(int(num_rows)):
    st.text(f"Line {i + 1}")
    
    # 🔧 폭 조정: Type 2.2 / Description 4 / Hours 0.6
    cols = st.columns([2.2, 4, 0.6])

    with cols[0]:
        type_selected = st.selectbox("Type", list(rates.keys()), key=f"type_{i}")

    with cols[1]:
        description_text = st.text_input("Description", placeholder="e.g., Remote radar tuning", key=f"desc_{i}")

    with cols[2]:
        # 좁은 공간에 적합한 정수 입력 (버튼 제거 효과 없음)
        hour = st.number_input("Hours", min_value=0, step=1, value=0, key=f"hour_{i}")

    input_data.append({
        "Type": type_selected,
        "Description": description_text,
        "Hours": hour
    })

# 결과 계산
if st.button("🔍 Calculate Total Cost"):
    df = pd.DataFrame(input_data)
    df["Cost (USD)"] = df.apply(lambda row: rates[row["Type"]] * row["Hours"], axis=1)

    st.subheader("💰 Calculation Result:")
    st.dataframe(df)

    total = df["Cost (USD)"].sum()
    st.success(f"✅ Total Cost: ${total:,.2f}")
