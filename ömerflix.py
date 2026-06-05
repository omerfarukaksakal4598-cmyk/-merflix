import streamlit as st
import os
import random

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="ÖmerFlix Premium", layout="wide", page_icon="🍿")

# --- TASARIM ---
st.markdown("""
    <style>
    .netflix-logo { color: #E50914 !important; font-size: 55px; font-weight: 900; letter-spacing: 3px; }
    .film-card { background-color: #141414; padding: 15px; border-radius: 12px; border: 1px solid #333; }
    .stButton>button { background-color: #E50914 !important; color: white !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- SENİN DRIVE KLASÖRÜN ---
# Buraya paylaşıma açık klasörünün linkini koyuyoruz
DRIVE_KLASOR_LINKI = "https://drive.google.com/drive/folders/1s-y-m6SA1wLwE4uLvjhoN2gFA5yIvMMT"

st.markdown("<div class='netflix-logo'>ÖMERFLIX</div>", unsafe_allow_html=True)
st.write("---")

st.info("Filmlerin Drive klasöründe! İzlemek için aşağıdaki butona tıkla, seni direkt dosyaların olduğu klasöre yönlendireceğim.")

if st.button("🚀 TÜM FİLMLERİ DRIVE'DA İZLE", use_container_width=True):
    st.markdown(f'<meta http-equiv="refresh" content="0; url={DRIVE_KLASOR_LINKI}">', unsafe_allow_html=True)
    st.write(f"Yönlendiriliyorsun... [Tıklayarak Git]({DRIVE_KLASOR_LINKI})")

st.write("---")
st.subheader("🍿 Kütüphane Görünümü")
col1, col2, col3 = st.columns(3)

# Basit bir görselleştirme
with col1:
    st.image("https://image.pollinations.ai/prompt/movie%20poster%20collection?width=300&height=400", use_container_width=True)
with col2:
    st.image("https://image.pollinations.ai/prompt/cinema%20popcorn?width=300&height=400", use_container_width=True)
with col3:
    st.image("https://image.pollinations.ai/prompt/film%20reel?width=300&height=400", use_container_width=True)

st.success("ÖmerFlix şu an canlı ve yayında! Arkadaşlarına linkini atabilirsin.")
