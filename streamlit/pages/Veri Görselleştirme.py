import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
import requests

# Streamlit sayfa ayarları
st.set_page_config(
    page_title="TraderMentorAI",
    page_icon="C:\\Users\\rusen\\source\\repos\\Proje\\Proje\\TradeMentor-AI\\streamlit\\images\\Leonardo_Phoenix_Create_a_modern_sleek_logo_for_the_stock_trad_2.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
db = client["proje"]  # Kendi veritabanı adınızı yazın

# Kripto para birimlerinin listesi
cryptos = ["BTC", "ADA", "BNB", "DOGE", "DOGS", "ETH", "MATIC", "NOT", "SHIB", "SOL", "TON", "XRP"]

# Kripto para seçimi
selected_crypto = st.selectbox("Bir kripto para birimi seçin", cryptos)

# Veriyi MongoDB'den çek
collection = db[selected_crypto]
data = list(collection.find({}))
df = pd.DataFrame(data)

# Veriyi formatla
df["time"] = pd.to_datetime(df["time"])
df = df.sort_values(by="time")

# Tarih aralığı seçme
start_date = st.date_input("Başlangıç Tarihi", df["time"].min().date())
end_date = st.date_input("Bitiş Tarihi", df["time"].max().date())

# Seçilen tarih aralığına göre filtreleme
filtered_df = df[(df["time"] >= pd.to_datetime(start_date)) & (df["time"] <= pd.to_datetime(end_date))]

# Zaman serisi grafiği
st.title(f"{selected_crypto} Verileri Görselleştirme")
fig = px.line(filtered_df, x="time", y="close", title=f"{selected_crypto} Fiyat Zaman Serisi (Kapanış Fiyatı)")
st.plotly_chart(fig)

# Filtrelenmiş veriyi göster
st.write(filtered_df)

# News API'den haberleri çekme fonksiyonu
def get_news():
    api_key = "dc482f4ae1fc4005bd3b6887d20e8c90"
    url = f"https://newsapi.org/v2/everything?q={selected_crypto}&language=tr&apiKey={api_key}"
    response = requests.get(url)
    return response.json()

# Anahtar kelimelerle haber filtreleme
def filter_news_by_keywords(articles, keywords):
    filtered_articles = []
    for article in articles:
        # Başlık ve açıklamada anahtar kelimeleri kontrol et
        if any(keyword.lower() in article['title'].lower() or keyword.lower() in article['description'].lower() for keyword in keywords):
            filtered_articles.append(article)
    return filtered_articles

# Kripto para ile ilgili haberleri çek
st.title(f"{selected_crypto} Haberleri")
if selected_crypto:
    news_data = get_news()
    
    if news_data and "articles" in news_data:
        articles = news_data["articles"]
        
        # Anahtar kelimelerle filtreleme (örn. "Bitcoin" ve "Kripto" gibi)
        keywords = ["bitcoin", "kripto", "blockchain"]
        filtered_articles = filter_news_by_keywords(articles, keywords)
        
        # Tüm haberleri listele
        if len(filtered_articles) > 0:
            for article in filtered_articles:
                st.subheader(article["title"])
                st.write(f"Yayın Tarihi: {article['publishedAt']}")
                st.write(article["description"])
                st.write(f"Detaylar: [{article['title']}]({article['url']})")
                st.markdown("---")
        else:
            st.write("Bu kripto para hakkında daha fazla haber bulunamadı.")
    else:
        st.error("Haberler alınırken bir hata oluştu.")

# İletişim baloncuğunu tanımla
def contact_bubble():
    st.markdown(
        """
        <style>
        .contact-bubble {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #007BFF;
            color: white;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            cursor: pointer;
            font-size: 20px;
            text-decoration: none;
        }
        </style>
        <a class="contact-bubble" href="https://servispy-2etfjh5ephbuz2qeltdvsk.streamlit.app/" target="_blank">
            📞
        </a>
        """,
        unsafe_allow_html=True,
    )

# İletişim baloncuğunu göster
contact_bubble()
