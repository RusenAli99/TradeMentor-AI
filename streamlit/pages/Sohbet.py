import ollama
import streamlit as st

st.title("Ollama Python Chatbot")

# Geçmişi başlat
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Modeli başlat
if "model" not in st.session_state:
    st.session_state["model"] = None  # Başlangıçta model belirlenmemiş

# Mevcut modelleri listele
models = [model["name"] for model in ollama.list()["models"]]

# Eğer daha önce kaydedilen model mevcutsa, onu seç
if st.session_state["model"] not in models:
    st.session_state["model"] = models[0]  # Mevcut modellerden ilkini seç

# Kullanıcıya model seçtirme
st.session_state["model"] = st.selectbox("Choose your model", models, index=models.index(st.session_state["model"]))

# Modelin yanıtlarını akış olarak getiren fonksiyon
def model_res_generator():
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=st.session_state["messages"],
        stream=True,
    )
    full_message = ""
    # Gelen her bir akış parçasını birleştir
    for chunk in stream:
        full_message += chunk["message"]["content"]
        yield full_message  # Yanıtı anlık olarak gönder

# Chat geçmişini görüntüle
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcının yeni mesajını al
if prompt := st.chat_input("What is up?"):
    # Kullanıcının mesajını geçmişe ekle
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Kullanıcının mesajını göster
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant'ın yanıtını almak için stream başlat
    with st.chat_message("assistant"):
        message = ""
        for chunk in model_res_generator():
            message = chunk  # Yanıtı anlık olarak güncelle
            st.markdown(message)  # Anlık olarak göster
        # Assistant yanıtını geçmişe ekle
        st.session_state["messages"].append({"role": "assistant", "content": message})
