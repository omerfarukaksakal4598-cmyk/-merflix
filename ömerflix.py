import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="ÖmerFlix Premium", layout="wide")

# Tasarım
st.markdown("""
    <style>
    .film-card { background: #141414; padding: 15px; border-radius: 12px; border: 1px solid #333; margin-bottom: 20px; text-align: center; }
    .stButton>button { background-color: #E50914 !important; color: white !important; font-weight: bold !important; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# FİLMLERİN VERİTABANI
filmler = [
    {"ad": "Grizzy & les Lemmings", "id": "1x39h1ne0e3esRye5dG6fZcAF6Vt_Nab6"},
    {"ad": "Big Hero 6", "id": "1CmKZ8lXRshnBtxeAJlxlbtxLxO5xFWTR"},
    {"ad": "Hababam Sınıfı", "id": "1fa3oRFRfAh9NJsnZb4XD-vVFyQ6gzcz4"},
    {"ad": "Hababam Sınıfı Sınıfta Kaldı", "id": "11XY4vjYqOxXMSSPGF5bb6qfvXoStLIPj"},
    {"ad": "Şaban Oğlu Şaban", "id": "1mEATprqTLwaKyH8wl_7gHQOPx2oFoOVY"},
    {"ad": "Zehir (Venom)", "id": "1kQGXuE21Yy3zSVbjDxm7aWAqDCZmCQJl"}
]

st.markdown("<h1 style='color: #E50914; text-align: center;'>ÖMERFLIX</h1>", unsafe_allow_html=True)
st.write("---")

# İzleme Modu (Eğer bir film seçildiyse)
if "secili_video" in st.session_state:
    st.markdown(f"### 🎬 {st.session_state.secili_ad}")
    # Drive Preview Linki
    embed_url = f"https://drive.google.com/file/d/{st.session_state.secili_id}/preview"
    st.components.v1.iframe(embed_url, height=500, scrolling=True)
    if st.button("⬅️ Kütüphaneye Dön"):
        del st.session_state.secili_video
        st.rerun()
else:
    # Film Listesi
    cols = st.columns(3)
    for i, film in enumerate(filmler):
        with cols[i % 3]:
            st.markdown("<div class='film-card'>", unsafe_allow_html=True)
            # Otomatik kapak görseli
            st.image(f"https://image.pollinations.ai/prompt/movie%20poster%20{film['ad'].replace(' ', '%20')}?width=300&height=400")
            st.subheader(film['ad'])
            if st.button(f"▶️ İZLE", key=film['ad']):
                st.session_state.secili_video = True
                st.session_state.secili_id = film['id']
                st.session_state.secili_ad = film['ad']
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
