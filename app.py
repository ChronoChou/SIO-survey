import streamlit as st
import pandas as pd
import os
import base64  # 💡 隆重請出二進位加密套件
from datetime import datetime

# 1. 網頁基本設定 (特務機關風格)
st.set_page_config(page_title="SIO 情資收集系統", page_icon="🦉", layout="centered")

# =====================================================================
# 🔒 SIO 官方防偽浮水印（內嵌白底遮罩防遮擋版）
# =====================================================================
if os.path.isfile("sio_logo.png"):
    with open("sio_logo.png", "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        /* 直接鎖定主底層，利用 linear-gradient 在圖片上方塗一層 90% 的透明白漆 */
        .stApp {{
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.90), rgba(255, 255, 255, 0.90)), 
                url("data:image/png;base64,{b64_string}") !important;
            background-repeat: no-repeat !important;
            background-position: center 38% !important; /* 控制浮水印上下位置 */
            background-size: 420px !important;          /* 控制浮水印大小 */
            background-attachment: fixed !important;    /* 固定背景不隨滾輪滑動 */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# =====================================================================
# 🖼️ SIO 官方徽章置頂 (完美置中版)
# =====================================================================
if os.path.isfile("sio_3.png"):
    # 建立三個左右對稱的虛擬欄位，比例為 1 : 2 : 1 
    # 中間的欄位比例較大(2)，用來放圖片；左右兩邊(1)負責當隱形推手
    left_co, cent_co, right_co = st.columns([1, 2, 1])
    
    # 叫 Streamlit 把圖片畫在中間那一欄
    with cent_co:
        st.image("sio_3.png", use_container_width=True)

# 2. 標題與視覺營造 (啟動 Flexbox 磁力吸盤，徹底解決 Emoji 干擾造成的偏心問題)
st.markdown(
    """
    <div style="
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        width: 100%; 
        padding: 10px 0;
    ">
        <span style="font-size: 26px; visibility: hidden;">🦉</span>
        <h1 style="
            font-size: 26px; 
            margin: 0; 
            text-align: center; 
            flex-grow: 1; 
            letter-spacing: 1px;
            font-weight: bold;
        ">🦉 家族旅遊意向調查 🦉</h1>
        <span style="font-size: 26px; visibility: hidden;">🦉</span>
    </div>
    """, 
    unsafe_allow_html=True
)

# 3. 定義資料庫路徑
csv_file = "sio_responses.csv"

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
        "請選擇您的匿名代號：", placeholder="例如：apple-1、banana-2..." 
    )
    st.write("--------------------------------------------------------")    
    
    # 1. 營地選擇 (單選題)
    camp_choice = st.radio(
        "**1. 預計冬天再舉辦一次露營，地點同樣是小路露營區**",
        ["贊成", "有困難"]
    )
    
    # 2. 天數偏好
    Days_preference = st.radio(
        "**2. 承上，希望安排幾天幾夜**",
        ["三天兩夜", "兩天一夜"]
    )

    # 3. 暑假舉辦形式
    Summer_preference = st.radio(
        "**3. 是否希望在暑假期間再安排一次家族旅遊，願意的話希望包棟還是露營?**",
        ["包棟", "高海拔露營(氣溫涼爽)", "沒意願"]
    )
    
    # 4. 複選題題目大小鎖定
    st.markdown("<p style='font-size: 16px; font-weight: bold; margin-bottom: -5px;'>4. 承上，希望舉辦的地區？(可複選)</p>", unsafe_allow_html=True)
    
    travel_options = ["北部", "中部", "南部", "東部", "離島-澎湖"]
    selected_places = []
    
    for option in travel_options:
        if st.checkbox(option, key=f"check_{option}"):
            selected_places.append(option)
            
    # 5. 暑假天數
    Summerday_preference = st.radio(
        "**5. 承上，如有意願希望安排天數?**",
        ["三天兩夜", "兩天一夜"]
    )

    # 6. 住宿預算
    Price_preference = st.radio(
        "**6. 因包棟價位較高，約露營的1.5-2.5倍，故可接受家族旅遊住宿每人每晚價位(元/晚*人)為?**",
        ["1500 ~ 2000", "2000 ~ 2500", "2500 ~ 3000", "3000 ~ 3500", "無所謂😎🤘🔥"]
    )
    
    # =====================================================================
    # 🎨 關鍵校正點：補充說明的字體大小與題目一模一樣(16px)，並換上深灰色調
    # =====================================================================
    st.write("") # 留一空行排版較漂亮
    st.markdown(
        """
        <div style="color: #556677; font-size: 16px; line-height: 1.6;">
            <strong>💡 補充說明：</strong><br>
            1. <strong>包棟費用計算方式</strong>：「每晚包棟費用」除以「總人頭數」，大人算 1 人頭，小孩算 0.5 人頭。<br>
            2. <strong>露營費用計算方式</strong>：比照初露，各自負擔所屬營地費及設備租用費。<br>
            <strong>※ 範例</strong>：育德家兩大人兩小孩，故需乘 3。
        </div>
        """, 
        unsafe_allow_html=True
    )
    # =====================================================================
    
    st.write("----------------------------------")
    # 自由意見回饋 (簡答題)
    suggestions1 = st.text_area("對於初露有什麼建議，請在此留言：", placeholder="一定要寫喔!建議根鼓勵的話都可以~")

    suggestions2 = st.text_area("對於家族旅遊有什麼建議，請在此留言：",placeholder="一定要寫喔!建議根鼓勵的話都可以~")
    
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
        "旅遊地點": ", ".join(selected_places),  # 💡 Bug已修正：確實儲存成員勾選的地點清單
        "暑假家旅天數": Summerday_preference,
        "可接受價位": Price_preference,
        "初露留言建議": suggestions1,
        "家旅留言建議": suggestions2
    }
    
    df_new = pd.DataFrame([survey_data])
    
    if not os.path.isfile(csv_file):
        df_new.to_csv(csv_file, index=False, encoding="utf-8-sig")
    else:
        df_new.to_csv(csv_file, mode='a', header=False, index=False, encoding="utf-8-sig")
        
    # 戰術修正：不當場噴氣球，而是先在雲端筆記本寫下「已成功」
    st.session_state["submitted"] = True
    st.session_state["submitted_agent"] = agent_name
    st.rerun() # 安心重新整理網頁

