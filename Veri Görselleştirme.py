import streamlit as st
import yfinance as yf
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO
import pandas as pd

# Başlık ve ayarlar
TİTLE = "VERİ GÖRSELLEŞTİRME"
st.set_page_config(
    page_title="TraderMentorAI",
    page_icon="C:\\Users\\omera\\Desktop\\STREAMLIT\\streamlit_TradeMentorAi\\images\\Leonardo_Phoenix_Create_a_modern_sleek_logo_for_the_stock_trad_2.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an extremely cool app!"
    }
)

# Kripto para sembolleri ve logo URL'leri
crypto_info = {
    "Bitcoin": {"symbol": "BTC-USD", "logo": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png"},
    "Ethereum": {"symbol": "ETH-USD", "logo": "https://assets.coingecko.com/coins/images/279/large/ethereum.png"},
    "Binance Coin": {"symbol": "BNB-USD", "logo": "https://assets.coingecko.com/coins/images/825/large/binance-coin-logo.png"},
    "Ripple": {"symbol": "XRP-USD", "logo": "https://assets.coingecko.com/coins/images/44/large/xrp-symbol-white-128.png"},
    "Cardano": {"symbol": "ADA-USD", "logo": "https://assets.coingecko.com/coins/images/975/large/cardano.png"},
    "Dogecoin": {"symbol": "DOGE-USD", "logo": "https://assets.coingecko.com/coins/images/5/large/dogecoin.png"},
    "Polygon": {"symbol": "MATIC-USD", "logo": "https://assets.coingecko.com/coins/images/4713/large/matic-token-icon.png"},
    "Solana": {"symbol": "SOL-USD", "logo": "https://assets.coingecko.com/coins/images/4128/large/solana.png"},
    "Toncoin": {"symbol": "TON-USD", "logo": "https://assets.coingecko.com/coins/images/17980/large/ton_symbol.png"},
    "Shiba Inu": {"symbol": "SHIB-USD", "logo": "https://assets.coingecko.com/coins/images/11939/large/shiba.png"}
}

# Fonksiyonlar
def show_bitcoin_chart(chart_type):
    if chart_type == "Line":
        st.image("C:\\Users\\omera\\Desktop\\TradeMentorAi\\streamlit_TradeMentorAi\\images\\BTCUSD_Lİne.png", caption="Bitcoin Line Grafik", use_column_width=True)
    elif chart_type == "Bar":
        st.image("C:\\Users\\omera\\Desktop\\TradeMentorAi\\streamlit_TradeMentorAi\\images\\BTCUSD_Bar.png", caption="Bitcoin Bar Grafik", use_column_width=True)
    elif chart_type == "Scatter":
        st.image("C:\\Users\\omera\\Desktop\\TradeMentorAi\\streamlit_TradeMentorAi\\images\\BTCUSD_Scatter.jpg", caption="Bitcoin Scatter Grafik", use_column_width=True)

def show_ethereum_chart(chart_type):
    if chart_type == "Line":
        st.image("C:\\Users\\omera\\Desktop\\TradeMentorAi\\streamlit_TradeMentorAi\\images\\ETHUSD_Line.png", caption="Ethereum Line Grafik", use_column_width=True)
    elif chart_type == "Bar":
        st.image("C:\\Users\\omera\\Desktop\\TradeMentorAi\\streamlit_TradeMentorAi\\images\\ETHUSD_Bar.png", caption="Ethereum Bar Grafik", use_column_width=True)
    elif chart_type == "Scatter":
        st.image("C:\\Users\\omera\\Desktop\\TradeMentorAi\\streamlit_TradeMentorAi\\images\\ETHUSD_Scatter.jpg", caption="Ethereum Scatter Grafik", use_column_width=True)

# Diğer kripto paralar için de benzer şekilde fonksiyonlar tanımlanabilir...

# Yan menüde filtreleme seçenekleri
st.sidebar.header("Filtreleme Seçenekleri")

# Kripto para seçimi
coin_name = st.sidebar.selectbox("Bir Kripto Para Seçin", list(crypto_info.keys()))
symbol = crypto_info[coin_name]["symbol"]
logo_url = crypto_info[coin_name]["logo"]

# Tarih aralığı seçimi
start_date = st.sidebar.date_input("Başlangıç Tarihi", datetime(2021, 1, 1))
end_date = st.sidebar.date_input("Bitiş Tarihi", datetime.now())

# Grafik türü seçimi
chart_type = st.sidebar.selectbox("Grafik Türü Seçin", ["Line", "Bar", "Scatter"])

# Logo gösterimi
try:
    response = requests.get(logo_url)
    logo = Image.open(BytesIO(response.content))
    st.sidebar.image(logo, width=80)
except Exception as e:
    st.sidebar.warning(f"{coin_name} için logo yüklenemedi. Hata: {e}")

# Seçilen kripto paraya göre uygun grafik gösterimi
if coin_name == "Bitcoin":
    show_bitcoin_chart(chart_type)
elif coin_name == "Ethereum":
    show_ethereum_chart(chart_type)
# Diğer coinler için de benzer yapıda koşullar ekleyebilirsiniz.

# Veri setini sidebar'da dosya adı olarak gösterme
st.sidebar.subheader("Veri Setleri")
with open("C:\\Users\\omera\\Desktop\\TradeMentorAi\\streamlit_TradeMentorAi\\demo.csv", "rb") as file:
    st.sidebar.download_button(label="demo.csv", data=file, file_name="demo.csv", mime="text/csv")

# "Veri Setleri" başlığı altında veri tablosunu gösterme
st.subheader("Veri Setleri")
data = pd.read_csv("C:\\Users\\omera\\Desktop\\TradeMentorAi\\streamlit_TradeMentorAi\\demo.csv")
st.write(data)
# İletişim baloncuğu
def contact_bubble():
    st.markdown(
        """
        <style>
        .contact-bubble {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #007BFF; /* Mavi arka plan */
            color: white; /* Yazı rengi */
            border-radius: 50%; /* Yuvarlak şekil */
            width: 50px; /* Genişlik */
            height: 50px; /* Yükseklik */
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
        unsafe_allow_html=True
    )

# İletişim baloncuğunu göster
contact_bubble()
