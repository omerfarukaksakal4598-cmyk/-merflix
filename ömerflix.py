import streamlit as st
from google import genai
import os
import json
import re
import random

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="ÖmerFlix Premium", layout="wide", page_icon="🍿")

# --- ULTRA PREMİUM SİNEMA TASARIMI (CSS) ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
        background: linear-gradient(180deg, #111111 0%, #000000 100%) !important; 
    }
    h1, h2, h3, p, label, span { color: #F5F5F1 !important; font-family: 'Helvetica Neue', Arial, sans-serif; }
    
    .netflix-logo { 
        color: #E50914 !important; 
        font-size: 55px; 
        font-weight: 900; 
        letter-spacing: 3px; 
        text-shadow: 2px 2px 10px rgba(229, 9, 20, 0.5);
        margin-bottom: 30px;
    }
    
    .film-card { 
        background-color: #141414; 
        padding: 10px; 
        border-radius: 12px; 
        border: 1px solid #333; 
        transition: all 0.3s ease-in-out; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.8);
        height: 100%;
    }
    .film-card:hover { 
        transform: scale(1.06) translateY(-5px); 
        border-color: #E50914; 
        box-shadow: 0px 10px 25px rgba(229, 9, 20, 0.6);
        z-index: 10;
    }
    
    .stButton>button {
        background-color: #E50914 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #f40612 !important;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# API Anahtarı Kontrolü
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("HATA: Streamlit Secrets içinde 'GOOGLE_API_KEY' bulunamadı.")
    st.stop()

# EN YENİ NESİL GENAI CLIENT BAĞLANTISI
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

if not os.path.exists("filmler"): os.makedirs("filmler")
ONBELLEK_DOSYASI = "film_onbellek.json"

def onbellek_yukle():
    if os.path.exists(ONBELLEK_DOSYASI):
        try:
            with open(ONBELLEK_DOSYASI, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}
    return {}

def onbellek_kaydet(veri):
    with open(ONBELLEK_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)

# --- YENİLENEN İÇERİK VE KAPAK BULUCU ---
def internetten_film_bul(dosya_adi):
    temiz_isim = os.path.splitext(dosya_adi)[0]
    
    prompt = f"""
    Sen bir sinema uzmanısın. Kullanıcı şu dosyayı indirdi: '{temiz_isim}'
    Bu filmin (veya bu isme en yakın popüler filmin) bilgilerini getir.
    
    LÜTFEN SADECE AŞAĞIDAKİ JSON FORMATINDA YANIT VER:
    {{
        "adi": "Filmin Türkçe Adı",
        "kategori": "Türü",
        "aciklama": "Film hakkında sürükleyici, Türkçe kısa bir özet.",
        "imdb": "⭐ 8.5"
    }}
    """
    try:
        # Yeni SDK formatında içerik üretimi (gemini-2.5-flash modeli ile)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        json_match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if json_match:
            film_data = json.loads(json_match.group(0))
            url_isim = film_data["adi"].replace(" ", "%20")
            film_data["kapak"] = f"https://image.pollinations.ai/prompt/cinematic%20movie%20poster%20for%20{url_isim}?width=500&height=750&nologo=true"
            return film_data
    except Exception as e:
        pass
    
    url_isim = temiz_isim.replace(" ", "%20")
    return {
        "adi": temiz_isim,
        "kategori": "Bilinmiyor",
        "aciklama": "Yapay zeka heyecan verici bir özet hazırlıyor...",
        "imdb": "⭐ -.-",
        "kapak": f"https://image.pollinations.ai/prompt/movie%20poster%20{url_isim}?width=500&height=750&nologo=true"
    }

# --- FİLM TARAMA MOTORU ---
film_havuzu = onbellek_yukle()
klasordeki_dosyalar = [f for f in os.listdir("filmler") if f.lower().endswith(('.mp4', '.mkv', '.avi', '.mov'))]

yenileme_yapildi = False
for dosya in klasordeki_dosyalar:
    if dosya not in film_havuzu:
        with st.spinner(f"🤖 Yapay Zeka '{dosya}' için kapak ve açıklama üretiyor..."):
            film_havuzu[dosya] = internetten_film_bul(dosya)
            yenileme_yapildi = True

if yenileme_yapildi:
    onbellek_kaydet(film_havuzu)

aktif_filmler = {dosya: veri for dosya, veri in film_havuzu.items() if dosya in klasordeki_dosyalar}

# --- SOL MENÜ ---
with st.sidebar:
    st.markdown("<h1 style='color: #E50914;'>ÖmerFlix</h1>", unsafe_allow_html=True)
    st.write(f"📂 Kütüphanende **{len(aktif_filmler)}** film var.")
    st.write("---")
    kategoriler = ["Tümü"] + list(set([veri["kategori"] for veri in aktif_filmler.values()]))
    secilen_kategori = st.selectbox("🎯 Kategori Filtresi", kategoriler)

# --- ANA EKRAN ---
st.markdown("<div class='netflix-logo'>ÖMERFLIX</div>", unsafe_allow_html=True)

if "active_video" in st.session_state:
    st.markdown(f"### 🎬 <span style='color:#E50914;'>{st.session_state.active_title}</span> Oynatılıyor", unsafe_allow_html=True)
    st.video(st.session_state.active_video)
    if st.button("❌ Sinema Modundan Çık", use_container_width=True):
        del st.session_state.active_video
        st.rerun()
    st.write("---")

elif aktif_filmler and secilen_kategori == "Tümü":
    vitrin_dosya = random.choice(list(aktif_filmler.keys()))
    vitrin_veri = aktif_filmler[vitrin_dosya]
    
    col1, col2 = st.columns([1, 2.5])
    with col1:
        st.image(vitrin_veri["kapak"], use_container_width=True)
    with col2:
        st.markdown(f"<h1 style='font-size: 50px; margin-bottom: 0px;'>{vitrin_veri['adi']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #46d369;'>{vitrin_veri['imdb']} | {vitrin_veri['kategori']}</h3>", unsafe_allow_html=True)
        st.write(vitrin_veri["aciklama"])
        st.write("")
        if st.button("▶️ HEMEN İZLE", key="vitrin_izle"):
            st.session_state.active_video = f"filmler/{vitrin_dosya}"
            st.session_state.active_title = vitrin_veri["adi"]
            st.rerun()
    st.write("---")

st.markdown("### 🍿 İzlemeye Devam Et")

if not aktif_filmler:
    st.info("Kütüphanen henüz boş. İnternette yayında olduğu için GitHub depondaki projene bir 'filmler' klasörü açıp içine 1-2 MB'lık deneme videoları atabilirsin!")
else:
    cols = st.columns(3)
    gosterilen_sayi = 0
    
    for dosya, veri in aktif_filmler.items():
        if secilen_kategori == "Tümü" or veri["kategori"] == secilen_kategori:
            sutun_no = gosterilen_sayi % 3
            with cols[sutun_no]:
                st.markdown("<div class='film-card'>", unsafe_allow_html=True)
                st.image(veri["kapak"], use_container_width=True)
                st.markdown(f"<h4 style='margin-top: 10px; margin-bottom: 5px;'>{veri['adi']}</h4>", unsafe_allow_html=True)
                st.markdown(f"<span style='color: #46d369; font-weight: bold;'>{veri['imdb']}</span> | <span style='font-size: 13px; color: #aaa;'>{veri['kategori']}</span>", unsafe_allow_html=True)
                
                # Açıklama metnini hatasız çeken ve kısaltan temiz blok:
                aciklama_metni = veri.get("aciklama", "")
                kisa_ozet = aciklama_metni[:80] + "..." if len(aciklama_metni) > 80 else aciklama_metni
                st.markdown(f"<p style='font-size: 14px; color: #ddd;'>{kisa_ozet}</p>", unsafe_allow_html=True)
                
                if st.button("▶️ Oynat", key=f"oynat_{dosya}", use_container_width=True):
                    st.session_state.active_video = f"filmler/{dosya}"
                    st.session_state.active_title = veri["adi"]
                    st.rerun()
                st.markdown("</div><br>", unsafe_allow_html=True)
            gosterilen_sayi += 1