# =====================================================================
# 🎈 網頁重整完畢後，檢查筆記本，這時候再噴氣球就不會被擦掉了！
# =====================================================================
if st.session_state.get("submitted", False):
    st.balloons()
    current_agent = st.session_state.get("submitted_agent", "")
    st.success(f"💥 情資已加密傳輸！感謝特務 【{current_agent}】 協助本次 SIO 調查！")
    # 噴完後把筆記本擦乾淨，避免每次重整網頁都重複噴氣球
    st.session_state["submitted"] = False
    st.session_state["submitted_agent"] = ""

# =====================================================================
# 📊 管理員專屬情資下載區 (已全面開放給全體成員瀏覽與下載)
# =====================================================================
st.markdown("---")
st.write("### 📊 全體成員情資下載與預覽區")

# 檢查雲端主機裡是否已經有成員填寫的 CSV 檔
if os.path.isfile(csv_file):
    try:
        # 讀取目前的問卷數據
        df_download = pd.read_csv(csv_file, encoding="utf-8-sig")
        
        # 將資料轉換為 Streamlit 下載按鈕需要的格式
        csv_data = df_download.to_csv(index=False).encode('utf-8-sig')
        
        # 建立下載按鈕 (任何人都可以直接點擊下載)
        st.download_button(
            label="📥 下載最新問卷數據 (SIO_Responses.csv)",
            data=csv_data,
            file_name=f"SIO_Responses_{datetime.now().strftime('%m%d')}.csv",
            mime="text/csv",
            key="download_public_button"
        )
        
        st.write("📊 目前即時情資預覽：")
        st.dataframe(df_download)
    except Exception as e:
        st.error("⚠️ 偵測到雲端 CSV 資料結構損壞！請聯絡首席執行官使用左側控制台清空重置。")
else:
    st.info("💡 目前資料庫尚無數據 (填寫完成並按送出後，大家就能在這裡看到即時數據囉！)")