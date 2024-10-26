import requests
import time
from pymongo import MongoClient
from datetime import datetime

# MongoDB bağlantısını ayarla
client = MongoClient("mongodb://localhost:27017/")  # Yerel sunucuya bağlanma
db = client["proje"]  # 'proje' veritabanı
collection = db["proje"]  # 'proje' koleksiyonu

# Bağlantının doğru yapıldığını kontrol etmek için bir test çıktısı
print("MongoDB'ye başarıyla bağlanıldı.")

# API URL ve parametreler
url = "https://min-api.cryptocompare.com/data/price"
crypto_symbols = ["BTC", "ETH","ADA","BNB","DOGE","DOGS","MATIC","NOT","SHIB","SOL","TON","XRP"]  # Fiyatını almak istediğiniz kripto para birimleri
currencies = "USD,EUR,TRY"  # Fiyat bilgisi almak istediğiniz para birimleri

# Başlıklara (Headers) API anahtarını ekleyin
headers = {
    "authorization": "Apikey YOUR_API_KEY"  # YOUR_API_KEY kısmına kendi API anahtarınızı koyun
}

# Sonsuz döngü
while True:
    for symbol in crypto_symbols:
        parameters = {
            "fsym": symbol,
            "tsyms": currencies
        }
        
        # API'yi çağır
        response = requests.get(url, params=parameters, headers=headers)

        # Yanıtı alın
        if response.status_code == 200:
            data = response.json()
            print(f"{symbol} Fiyatları: {data}")  # Her kripto para için fiyat verileri

            # MongoDB'ye eklemeden önce veriyi kontrol etmek
            record = {
                "symbol": symbol,
                "prices": data,
                "timestamp": datetime.utcnow()  # UTC zaman damgası
            }

            # Kayıt yapıldığını doğrulamak için veriyi ekrana yazdır
            print("Kaydedilecek veri:", record)

            # MongoDB'ye ekle ve eklenen dokümanın ID'sini yazdır
            inserted_id = collection.insert_one(record).inserted_id
            print(f"{symbol} verileri MongoDB'ye kaydedildi. Kaydedilen ID: {inserted_id}")
        else:
            print(f"API Hatası ({symbol}):", response.status_code)
    
    # 10 saniye bekle
    time.sleep(10)
