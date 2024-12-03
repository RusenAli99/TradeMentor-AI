import ollama
import streamlit as st
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

# Modelin tam yanıtını döndüren fonksiyon
def get_full_response():
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=st.session_state["messages"],
        stream=True,
    )
    full_message = ""
    for chunk in stream:
        full_message += chunk["message"]["content"]  # Gelen tüm parçaları birleştir
    return full_message

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

    # Assistant'ın tam yanıtını al
    with st.chat_message("assistant"):
        message = get_full_response()  # Tüm parçaları birleştirip tek yanıt al
        st.markdown(message)  # Yanıtı göster

        # Assistant yanıtını geçmişe ekle
        st.session_state["messages"].append({"role": "assistant", "content": message})
