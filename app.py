import streamlit as st
import google.generativeai as genai

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Akıllı Buzdolabı & Yemek Asistanı", 
    page_icon="🍳", 
    layout="centered"
)

# Özel CSS ile Mutfak Arka Planı, Şık Butonlar ve Kart Tasarımı
st.markdown("""
    <style>
    /* Ana arkaplana profesyonel mutfak görseli ve yazılar okunsun diye karartma efekti (overlay) ekliyoruz */
    .stApp {
        background-image: linear-gradient(rgba(14, 17, 23, 0.88), rgba(14, 17, 23, 0.88)), 
                          url('https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&q=80&w=1920');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Buton Tasarımı */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff4b4b, #ff914d);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        border: none;
        box-shadow: 0 4px 10px rgba(255, 75, 75, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff2a2a, #ff7722);
        color: white;
        box-shadow: 0 6px 15px rgba(255, 75, 75, 0.5);
    }

    /* Sonuç Kutusu (Card) Tasarımı */
    .recipe-card {
        background-color: rgba(30, 37, 48, 0.92);
        padding: 25px;
        border-radius: 12px;
        border-left: 6px solid #ff4b4b;
        box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        color: #f0f0f0;
        backdrop-filter: blur(5px);
    }
    
    /* Yazı renklerini arka planda net okunacak şekilde ayarlayalım */
    h1, h2, h3, p, label {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Başlık ve Açıklama Alanı
st.markdown("<h1 style='text-align: center; color: #ff4b4b !important;'>🍳 Akıllı Buzdolabı & Şef Asistanı</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d0d0d0 !important;'>Dolabında kalan malzemeleri yaz, yapay zeka şefimiz sana restoran kalitesinde tarif versin!</p>", unsafe_allow_html=True)
st.markdown("---")

# API Anahtarı (Sabit)
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Kullanıcı Girdi Alanları
col1, col2 = st.columns([3, 1])
with col1:
    malzemeler = st.text_input("🥕 Dolabındaki malzemeler:", placeholder="Örn: domates, yumurta, kaşar, sucuk")
with col2:
    ogun = st.selectbox("🍽️ Öğün Seç:", ["Farketmez", "Kahvaltı", "Öğle", "Akşam", "Atıştırmalık"])

st.markdown("<small style='color: #b0b0b0;'>💡 İpucu: Malzemeleri araya virgül koyarak yazarsan şef çok daha iyi tarifler çıkarır.</small>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Buton ve Sonuç Alanı
if st.button("✨ Şaheser Bir Tarif Üret!"):
    if not malzemeler:
        st.warning("⚠️ Lütfen dolaptaki malzemeleri boş bırakma kanka!")
    else:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-3.5-flash')
            
            prompt = f"Sen usta ve neşeli bir şefsin. Kullanıcının evinde şu malzemeler var: {malzemeler}. Tercih edilen öğün: {ogun}. Bu malzemeleri ve temel ev malzemelerini (tuz, sıvı yağ, baharat vb.) kullanarak yapabileceği en lezzetli yemeğin tarifini ver. Yanıtın şu başlıklardan oluşsun: Yemek Adı, Malzemeler, Adım Adım Hazırlanışı ve Şefin Püf Noktası."
            
            with st.spinner("👨‍🍳 Şef mutfakta harikalar yaratıyor, beklemede kal..."):
                response = model.generate_content(prompt)
                
                # Şık cam efekti verilmiş kart içinde sonucu gösterelim
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 🔥 Şefin Sana Özel Menüsü")
                st.markdown(f"""
                <div class="recipe-card">
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")