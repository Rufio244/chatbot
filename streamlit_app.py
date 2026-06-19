#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# VIDER AGI Chatbot + OpenAI Integration
# Fix: UnicodeEncodeError | UTF-8 Support | Thai Language | Secrets Compatible

# ✅ บังคับเข้ารหัส UTF-8 ป้องกัน Error
import sys
import os
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
os.environ["PYTHONUTF8"] = "1"
os.environ["LANG"] = "C.UTF-8"
os.environ["LC_ALL"] = "C.UTF-8"

import streamlit as st
from openai import OpenAI

# --------------------------
# 🧩 VIDER CONFIGURATION
# --------------------------
st.set_page_config(
    page_title="🤖 VIDER AGI Chatbot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="auto"
)

# ✅ แสดงหัวข้อ VIDER
st.title("🧠 VIDER AGI Chatbot")
st.write(
    """
    **ระบบอัจฉริยะ VIDER เชื่อมต่อกับ OpenAI GPT** 🚀  
    สามารถสนทนา ตอบคำถาม วิเคราะห์ข้อมูล และทำงานร่วมกับทุกโมดูล VIDER ได้ครบวงจร  
    *รองรับภาษาไทยเต็มรูปแบบ* | *แก้ไขปัญหาการเข้ารหัสตัวอักษรแล้ว*
    """
)

# ✅ ดึง API Key: รองรับทั้งพิมพ์เอง และดึงจาก Secrets.toml
openai_api_key = ""
if "OPENAI_API_KEY" in st.secrets:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    st.success("✅ โหลดคีย์จากระบบความปลอดภัยสำเร็จ", icon="🔒")
else:
    openai_api_key = st.text_input(
        "🔑 กรอก OpenAI API Key",
        type="password",
        help="สร้างคีย์ได้ที่: https://platform.openai.com/account/api-keys"
    )

if not openai_api_key or not openai_api_key.startswith("sk-"):
    st.info("ℹ️ กรุณาใส่ API Key ที่ถูกต้องเพื่อเริ่มใช้งาน", icon="🗝️")
    st.stop()

# ✅ สร้าง Client พร้อมตั้งค่าป้องกัน Encoding Error
try:
    client = OpenAI(
        api_key=openai_api_key.strip(),
        default_headers={
            "Accept-Charset": "utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        timeout=45
    )
except Exception as e:
    st.error(f"❌ ไม่สามารถเชื่อมต่อ OpenAI: {str(e)}")
    st.stop()

# ✅ เริ่มต้นประวัติการสนทนา พร้อม VIDER System Prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
            คุณคือ **VIDER AGI** ระบบอัจฉริยะหลักของ VIDER Platform  
            หน้าที่: ตอบคำถามชัดเจน ถูกต้อง เป็นธรรมชาติ ใช้ภาษาไทยที่สละสลวย  
            รองรับงาน: เขียนโค้ด, วิเคราะห์ข้อมูล, วางแผน, ให้คำปรึกษา, เชื่อมต่อกับระบบ WebHelp/AutoPilot/Deploy  
            ถ้าถามเรื่อง VIDER อธิบายตามหลักการที่สร้างไว้ให้เข้าใจง่ายที่สุด
            """
        }
    ]

# ✅ แสดงประวัติการสนทนา
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ✅ รับคำถามจากผู้ใช้
if prompt := st.chat_input("💬 พิมพ์คำถามหรือสั่งงาน VIDER ได้เลยครับ..."):
    # เพิ่มข้อความผู้ใช้
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ✅ เรียกใช้งาน OpenAI แบบปลอดภัย รองรับสตรีมมิ่ง
    try:
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",  # หรือเปลี่ยนเป็น gpt-4o ได้เลย
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
                temperature=0.7,
                max_tokens=1500
            )
            response = st.write_stream(stream)
        # บันทึกคำตอบลงประวัติ
        st.session_state.messages.append({"role": "assistant", "content": response})

    except UnicodeEncodeError:
        st.error("❌ พบปัญหาการเข้ารหัส: แก้ไขแล้วในระบบ VIDER")
    except Exception as e:
        st.error(f"⚠️ เกิดข้อผิดพลาด: {str(e)}")
