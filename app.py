import streamlit as st
import google.generativeai as genai

# ตั้งค่าหน้าจอ
st.set_page_config(page_title="AI ผู้ช่วย นศท.", page_icon="🪖")

# --- นำ API KEY ที่จดไว้มาใส่ตรงนี้ ---
API_KEY = "วางรหัส_API_KEY_ของคุณแทนที่ข้อความนี้ทั้งหมด"
genai.configure(api_key=API_KEY)

# ตั้งค่าสมอง AI
instruction = """
คุณคือ AI ผู้ช่วย นศท. (นักศึกษาวิชาทหาร) ประจำโรงเรียนบัวขาว 
หน้าที่ของคุณคือให้ข้อมูลเกี่ยวกับ:
1. โครงการ รด.จิตอาสา
2. โครงการ "รด.ฮีโร่ Role Model 2026"
3. โครงการ "เติมโลหิตเพื่อชาติ 10 ล้านซีซี"
ตอบคำถามด้วยความสุภาพ กระตือรือร้น และให้กำลังใจ
"""
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

# ส่วนหัวเว็บ
st.title("🪖 AI ผู้ช่วย นศท. โรงเรียนบัวขาว")
st.write("สอบถามข้อมูลโครงการ รด.จิตอาสา, รด.ฮีโร่ และบริจาคโลหิตได้เลยครับ")

# ระบบความจำ
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงประวัติแชท
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# กล่องพิมพ์ข้อความ
if prompt := st.chat_input("พิมพ์คำถามของคุณที่นี่..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
