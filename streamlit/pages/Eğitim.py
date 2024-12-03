import streamlit as st
import requests

# Sayfa ayarlarını yapılandır
st.set_page_config(
    page_title="TraderMentorAI",
    page_icon="C:\\Users\\rusen\\source\\repos\\Proje\\Proje\\TradeMentor-AI\\streamlit\\images\\Leonardo_Phoenix_Create_a_modern_sleek_logo_for_the_stock_trad_2.jpg", 
    layout="wide",
    initial_sidebar_state="expanded",   
)

# Başlık
st.title("TraderMentorAI")

# Kripto Borsası başlığını oluştur
with st.expander("1.1 - Kripto Borsasına Yeni Girdim Nelere Dikkat Etmeliyim?"):
    st.write("Bu konu hakkında daha fazla bilgi almak için aşağıdaki videoyu izleyebilirsiniz.")
    
    # Video yalnızca başlık genişletildiğinde gösterilir
    video_path = "C:\\Users\\rusen\\Desktop\\1203(1).mp4"
    st.video(video_path)