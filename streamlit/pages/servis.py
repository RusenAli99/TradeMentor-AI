import streamlit as st
st.set_page_config(
    page_title="TraderMentorAI",
    page_icon="C:\\Users\\rusen\\source\\repos\\Proje\\Proje\\TradeMentor-AI\\streamlit\\images\\Leonardo_Phoenix_Create_a_modern_sleek_logo_for_the_stock_trad_2.jpg", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Sayfanın arka planını siyah yapmak için CSS ekleyelim
st.markdown(
    """
    <style>
    body {
        background-color: #121212;  /* Siyah arka plan */
        color: white;  /* Beyaz yazı rengi */
    }
    h1, h2, h3 {
        color: #4CAF50;  /* Başlıklar için yeşil renk */
    }
    .streamlit-expanderHeader {
        color: #4CAF50;  /* Açılır menü başlıkları için yeşil renk */
    }
    </style>
    """, unsafe_allow_html=True
)

# Sayfa başlığı
st.title("İletişim Bilgilerim")

# Alt başlık
st.subheader("Bana Ulaşın")

# İletişim bilgileri
st.write("""
    **Telefon**: +90 123 456 7890  
    **E-posta**: example@email.com  
    **LinkedIn**: [linkedin.com/in/yourprofile](https://www.linkedin.com/in/yourprofile)  
    **Twitter**: [@yourhandle](https://twitter.com/yourhandle)  
""")

# İletişim Formu (Opsiyonel)
st.write("Alternatif olarak aşağıdaki formu doldurabilirsiniz:")

# Kullanıcıdan alınacak bilgiler
name = st.text_input("Adınız")
email = st.text_input("E-posta adresiniz")
message = st.text_area("Mesajınız")

# Gönderme butonu
if st.button("Gönder"):
    if name and email and message:
        st.success("Mesajınız başarıyla gönderildi! Teşekkür ederim.")
    else:
        st.error("Lütfen tüm alanları doldurun.")
