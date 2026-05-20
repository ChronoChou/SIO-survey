import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. 網頁基本設定 (特務機關風格)
st.set_page_config(page_title="SIO 情資收集系統", page_icon="🦉", layout="centered")

# =====================================================================
# 🖼️ 頂部主視覺：手繪家族貼圖 (完美大圖置中)
# =====================================================================
if os.path.isfile("sio_3.png"):
    left_co, cent_co, right_co = st.columns([1, 5, 1])
    with cent_co:
        st.image("sio_3.png", use_container_width=True)

# 2. 標題與視覺營造 (網頁主標題置中)
st.markdown("<h1 style='text-align: center; padding-top: 10px;'>🦉 家族旅遊意向調查 🦉</h1>", unsafe_allow_html=True)
st.markdown("---")

# 3. 定義資料庫路徑
csv_file = "sio_responses.csv"

# =====================================================================
# ⚙️ 管理員緊急控制台 (安全密碼鎖防護版 + 組織Logo進駐)
# =====================================================================
with st.sidebar:
    # 🦉 戰略部署：將組織 Logo 安置在側邊欄最頂端，做為官方標章
    if os.path.isfile("sio_logo.png"):
        st.image("sio_logo.png", use_container_width=True)
        st.markdown("---")
        
    st.write("⚙️ **管理員緊急控制台**")
    
    # 在側邊欄加上一個獨立的密碼輸入框
    sidebar_password = st.text_input("🔑 請輸入控制台授權密碼：", type="password", key="sidebar_pwd")
    
    # 只有密碼正確，才會顯示出「重置/清空」按鈕
    if sidebar_password == "sio2026":
        st.warning("⚠️ 警告：高階控制權限已開啟")
        
        # 密碼正確才現形的毀滅按鈕
        if st.button("🚨 執行！重置/清空雲端資料庫"):
            if os.path.isfile(csv_file):
                os.remove(csv_file)
                st.success("舊資料庫已成功粉碎清空！")
                st.rerun()
            else:
                st.info("資料庫目前本來就是空的。")
                
    # 如果輸入錯誤密碼，給予警示
    elif sidebar_password != "":
        st.error("🔒 密碼錯誤，控制台已鎖定。")

# 4. 問卷表單設計
with st.form(key="sio_survey_form", clear_on_submit=True):
    agent_name = st.text_input(
        "請輸入您的匿名代號：", 
        placeholder="例如：apple-1、banana-2..."
    )
    st.markdown("---")    
    
    # 1. 營地選擇 (單選題)
    camp_choice = st.radio(
        "1. 預計冬天再舉辦一次露營，地點同樣是小路露營區",
        ["贊成", "有困難"]
    )
    
    # 2. 天數偏好 (單選題)
    Days_preference = st.radio(
        "2. 承上，希望安排幾天幾夜",
        ["三天兩夜", "兩天一夜"]
    )

    # 3. 暑假型式 (單選題)
    Summer_preference = st.radio(
        "3. 是否希望在暑假期間再安排一次家族旅遊，願意的話希望包棟還是露營?",
        ["包棟", "高海拔露營(氣溫涼爽)", "沒意願"]
    )
    
    # 4. 展開式複選題（地區選擇）
    st.write("4. 承上，希望舉辦的地區？(可複選)")
    travel_options = ["北部", "中部", "南部", "東部", "離島-澎湖"]
    selected_places = []
    
    for option in travel_options:
        if st.checkbox(option, key=f"check_{option}"):
            selected_places.append(option)
            
    # 5. 暑假天數 (單選題)
    Summerday_preference = st.radio(
        "5. 承上，如有意願希望安排天數?",
        ["三天兩夜", "兩天一夜"]
    )

    # 6. 住宿預算 (單選題)
    Price_preference = st.radio(
        "6. 因包棟價位較高，約露營的1.5-2.5倍，故可接受家族旅遊住宿每人每晚價位(元/晚*人)為?",
        ["1500 ~ 2000", "2000 ~ 2500", "2500 ~ 3000", "3000 ~ 3500", "無所謂😎🤘🔥"]
    )
    
    # 規則說明排版優化
    st.markdown("---")
    st.caption("💡 **補充說明：**")
    st.caption("1. **包棟費用計算方式**：「每晚包棟費用」除以「總人頭數」，大人算 1 人頭，小孩算 0.5 人頭。")
    st.caption("2. **露營費用計算方式**：比照初露，各自負擔所屬營地費及設備租用費。")
    st.caption("※ *範例：育德家兩大人兩小孩，故需乘 3。*")
    st.markdown("---")
    
    # 自由意見回饋 (簡答題)
    suggestions = st.text_area("對於家族旅遊有什麼建議，請在此留言：")
    
    # 送出按鈕
    submit_button = st.form_submit_button(label="🚀 發送情資 (Submit)")

