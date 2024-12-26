import streamlit as st
import ollama

# Sayfa ayarları
st.set_page_config(
    page_title="TraderMentorAI",
    page_icon="C:\\Users\\rusen\\source\\repos\\Proje\\Proje\\TradeMentor-AI\\streamlit\\images\\Leonardo_Phoenix_Create_a_modern_sleek_logo_for_the_stock_trad_2.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sohbet geçmişini başlat
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Başlık
st.title("TraderMentorAI ile Sohbet")

# Sohbet geçmişini görüntüle
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcının yeni mesajını al
if prompt := st.chat_input("Mesajınızı yazın..."):
    # Kullanıcının mesajını geçmişe ekle
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Kullanıcının mesajını göster
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant'ın yanıtını al ve göster
    with st.chat_message("assistant"):
        with st.spinner("Yanıt alınıyor..."):
            try:
                response = ollama.chat(model="llama3:latest", messages=st.session_state["messages"])
                if "message" in response:
                    assistant_message = response["message"]["content"]
                else:
                    assistant_message = "Bir hata oluştu veya yanıt alınamadı."
            except Exception as e:
                assistant_message = f"Bir hata oluştu: {e}"

        st.markdown(assistant_message)
        
        # Yanıtı geçmişe ekle
        st.session_state["messages"].append({"role": "assistant", "content": assistant_message})
