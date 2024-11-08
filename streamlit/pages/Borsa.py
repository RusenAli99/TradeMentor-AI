import streamlit as st
import datetime
import yfinance as yf
import time

# Kullanıcıdan sembol ve tarih bilgilerini al
symbol = st.sidebar.text_input('Hisse Senedi Sembolü', value='GOOGL')
st.title(symbol + ' Hisse Senedi Grafiği')
start_date = st.sidebar.date_input('Başlangıç tarihi', value=datetime.datetime(2020, 1, 1))
end_date = st.sidebar.date_input('Bitiş tarihi', value=datetime.datetime.now())

# Döngü için bir boş alan oluşturuyoruz
chart_placeholder = st.empty()
table_placeholder = st.empty()

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

    # 5 saniye bekle
    time.sleep(5)
