import streamlit as st
import requests

# NewsAPI anahtarınızı buraya ekleyin
api_key = "dc482f4ae1fc4005bd3b6887d20e8c90"

# Streamlit ile başlık ve arama terimi almak
st.title('Türkçe Haber Başlıkları')
query = st.text_input('Arama Terimi Girin:', 'Teknoloji')

# API'yi çağırma ve haberleri çekme fonksiyonu
def get_news(query):
    url = f'https://newsapi.org/v2/everything?q={query}&language=tr&apiKey={api_key}'
    response = requests.get(url)
    return response.json()

# Haberleri çekme
if query:
    news_data = get_news(query)

    if news_data['status'] == 'ok':
        articles = news_data['articles']
        
        # Başlıkları listele
        for article in articles:
            st.subheader(article['title'])
            st.write(f"Yayın Tarihi: {article['publishedAt']}")
            st.write(f"{article['description']}")
            st.write(f"Detaylar: [{article['title']}]({article['url']})")
            st.markdown("---")
    else:
        st.error("Haberler alınırken bir hata oluştu.")