# 5. 後台資料處理邏輯 (當使用者按送出時)
if submit_button:
    # 建立單筆紀錄資料
    survey_data = {
        "填寫時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "匿名代號": agent_name,
        "冬天是否再小路舉辦露營": camp_choice,
        "冬天舉辦天數": Days_preference,
        "暑假舉辦型式": Summer_preference,
        "旅遊地點": ", ".join(selected_places),  # 💡 Bug 已修正：確實儲存成員勾選的地點清單
        "暑假家旅天數": Summerday_preference,
        "可接受價位": Price_preference,
        "留言建議": suggestions
    }
    
    df_new = pd.DataFrame([survey_data])
    
    if not os.path.isfile(csv_file):
        df_new.to_csv(csv_file, index=False, encoding="utf-8-sig")
    else:
        df_new.to_csv(csv_file, mode='a', header=False, index=False, encoding="utf-8-sig")
        
    st.session_state["submitted"] = True
    st.session_state["submitted_agent"] = agent_name
    st.rerun()

# =====================================================================
# 🎈 網頁重整完畢後，安全噴氣球
# =====================================================================
if st.session_state.get("submitted", False):
    st.balloons()
    current_agent = st.session_state.get("submitted_agent", "")
    st.success(f"💥 情資已加密傳輸！感謝特務 【{current_agent}】 協助本次 SIO 調查！")
    st.session_state["submitted"] = False
    st.session_state["submitted_agent"] = ""

# =====================================================================
# 🔐 SIO 首席執行官秘密通道 (高階授權密碼鎖安全版)
# =====================================================================
st.markdown("---")
st.write("### 🔐 管理員專屬情資下載區")

admin_password = st.text_input("🔑 請輸入 SIO 高階授權密碼鎖解鎖通道：", type="password", key="download_pwd")

if admin_password == "sio2026":
    st.success("🔓 執行官身分驗證成功！中央數據庫通道已開啟。")
    
    if os.path.isfile(csv_file):
        try:
            df_download = pd.read_csv(csv_file, encoding="utf-8-sig")
            csv_data = df_download.to_csv(index=False).encode('utf-8-sig')
            
            st.download_button(
                label="📥 下載最新問卷數據 (SIO_Responses.csv)",
                data=csv_data,
                file_name=f"SIO_Responses_{datetime.now().strftime('%m%d')}.csv",
                mime="text/csv",
                key="download_secret_button"
            )
            
            st.write("📊 目前即時情資預覽：")
            st.dataframe(df_download)
        except Exception as e:
            st.error("⚠️ 偵測到雲端 CSV 資料結構損壞！請使用左側側邊欄的『緊急控制台』按鈕清空重置。")
    else:
        st.info("💡 目前資料庫尚無數據 (填寫完成並按送出後，下載按鈕就會出現在這喔！)")
        
elif admin_password != "":
    st.error("🚨 警告：密碼錯誤！非授權特務試圖入侵。")