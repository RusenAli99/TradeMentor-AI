import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="TradeMentor Ai")
st.title("SOHBET")
# İletişim baloncuğu
def contact_bubble():
    st.markdown(
        """
        <style>
        .contact-bubble {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #007BFF; /* Mavi arka plan */
            color: white; /* Yazı rengi */
            border-radius: 50%; /* Yuvarlak şekil */
            width: 50px; /* Genişlik */
            height: 50px; /* Yükseklik */
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            cursor: pointer;
            font-size: 20px;
            text-decoration: none;
        }
        </style>
        <a class="contact-bubble" href="https://servispy-2etfjh5ephbuz2qeltdvsk.streamlit.app/" target="_blank">
            📞
        </a>
        """,
        unsafe_allow_html=True
    )

# İletişim baloncuğunu göster
contact_bubble()
