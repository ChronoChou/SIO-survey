import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. 網頁基本設定 (特務機關風格)
st.set_page_config(page_title="SIO 情資收集系統", page_icon="🦉", layout="centered")

# =====================================================================
# 🖼️ 頂部視覺完美大升級：雙徽章夾標題流
# =====================================================================
# 建立三個欄位，比例為 1 : 4 : 1（左右放圖，中間放文字）
col1, col2, col3 = st.columns([1, 4, 1])

# 1. 左邊第一欄：放 SIO 藍色貓頭鷹徽章
with col1:
    if os.path.isfile("sio_logo.png"):
        st.image("sio_logo.png", use_container_width=True)

# 2. 中間第二欄：放核心大標題 (設定置中對齊，讓字夾在兩張圖正中間)
with col2:
    st.markdown(
        "<h1 style='text-align: center; padding-top: 15px; font-size: 36px;'>家族旅遊意向調查</h1>", 
        unsafe_allow_html=True
    )

# 3. 右邊第三欄：放手繪家族大頭貼 (sio_3.png)
with col3:
    if os.path.isfile("sio_3.png"):
        st.image("sio_3.png", use_container_width=True)

st.markdown("---")
# =====================================================================

# 3. 定義資料庫路徑
csv_file = "sio_responses.csv"

# =====================================================================
# 🛠️ 萬能修復手段：如果之前的 CSV 壞掉了，提供一個緊急重置按鈕
# =====================================================================
# =====================================================================
# ⚙️ 管理員緊急控制台 (安全密碼鎖防護版)
# =====================================================================
with st.sidebar:
    st.write("⚙️ **管理員緊急控制台**")
    
    # 1. 在側邊欄加上一個獨立的密碼輸入框
    sidebar_password = st.text_input("🔑 請輸入控制台授權密碼：", type="password", key="sidebar_pwd")
    
    # 2. 只有密碼正確，才會顯示出「重置/清空」按鈕
    if sidebar_password == "sio2026":  # 您可以改成跟下載區一樣的密碼，或是設更難的
        st.warning("⚠️ 警告：高階控制權限已開啟")
        
        # 密碼正確才現形的毀滅按鈕
        if st.button("🚨 執行！重置/清空雲端資料庫"):
            if os.path.isfile(csv_file):
                os.remove(csv_file)
                st.success("舊資料庫已成功粉碎清空！")
                st.rerun()
            else:
                st.info("資料庫目前本來就是空的。")
                
    # 3. 如果輸入錯誤密碼，給予警示
    elif sidebar_password != "":
        st.error("🔒 密碼錯誤，控制台已鎖定。")

# 4. 問卷表單設計
with st.form(key="sio_survey_form", clear_on_submit=True):
    agent_name = st.text_input(
        "請選擇您的匿名代號：",placeholder="例如：apple-1、banana-2..." # 這是輸入框內淡淡的提示字，點擊打字就會消失
    )
    st.write("--------------------------------------------------------")    
    # 營地選擇 (單選題)
    camp_choice = st.radio(
        "1. 預計冬天再舉辦一次露營，地點同樣是小路露營區",
        ["贊成", "有困難"]
    )
    
    # 飲食偏好 (複選題)
    Days_preference = st.radio(
        "2. 承上，希望安排幾天幾夜",
        ["三天兩夜", "兩天一夜"]
    )

    Summer_preference = st.radio(
        "3. 是否希望在暑假期間再安排一次家族旅遊，願意的話希望包棟還是露營?",
        ["包棟", "高海拔露營(氣溫涼爽)", "沒意願"]
    )
    # =====================================================================
    # 🗂️ 展開式複選題（像 radio 一樣展開，但可以複選）
    # =====================================================================
    st.write("4. 承上，希望舉辦的地區？(可複選)")
    
    # 先把您要展開的選項用清單（List）列出來
    travel_options = ["北部", "中部", "南部", "東部", "離島-澎湖"]
    
    # 建立一個空清單，用來裝成員最後「有勾選」的答案
    selected_places = []
    
    # 用迴圈把選項一個個變成 radio 風格的勾選框
    for option in travel_options:
        # 如果成員勾選了，這個變數就會是 True
        if st.checkbox(option, key=f"check_{option}"):
            selected_places.append(option) # 將有勾選的塞進答案庫
            
    # =====================================================================
    Summerday_preference = st.radio(
        "4. 承上，如有意願希望安排天數?",
        ["三天兩夜", "兩天一夜"]
    )


    Price_preference = st.radio(
        "5. 因包棟價位較高，約露營的1.5-2.5倍，故可接受家族旅遊住宿每人每晚價位(元/晚*人)為?",
        ["1500 ~ 2000", "2000 ~ 2500", "2500 ~ 3000", "3000 ~ 3500", "無所謂😎🤘🔥"]
    )
    st.write("補充：")
    st.write("1. 包棟費用計算方式：「每晚包棟費用」除以「總人頭數」，大人算1人頭，小孩算0.5人頭")
    st.write("2. 露營費用計算方式：比照初露，各自負擔所屬營地費及設備租用費")
    st.write("範例：育德家兩大人兩小孩，故需乘3")
    st.write("----------------------------------")
    # 自由意見回饋 (簡答題)
    suggestions = st.text_area("對於家族旅遊有什麼建議，請在此留言：")
    
    # 4. 送出按鈕
    submit_button = st.form_submit_button(label="🚀 發送情資 (Submit)")

# 5. 後台資料處理邏輯 (當使用者按送出時)
if submit_button:
    # 建立單筆紀錄資料
    survey_data = {
        "匿名代號": agent_name,
        "冬天是否再小路舉辦露營": camp_choice,
        "冬天舉辦天數": Days_preference,
        "暑假舉辦型式": Summer_preference,
        "暑假家旅天數": Summerday_preference,
        "旅遊地點": travel_options,
        "可接受價位": Price_preference,
        "留言建議": suggestions
    }
    
    df_new = pd.DataFrame([survey_data])
    
    if not os.path.isfile(csv_file):
        df_new.to_csv(csv_file, index=False, encoding="utf-8-sig")
    else:
        df_new.to_csv(csv_file, mode='a', header=False, index=False, encoding="utf-8-sig")
        
    # 💡 戰術修正：不當場噴氣球，而是先在雲端筆記本寫下「已成功」
    st.session_state["submitted"] = True
    st.rerun() # 安心重新整理網頁

# =====================================================================
# 🎈 網頁重整完畢後，檢查筆記本，這時候再噴氣球就不會被擦掉了！
# =====================================================================
if st.session_state.get("submitted", False):
    st.balloons()
    st.success("情資已加密傳輸至 SIO 中央數據庫，感謝您的協助！")
    # 噴完後把筆記本擦乾淨，避免每次重整網頁都重複噴氣球
    st.session_state["submitted"] = False

# =====================================================================
# 🔐 SIO 首席執行官秘密通道 (移到 if 外部，讓它隨時顯示在網頁最下方)
# =====================================================================
st.markdown("---")
st.write("### 🔐 管理員專屬情資下載區")

# 檢查雲端主機裡是否已經有成員填寫的 CSV 檔
if os.path.isfile(csv_file):
    try:
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
    except Exception as e:
        st.error("⚠️ 偵測到雲端 CSV 資料結構損壞！請使用左側側邊欄的『緊急控制台』按鈕清空重置。")
else:
    st.info("💡 目前資料庫尚無數據 (填寫完成並按送出後，下載按鈕就會出現在這喔！)")