import streamlit as st
import os
import base64
from datetime import datetime

# 1. 網頁基本設定 (特務機關成果報告風格)
st.set_page_config(page_title="胡搞SIO搞家族旅遊統計結果", page_icon="📊", layout="centered")

# =====================================================================
# 🔒 SIO 官方防偽浮水印（成果報告專用版）
# =====================================================================
if os.path.isfile("sio_6.png"):
    with open("sio_6.png", "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.92)), 
                url("data:image/png;base64,{b64_string}") !important;
            background-repeat: no-repeat !important;
            background-position: center 38% !important;
            background-size: 420px !important;
            background-attachment: fixed !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# =====================================================================
# 🖼️ SIO 官方徽章置頂
# =====================================================================
if os.path.isfile("sio_3.png"):
    left_co, cent_co, right_co = st.columns([1, 2, 1])
    with cent_co:
        st.image("sio_3.png", use_container_width=True)

# 2. 標題與視覺營造 (Flexbox 絕對居中對稱版)
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
        ">🦉 問卷統計結果 🦉</h1>
        <span style="font-size: 26px; visibility: hidden;">🦉</span>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown("<p style='text-align: center; color: #556677; font-size: 14px;'>胡搞SIO搞-WHO GOAL SIO GOAL | 數據提供時間：" + datetime.now().strftime("%Y-%m-%d") + "</p>", unsafe_allow_html=True)
st.markdown("---")

# =====================================================================
# 📊 第一部分：意向調查統計圖表展現
# =====================================================================
st.subheader("📊 各項數據統計結果")

# 功能函式：確保圖表置中且大小適中
def display_centered_chart(img_name, caption_text):
    if os.path.isfile(img_name):
        left, cent, right = st.columns([1, 12, 1])
        with cent:
            st.image(img_name, use_container_width=True)
            st.markdown(f"<p style='text-align: center; color: #778899; font-size: 13px; margin-top: -10px;'>{caption_text}</p>", unsafe_allow_html=True)
            st.write("")

display_centered_chart("P1.png", "圖一：冬天再次小路露營意願統計")
display_centered_chart("P2.png", "圖二：暑假家族旅遊類型與天數統計")
display_centered_chart("P3.png", "圖三：暑假家族旅遊天數與可接受預算統計")

st.markdown("---")

# =====================================================================
# 💬 第二部分：精美文字意見回饋
# =====================================================================
st.subheader("💬 家族真心話回饋")

# HTML 質感文字框樣式定義
def render_suggestion_box(title, feedback_list, border_color="#4A90E2"):
    html_content = f"""
    <div style="
        border-left: 5px solid {border_color}; 
        background-color: rgba(245, 247, 250, 0.8); 
        padding: 15px; 
        border-radius: 0 8px 8px 0; 
        margin-bottom: 20px;
    ">
        <h4 style="margin-top: 0; color: #2C3E50; font-weight: bold;">{title}</h4>
        <ol style="margin-bottom: 0; padding-left: 20px; color: #34495E; line-height: 1.7; font-size: 15px;">
    """
    for item in feedback_list:
        # 將換行符號轉成網頁換行標籤
        safe_item = item.replace("\n", "<br>")
        html_content += f"<li style='margin-bottom: 12px;'>{safe_item}</li>"
        
    html_content += "</ol></div>"
    st.markdown(html_content, unsafe_allow_html=True)


# --- 整理後的 A 資料集 ---
feedback_A = [
    "我覺得不錯",
    "大家都很棒呢！",
    "嘻嘻嘻嘻嘻",
    "這趟旅程很開心好棒👍🏻",
    "我應該要準備肉品的覺得肉品有點少",
    "據我看到的個人想法，看到幾乎家綾姐承包了很多東西，不管是吃的用的，都幫大家盡量減少支付費用的金額，姐也說我們都是一家人家裡有什麼能帶就帶，減少支出幫大家省錢，東西多到塞兩車才載完，很感謝姐、姐夫幫大家省扣扣。"
    "我覺得因為這樣幫忙省很多也幫忙買午餐飯捲，怕小朋友餓到、大家餓到，真素細心照料大家的巴豆，我覺得彼此應該要一起幫忙弄，分工合作，重點就是我覺得應該要在積極主動，幫忙減輕彼此的負擔，大家都是從各地到小路齊聚的，大家的體力也是有限，我看到的就是家綾姐姐一直在照料大家的巴豆。"
    "再來是我覺得溝通要在明確，缺少東西要去買，據我所知要買的東西已經交代清楚了，等了半小時快一小時還沒去買，雖然中途突然說要買油，但那是意外沒想到居然沒油了，目前就想到醬。"
    "第一個就是主動幫忙，分工要明確確實一點"
    "第二個就是溝通，更好的溝通"
    "A:買東西"
    "B:買什麼"
    "A:飲料、柴魚片、#$^^#&+!-"
    "B:好，飲料喝什麼"
    "A:沒有了，就這樣飲料看你們自己喝什麼，或是要買什麼，飲料紅茶綠茶都可以，【問一下沒人回就『直接去』了】，不用等。可能有些是我沒有考慮到的部分，就先說聲抱歉嚕",
    "三人主辦成員很適合轉行當企劃，太有才了👍",
    "育德又帥又會企劃，家綾姊很罩、最會照顧大家，瑋瑋<span style='color: transparent; text-shadow: 0 0 5px rgba(0,0,0,0.01); user-select: text;' title='提示：反白此處解密機密情資'>詭計多端（？）/ 顏值擔當（？）反差萌（？）</span>",
    "很感謝這次規劃的哥哥姐姐們，大家百忙之中抽空參與討論，一起為這次的旅遊盡一份心力，讓這次活動添加許多回憶。讓我看見大家都各奔東西，還會互相關心大家的生活狀況，一起談心說笑，這是很少家族有的團結和向心力，是這次我很喜歡的一個環節。建議的部分就是，營地可以選高海拔的地點，比較舒適。",
    "主辦辛苦了",
    "初露大成功～氣氛、天氣及地點，無論哪一項都很棒，感謝大家都很有默契的配合。",
    "可以再多天一點",
    "三位主辦都很棒，完美！"
]

# --- 整理後的 B 資料集 ---
feedback_B = [
    "希望每年都能來一次這樣的活動",
    "辛苦主辦的大家！👍👍👍",
    "不管怎麼安排一定都是大拇指的💙",
    "可以去澎湖浮潛嗎～",
    "我覺得活動的部分可以大家一起討論，不用說三四個人在準備活動",
    "家族旅遊了話，我覺得南部比較適合，考慮到阿嬤的行動；如果阿嬤沒有辦法去了話，個人認為離島澎湖是蠻好的",
    "建議政府放假天數長一點啦，天數有限不夠家族旅遊，太短了，休息不夠啦，很累內🤣",
    "如果要三天兩夜我只能月底🥹🥹🥹。社畜的悲哀",
    "每年舉辦一次簡單的露營，營地可以不同地方，比較有新鮮感，也可以欣賞不同景點，CP值高。資金許可，可往包棟、外島的方向列入名單。依季節可以增加活動項目，像是夏季可以遊樂園的水上設施、海上活動，冬季泡湯等項目。",
    "私心想要三天兩夜，但是兩天一夜比較好排假",
    "很期待再次家旅，但也明白時間上的配合是最大難題，不過初露的成功也意謂這道高牆是可以被跨越的。希望大家熱絡的氛圍不止體現在家旅上，平時在群組說說幹話、分享事物都是點燃家族溫度的火種。",
    "海外旅遊 如沖繩 ",
    "建議一直辦到老！"
]

# 渲染兩大回饋區塊
render_suggestion_box("⛺ A. 初露留言建議及鼓勵", feedback_A, border_color="#3A7BD5")
render_suggestion_box("🏡 B. 家旅建議與期望", feedback_B, border_color="#00D2FF")

st.markdown("<p style='text-align: center; color: #99A9BF; font-size: 14px; margin-top: 30px;'>SIO 謹製</p>", unsafe_allow_html=True)