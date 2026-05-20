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
    
    # 營地選擇 (單選題)
    camp_choice = st.radio(
        "1. 預計冬天再舉辦一次露營，地點同樣是小路露營區",
        ["贊成", "有困難"]
    )
    
    # 飲食偏好 (複選題)
    Days_preference = st.radio(
        "2. 希望安排幾天幾夜",
        ["三天兩夜", "兩天一夜"]
    )

    Summer_preference = st.radio(
        "3. 是否希望在暑假期間再安排一次家族旅遊，願意的話希望包棟還是露營?",
        ["包棟", "高海拔露營(氣溫涼爽)", "沒意願"]
    )

    Summerday_preference = st.radio(
        "4. 承上，如有意願希望安排天數?",
        ["三天兩夜", "兩天一夜"]
    )

    Price_preference = st.radio(
        "5. 因包棟價位較高，約露營的1.5-2.5倍，故可接受家族旅遊住宿(一晚)價位為?",
        ["比小路再便宜", "小路 * 1~1.5", "小路 * 1.5~2", "小路 * 2~2.5", "小路 * 2.5~3", "無所謂"]
    )
    
    # 自由意見回饋 (簡答題)
    suggestions = st.text_area("對於家族旅遊有什麼建議，請在此留言：")
    
    # 4. 送出按鈕
    submit_button = st.form_submit_button(label="🚀 發送情資 (Submit)")

# 5. 定義資料庫路徑
csv_file = "sio_responses.csv"

# 6. 後台資料處理邏輯 (當使用者按送出時)
if submit_button:
    # 建立單筆紀錄資料
    survey_data = {
        "填寫時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "冬天是否再小路舉辦露營": camp_choice,
        "冬天舉辦天數": Days_preference,
        "暑假舉辦型式": Summer_preference,
        "暑假家旅天數": Summerday_preference,
        "可接受價位": Price_preference,
        "留言建議": suggestions
    }
    
    df_new = pd.DataFrame([survey_data])
    
    if not os.path.isfile(csv_file):
        df_new.to_csv(csv_file, index=False, encoding="utf-8-sig")
    else:
        df_new.to_csv(csv_file, mode='a', header=False, index=False, encoding="utf-8-sig")
        
    st.balloons()
    # 修正點：移除未定義的 agent_name，改成泛用特務感謝詞
    st.success("情資已加密傳輸至 SIO 中央數據庫，感謝您的協助！")

# =====================================================================
# 🔐 SIO 首席執行官秘密通道 (移到 if 外部，讓它隨時顯示在網頁最下方)
# =====================================================================
st.markdown("---")
st.write("### 🔐 管理員專屬情資下載區")

# 檢查雲端主機裡是否已經有成員填寫的 CSV 檔
if os.path.isfile(csv_file):
    # 讀取目前的問卷數據
    df_download = pd.read_csv(csv_file, encoding="utf-8-sig")
    
    # 將資料轉換為 Streamlit 下載按鈕需要的格式
    csv_data = df_download.to_csv(index=False).encode('utf-8-sig')
    
    # 建立下載按鈕
    st.download_button(
        label="📥 下載最新問卷數據 (SIO_Responses.csv)",
        data=csv_data,
        file_name=f"SIO_Responses_{datetime.now().strftime('%m%d')}.csv",
        mime="text/csv",
        key="download_secret_button"
    )
    
    st.write("📊 目前即時情資預覽：")
    st.dataframe(df_download)
else:
    st.info("💡 目前資料庫尚無數據 (填寫完成並按送出後，下載按鈕就會出現在這喔！)")