import streamlit as st
import pymongo
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Streamlit sayfa yapılandırması
st.set_page_config(
    page_title="TraderMentorAI",
    page_icon="C:\\Users\\rusen\\source\\repos\\Proje\\Proje\\TradeMentor-AI\\streamlit\\images\\Leonardo_Phoenix_Create_a_modern_sleek_logo_for_the_stock_trad_2.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# MongoDB'den veri çekme
def fetch_data_from_mongodb(uri, database_name, collection_name):
    try:
        client = pymongo.MongoClient(uri)
        db = client[database_name]
        collection = db[collection_name]
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)  # Son 3 ay
        
        data = list(collection.find(
            {"time": {"$gte": start_date.strftime("%Y-%m-%d %H:%M:%S"), "$lte": end_date.strftime("%Y-%m-%d %H:%M:%S")}}
        ))
        client.close()
        
        if not data:
            st.error("Seçilen koleksiyon için veri bulunamadı.")
            return pd.DataFrame()

        df = pd.DataFrame(data)
        if 'time' not in df or 'close' not in df:
            st.error("Veri setinde 'time' veya 'close' sütunları eksik.")
            return pd.DataFrame()

        df['time'] = df['time'].astype(str)
        df.sort_values('time', inplace=True)
        return df[['time', 'close']]
    except Exception as e:
        st.error(f"MongoDB'den veri çekme hatası: {e}")
        return pd.DataFrame()

# Veri setini hazırlama
def preprocess_data(df):
    df.set_index('time', inplace=True)  
    return df[['close']]

# Zaman serisi verisini pencereleme
def create_dataset(data, look_back=60):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:i + look_back])
        y.append(data[i + look_back])
    return np.array(X), np.array(y)

# Model oluşturma
def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(100, return_sequences=True, input_shape=input_shape),
        LSTM(100),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Tahmin işlemi
def predict_for_collection(uri, database_name, collection_name):
    df = fetch_data_from_mongodb(uri, database_name, collection_name)
    if df.empty:
        return None, None, None, None

    df = preprocess_data(df)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))
    
    look_back = 60
    X, y = create_dataset(scaled_data, look_back)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    model = build_lstm_model((X_train.shape[1], 1))
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=0)
    
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)
    y_test = scaler.inverse_transform(y_test.reshape(-1, 1))
    
    result_df = pd.DataFrame({
        "Gerçek Değer": y_test.flatten(),
        "Tahmin": predictions.flatten()
    })
    
    return result_df, y_test.flatten(), predictions.flatten(), df

# Grafik ile görselleştirme
def plot_results(real_values, predicted_values):
    # Stil değişikliği
    plt.style.use('dark_background')  # Karanlık arka plan stili

    
    # Grafik boyutu
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Gerçek değerleri ve tahminleri çizme
    ax.plot(real_values, label="Gerçek Değer", color='blue', linewidth=2)
    ax.plot(predicted_values, label="Tahmin Edilen Değer", color='red', linestyle='--', linewidth=2)
    
    # Başlık ve etiketler
    ax.set_title("Gerçek Değer vs Tahmin Edilen Değer", fontsize=16, fontweight='bold', color='darkblue')
    ax.set_xlabel("Zaman", fontsize=12, color='darkgreen')
    ax.set_ylabel("Fiyat", fontsize=12, color='darkgreen')
    
    # Efsane (legend) ve grid
    ax.legend(fontsize=12, loc='upper left', frameon=False)
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='gray')  # Grid çizgisi
    
    return fig

# Yorum ve görsel belirleme
def generate_trade_signal(real_value, predicted_value):
    percentage_difference = (predicted_value - real_value) / real_value * 100
    if percentage_difference > 3:
        return "Yüksek Al", "C:\\Users\\rusen\\Desktop\\veriproje\\3.png"
    elif percentage_difference < -3:
        return "Yüksek Sat", "C:\\Users\\rusen\\Desktop\\veriproje\\1.png"
    else:
        return "Tut", "C:\\Users\\rusen\\Desktop\\veriproje\\2.png"

# Streamlit arayüzü
def main():
    uri = "mongodb://localhost:27017/"  
    database_name = "proje"            

    collections = ["ADA", "BNB", "BTC", "DOGE", "DOGS", "ETH", "MATIC", "NOT", "SHIB", "SOL", "TON", "XRP"]

    st.title("Kripto Para Tahmin Sistemi")
    collection_name = st.selectbox("Bir kripto para seçin", collections)

    if st.button('Tahmin Yap'):
        try:
            result_df, real_values, predicted_values, df = predict_for_collection(uri, database_name, collection_name)
            if result_df is None:
                st.error("Tahmin yapılamadı.")
                return

            st.write("Tahmin Sonuçları:")
            st.dataframe(result_df.head())
            
            fig = plot_results(real_values, predicted_values)
            st.pyplot(fig)
            
            trade_signal, image_path = generate_trade_signal(real_values[-1], predicted_values[-1])
            st.write("Ticaret Sinyali: ", trade_signal)
            st.image(image_path, width=250)  # Fotoğraf genişliği 250 piksel olarak ayarlandı
        
        except Exception as e:
            st.error(f"Hata oluştu: {e}")

if __name__ == "__main__":
    main()