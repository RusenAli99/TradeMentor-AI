import streamlit as st
import datetime
import yfinance as yf
import time
import requests

# NewsAPI anahtarınız
api_key = "dc482f4ae1fc4005bd3b6887d20e8c90"

# Kullanıcıdan sembol ve tarih bilgilerini al
symbol = st.sidebar.text_input('Hisse Senedi Sembolü', value='GOOGL')
st.title(symbol + ' Hisse Senedi Grafiği')
start_date = st.sidebar.date_input('Başlangıç tarihi', value=datetime.datetime(2020, 1, 1))
end_date = st.sidebar.date_input('Bitiş tarihi', value=datetime.datetime.now())

# Döngü için bir boş alan oluşturuyoruz
chart_placeholder = st.empty()
table_placeholder = st.empty()
news_placeholder = st.empty()

# Haberleri sadece bir kez çekme
news_data = None
if symbol:
    news_url = f'https://newsapi.org/v2/everything?q={symbol}&language=tr&apiKey={api_key}'
    response = requests.get(news_url)
    
    # API yanıtını kontrol et
    if response.status_code == 200:
        news_data = response.json()
        if 'articles' not in news_data:
            news_data = {"status": "error", "message": "No articles found."}
    else:
        news_data = {"status": "error", "message": "NewsAPI request failed"}

# Ana döngü
while True:
    # Verileri indir
    df = yf.download(symbol, start=start_date, end=end_date)

    # Grafiği ve tabloyu boş alanlara yerleştir
    with chart_placeholder:
        st.subheader(symbol + ' Hisse Senedi Grafiği')
        st.line_chart(df['Close'])

    with table_placeholder:
        st.subheader('Hisse Senedi Fiyatlar Tablosu')
        st.write(df)

    # Haberleri bir kez göster
    if news_data and news_data['status'] == 'ok' and 'articles' in news_data:
        with news_placeholder:
            st.subheader(f'{symbol} Hakkındaki Türkçe Haberler')
            for article in news_data['articles']:
                st.subheader(article['title'])
                st.write(f"Yayın Tarihi: {article['publishedAt']}")
                st.write(f"{article['description']}")
                st.write(f"Detaylar: [{article['title']}]({article['url']})")
                st.markdown("---")
    elif news_data and news_data['status'] == 'error':
        with news_placeholder:
            st.error("Haberler alınırken bir hata oluştu. Lütfen daha sonra tekrar deneyin.")

    # 5 saniye bekle sadece hisse senedi verilerini güncellemek için
    time.sleep(5)
