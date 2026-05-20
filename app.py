import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. 網頁基本設定 (特務機關風格)
st.set_page_config(page_title="SIO 情資收集系統", page_icon="🦉", layout="centered")

# 2. 標題與視覺營造
st.title("🦉 SIO 隱密情報局 // 任務問卷")
st.subheader("【絕密】下一階段露營行動意向調查 (PDC-2026-TECH-001)")
st.markdown("---")

# 3. 問卷表單設計
with st.form(key="sio_survey_form", clear_on_submit=True):
    st.write("### 📥 第一階段：特務基本資料")
    
    # 填寫人姓名 (下拉選單，防止打錯字方便後續分析)
    agent_name = st.selectbox(
        "請選擇您的特務代號/稱呼：",
        ["Ann Sui Kuo", "Liu Lian Chou", "Lao Oua Kuo", "Hang Hea Hu", "姐呼", "其他家族成員"]
    )
    
    st.write("---")
    st.write("### 🏔️ 第二階段：戰略營地部署投票")
    
    # 營地選擇 (單選題)
    camp_choice = st.radio(
        "下次高海拔避暑行動，您傾向哪一個營地？(海拔 1000m+)",
        ["春露茶園 (1100m) - 觀星與無敵雲海", "密靜莊園 (1200m) - 森林系獨立空間", "非比尋常 (1100m) - 厚實草皮包區"]
    )
    
    # 飲食偏好 (複選題)
    food_preference = st.multiselect(
        "針對新成員 Hang Hea Hu 的熱能海鮮補給，您最期待吃到什麼？(可多選)",
        ["招牌泰式烤蝦 🦐", "鹽烤大草蝦 🦐", "蒜蓉啤酒蝦 🍺", "不挑食，執行官烤的都吃！"]
    )
    
    # 自由意見回饋 (簡答題)
    suggestions = st.text_area("對於這次『群牛亂舞』行動的辛酸或未來建議，請在此留下您的機密留言：")
    
    # 4. 送出按鈕
    submit_button = st.form_submit_button(label="🚀 發送情資 (Submit)")

# 5. 後台資料處理邏輯 (當使用者按送出時)
if submit_button:
    # 建立單筆紀錄資料夾
    survey_data = {
        "填寫時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "特務代號": agent_name,
        "偏好營地": camp_choice,
        "期待蝦料理": ", ".join(food_preference),
        "特務意見": suggestions
    }
    
    # 資料存檔路徑 (本機測試時會存成 Excel)
    csv_file = "sio_responses.csv"
    df_new = pd.DataFrame([survey_data])
    
    if not os.path.isfile(csv_file):
        df_new.to_csv(csv_file, index=False, encoding="utf-8-sig")
    else:
        df_new.to_csv(csv_file, mode='a', header=False, index=False, encoding="utf-8-sig")
        
    # 畫面上顯示成功訊息 (帶有 SIO 特有的吃瓜幽默)
    st.balloons()
    st.success(f"感謝特務 {agent_name}！情資已加密傳輸至 SIO 中央數據庫。")