import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import time

# Streamlit sayfa ayarları
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

# Coin bilgilerini alma fonksiyonu
@st.cache_data(ttl=600)  # 10 dakika önbellekleme
def get_coin_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    coin_ids = [
        "bitcoin", "ethereum", "cardano", "binancecoin", "solana", "polygon",
        "dogecoin", "shiba-inu", "ripple", "toncoin", "matic-network", "binance-usd",
        "tron", "polkadot", "avalanche-2", "litecoin", "stellar", "chainlink"
    ]
    params = {
        "vs_currency": "usd",
        "ids": ",".join(coin_ids)  # Belirli coinlerin kimliklerini ekle
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return [
            {
                "name": coin["name"],
                "price": coin["current_price"],
                "change_24h": coin["price_change_percentage_24h"],
                "volume_24h": coin["total_volume"],
                "logo": coin["image"]
            }
            for coin in data
        ]
    except requests.exceptions.RequestException as e:
        st.error(f"Veri alınırken hata oluştu: {e}")
        return None

# Güncel coin bilgilerini çekme ve gösterme
coin_data = get_coin_data()

if coin_data:
    st.subheader("Güncel Coin Fiyatları")
    
    # Görsellerin ve bilgilerin grid formatında gösterimi
    cols = st.columns(3)  # 3 sütun halinde gösterim
    for idx, coin in enumerate(coin_data):
        with cols[idx % 3]:
            # Coin logosunu yükle
            try:
                response = requests.get(coin["logo"])
                response.raise_for_status()
                logo_image = Image.open(BytesIO(response.content))
            except requests.exceptions.RequestException:
                logo_image = None

            # Coin bilgilerini ve logosunu göster
            if logo_image:
                st.image(logo_image, width=75)
            st.markdown(f"**{coin['name']}**")
            st.write(f"Fiyat: ${coin['price']:.2f}")
            st.write(f"24 Saatlik Değişim: {coin['change_24h']:.2f}%")
            st.write(f"24 Saatlik Hacim: ${coin['volume_24h']:.2f}")
            st.markdown("---")

    time.sleep(0.5)  # Yükleme süresini kontrol etmek için ufak bir bekleme süresi
