import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import streamlit as st
import warnings

# Uyarıları yok sayma
warnings.filterwarnings('ignore')

# LSTM Modeli (Eğitim için kullanılan modelin aynısı)
class LSTMModel(nn.Module):
    def _init_(self, input_size=1, hidden_layer_size=20, output_size=1):
        super(LSTMModel, self)._init_()
        self.lstm = nn.LSTM(input_size, hidden_layer_size, batch_first=True)
        self.fc = nn.Linear(hidden_layer_size, output_size)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        predictions = self.fc(lstm_out[:, -1, :])  # Sadece son zaman adımını alıyoruz
        return predictions

# Veriyi hazırlama
def prepare_data(data, look_back=60):
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data['close'].values.reshape(-1, 1))

    X, y = [], []
    for i in range(look_back, len(data_scaled) - 1):  # Son adımı çıkarıyoruz
        X.append(data_scaled[i-look_back:i, 0])  # Son 60 günü kullanacağız
        y.append(data_scaled[i + 1, 0])  # Sadece bir sonraki günü tahmin edeceğiz

    X = np.array(X)
    y = np.array(y)

    # PyTorch tensörlerine dönüştürme
    X = torch.tensor(X, dtype=torch.float32).unsqueeze(-1)
    y = torch.tensor(y, dtype=torch.float32).unsqueeze(-1)

    return X, y, scaler

# Modeli yükleme
def load_model(coin_name, model_path='./models/'):
    model = LSTMModel()
    model_save_path = os.path.join(model_path, f"{coin_name}_model.pt")
    model.load_state_dict(torch.load(model_save_path))
    model.eval()
    return model

# Tahmin yapma
def make_prediction(model, X_test, scaler, device):
    last_60_days = X_test[-1].unsqueeze(0)  # Son 60 gün verisi
    model.to(device)
    last_60_days = last_60_days.to(device)
    
    with torch.no_grad():
        prediction = model(last_60_days)
    
    # Tahmini orijinal ölçekle geri çevirme
    prediction = prediction.cpu().numpy()
    prediction = scaler.inverse_transform(prediction)
    
    return prediction[0][0]

# Kullanım
def predict_for_all_coins(coin_data_files, model_path='./models/'):
    # Cihaz (GPU varsa GPU, yoksa CPU kullanacağız)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    st.write(f"Model tahminleri için {device} kullanılacak.")
    
    predictions = []
    
    for coin_name, file_path in coin_data_files.items():
        st.write(f"\n{coin_name} için tahmin yapılıyor...")
        
        # Veriyi yükle
        data = pd.read_csv(file_path)
        
        # Veriyi hazırlama
        X_test, _, scaler = prepare_data(data)

        # Modeli yükleme
        model = load_model(coin_name, model_path=model_path)

        # Tahmin yapma
        prediction = make_prediction(model, X_test, scaler, device)
        
        # Tahmin değerini listeye ekle
        predictions.append((coin_name, prediction))
    
    # Tahminlerin görselleştirilmesi
    st.write("Tahmin Sonuçları:")
    
    for coin_name, prediction in predictions:
        st.write(f"{coin_name} için ertesi gün tahmini: {prediction:.2f}")
    
    # Görselleştirme - Tahminlerin grafiği
    coin_names = [coin_name for coin_name, _ in predictions]
    coin_predictions = [prediction for _, prediction in predictions]
    
    plt.figure(figsize=(10, 6))
    plt.bar(coin_names, coin_predictions, color='skyblue')
    plt.title('Coin Tahmin Sonuçları')
    plt.xlabel('Coin')
    plt.ylabel('Tahmin Edilen Değer')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

# Coin dosyalarının yolu
coin_data_files = {
    'ADA': 'ADA_1y_hourly.csv',
    'BNB': 'BNB_1y_hourly.csv',
    'BTC': 'BTC_1y_hourly.csv',
    'DOGS': 'DOGS_1y_hourly.csv',
    'ETH': 'ETH_1y_hourly.csv',
    'MATIC': 'MATIC_1y_hourly.csv',
    'SHIB': 'SHIB_1y_hourly.csv',
    'SOL': 'SOL_1y_hourly.csv',
    'TON': 'TON_1y_hourly.csv',
    'XRP': 'XRP_1y_hourly.csv',
}

# Streamlit uygulamasını başlat
if _name_ == '_main_':
    st.title('Coin Tahmin Modeli')
    st.write("Bu uygulama, belirli coinler için LSTM modeli kullanarak ertesi gün tahminleri yapmaktadır.")
    
    predict_for_all_coins(coin_data_files)