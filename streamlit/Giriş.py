import streamlit as st
from PIL import Image

TITLE = "Trader Mentor AI'a hoşgeldiniz"

# Page configuration with updated icon
st.set_page_config(
    page_title="TraderMentorAI",
    page_icon="C:\\Users\\rusen\\source\\repos\\Proje\\Proje\\TradeMentor-AI\\streamlit\\images\\Leonardo_Phoenix_Create_a_modern_sleek_logo_for_the_stock_trad_3.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Center-align the title
st.markdown(
    f"""
    <h1 style="text-align: center;">{TITLE}</h1>
    """,
    unsafe_allow_html=True
)

# Load and resize the main page image
image_path = "C:\\Users\\rusen\\source\\repos\\Proje\\Proje\\TradeMentor-AI\\streamlit\\images\\Leonardo_Phoenix_Create_a_modern_sleek_logo_for_the_stock_trad_3.jpg"

image = Image.open(image_path)
image = image.resize((600, 600))

# Display the image below the title, centered in the middle column
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.image(image)

# Hakkımızda bölümü (Sayfanın en alt kısmında)
st.markdown("---")  # Ayrıcı çizgi
st.subheader("Hakkımızda")

# Bilgileri liste olarak ekleyin
st.write("""
**Telefon Numarası**: +90 555 123 4567  
**E-posta**: info@tradermentorai.com  
**Adres**: Büyükdere Caddesi No:123, Maslak, İstanbul  
**Merkez Adresi**: Trader Mentor AI Merkezi, İstanbul, Türkiye  
""")

# Bu bölümü ekranın en altına yerleştirmek için ayraç ekleyebiliriz.
st.markdown("<br><br>", unsafe_allow_html=True)
