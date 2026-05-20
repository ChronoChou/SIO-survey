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

# 3. 定義資料庫路徑
csv_file = "sio_responses.csv"

# =====================================================================
# 🛠️ 萬能修復手段：如果之前的 CSV 壞掉了，提供一個緊急重置按鈕
# =====================================================================
with st.sidebar:
    st.write("⚙️ **管理員緊急控制台**")
    if st.button("⚠️ 重置/清空雲端資料庫"):
        if os.path.isfile(csv_file):
            os.remove(csv_file)
            st.success("舊資料庫已成功粉碎清空！")
            st.rerun()
        else:
            st.info("資料庫目前本來就是空的。")

# 4. 問卷表單設計
with st.form(key="sio_survey_form", clear_on_submit=True):
    
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
        ["1500 ~ 2000", "2000 ~ 2500", "2500 ~ 3000", "3000 ~ 3500", ""]
    )
    # =====================================================================
    # 📝 獨立一行的補充說明與虛線區
    # =====================================================================
    # 使用 markdown 的 ----------------- 會自動變成一條漂亮的灰色實線
    st.markdown("---") 
    
    # 使用 st.caption 會自動讓文字變成「小字、灰色」，非常適合拿來當備註或補充說明
    st.caption("💡 **補充說明：**")
    st.caption("1. **包棟費用計算方式**：「每晚包棟費用」除以「總人頭數」，大人算 1 人頭，小孩算 0.5 人頭。")
    st.caption("2. **露營費用計算方式**：比照初露，各自負擔所屬營地費及設備租用費。")
    st.caption("※ *以育德當範例，兩大人兩小孩，故需乘 3。*")
    # =====================================================================



    # 自由意見回饋 (簡答題)
    suggestions = st.text_area("對於家族旅遊有什麼建議，請在此留言：")
    
    # 4. 送出按鈕
    submit_button = st.form_submit_button(label="🚀 發送情資 (Submit)")

# 5. 後台資料處理邏輯 (當使用者按送出時)
if submit_button:
    # 建立單筆紀錄資料
    survey_data = {
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