import streamlit as st
import requests
import pandas as pd

# Coin bilgilerini alma fonksiyonu
@st.cache_data(ttl=600)  # 10 dakika süreyle önbellekle
def get_coin_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,cardano,binancecoin,solana,polygon"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Hataları kontrol et
        data = response.json()
        return [
            {
                "name": coin["name"],
                "price": coin["current_price"],
                "change_24h": coin["price_change_percentage_24h"],
                "volume_24h": coin["total_volume"],
                "logo": coin["image"],
                "id": coin["id"]  # Coin'in id'sini ekleyin
            }
            for coin in data
        ]
    except requests.exceptions.RequestException as e:
        st.error(f"Veri alınırken hata oluştu: {e}")
        return None

# Sayfa yapılandırması
page = st.sidebar.selectbox("Sayfa Seçin", ("Ana Sayfa", "Veri Görselleştirme"))

# Ana Sayfa: Coin Kartlarını Göster
if page == "Ana Sayfa":
    coin_data = get_coin_data()

    if coin_data:
        st.markdown("<h2 style='text-align: center;'>Güncel Coin Fiyatları</h2>", unsafe_allow_html=True)

        # Kart stili
        card_style = """
        <style>
        body {
            background-color: #000; /* Arka plan rengi siyah */
            color: #fff; /* Metin rengi beyaz */
        }
        .card-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr); /* 4 sütunlu grid */
            gap: 20px; /* Kartlar arasındaki boşluk */
            margin-top: 20px; /* Üstten boşluk */
        }
        .coin-card {
            border: 2px solid #4CAF50; /* Kenar rengi */
            border-radius: 10px; 
            padding: 15px; 
            background-color: #1e1e1e; /* Koyu gri arka plan rengi */
            text-align: center; 
            transition: box-shadow 0.3s;
        }
        .coin-card:hover {
            box-shadow: 0 4px 8px rgba(76, 175, 80, 0.7); /* Hover rengi */
        }
        .coin-logo {
            width: 50px;
            height: 50px;
        }
        h3 {
            color: #4CAF50; /* Başlık rengi */
        }
        p {
            color: #fff; /* Metin rengi beyaz */
        }
        </style>
        """

        st.markdown(card_style, unsafe_allow_html=True)

        # Kartları saracak bir div oluştur
        st.markdown('<div class="card-container">', unsafe_allow_html=True)

        for coin in coin_data:
            # Coin kartına tıklanabilir link ekleme
            link = f"/Veri%20Görselleştirme?selected_coin={coin['id']}"  # Sayfa linkini düzenle

            # Her coin için kart oluşturma
            st.markdown(f"""
            <div class="coin-card">
                <a href="{link}">
                    <img class="coin-logo" src="{coin["logo"]}" alt="{coin['name']} Logo"/>
                    <h3>{coin["name"]}</h3>
                    <p><strong>Fiyat:</strong> ${coin['price']:.2f}</p>
                    <p><strong>24H Değişim:</strong> {coin['change_24h']:.2f}%</p>
                    <p><strong>24H Hacim:</strong> ${coin['volume_24h']:.2f}</p>
                </a>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # Kartların kapanış divi  

# Veri Görselleştirme Sayfası
elif page == "Veri Görselleştirme":
    selected_coin_id = st.experimental_get_query_params().get("selected_coin", [None])[0]

    if selected_coin_id:
        # Coin verilerini getirme
        coin_data = get_coin_data()
        selected_coin = next(coin for coin in coin_data if coin['id'] == selected_coin_id)

        # Veri görselleştirme kısmı
        st.markdown(f"<h2>{selected_coin['name']} - Fiyat Verisi</h2>", unsafe_allow_html=True)
        st.write(f"**Fiyat:** ${selected_coin['price']:.2f}")
        st.write(f"**24H Değişim:** {selected_coin['change_24h']:.2f}%")
        st.write(f"**24H Hacim:** ${selected_coin['volume_24h']:.2f}")
        
        # Burada veri görselleştirme işlemini gerçekleştirebilirsiniz, örneğin:
        # - Coin'in tarihsel verilerini görselleştirmek
        # - Zaman serisi grafiği oluşturmak
        # vb.
