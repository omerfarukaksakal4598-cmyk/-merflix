import streamlit as st

st.set_page_config(page_title="ÖmerFlix Premium", layout="wide")

st.markdown("""
    <style>
    .film-card { background: #141414; padding: 15px; border-radius: 12px; border: 1px solid #333; margin-bottom: 20px; text-align: center; }
    .stButton>button { background-color: #E50914 !important; color: white !important; font-weight: bold !important; width: 100%; }
    h3 { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# Film Listesi (API'sız versiyon)
filmler = [
    {"ad": "Grizzy & les Lemmings", "id": "1x39h1ne0e3esRye5dG6fZcAF6Vt_Nab6", "kapak": "https://i.ibb.co/ZRy2k3XY/image-8c4cff.jpg"},
    {"ad": "Big Hero 6", "id": "1CmKZ8lXRshnBtxeAJlxlbtxLxO5xFWTR", "kapak": "https://i.ibb.co/5hSnzskv/image-8c4cd7.jpg"},
    {"ad": "Hababam Sınıfı", "id": "1fa3oRFRfAh9NJsnZb4XD-vVFyQ6gzcz4", "kapak": "https://i.ibb.co/C52zMnzp/image-8c4c81.jpg"},
    {"ad": "Hababam Sınıfı Sınıfta Kaldı", "id": "11XY4vjYqOxXMSSPGF5bb6qfvXoStLIPj", "kapak": "https://i.ibb.co/XZPhWL5L/image-8c4939.jpg"},
    {"ad": "Şaban Oğlu Şaban", "id": "1mEATprqTLwaKyH8wl_7gHQOPx2oFoOVY", "kapak": "https://i.ibb.co/99zZ14H9/image-8c4c26.jpg"}
]

st.markdown("<h1 style='color: #E50914; text-align: center;'>ÖMERFLIX</h1>", unsafe_allow_html=True)
st.write("---")

if "secili_video" in st.session_state:
    st.markdown(f"### 🎬 {st.session_state.secili_ad}")
    embed_url = f"https://drive.google.com/file/d/{st.session_state.secili_id}/preview"
    st.components.v1.iframe(embed_url, height=500, scrolling=True)
    if st.button("⬅️ Kütüphaneye Dön"):
        del st.session_state.secili_video
        st.rerun()
else:
    cols = st.columns(3)
    for i, film in enumerate(filmler):
        with cols[i % 3]:
            st.markdown("<div class='film-card'>", unsafe_allow_html=True)
            st.image(film['kapak'], use_container_width=True)
            st.subheader(film['ad'])
            if st.button(f"▶️ İZLE", key=film['ad']):
                st.session_state.secili_video = True
                st.session_state.secili_id = film['id']
                st.session_state.secili_ad = film['ad']
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
