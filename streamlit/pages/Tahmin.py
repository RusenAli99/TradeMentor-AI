import streamlit as st
from vega_datasets import data # type: ignore
import pandas as pd
from PIL import Image

TİTLE="TAHMİN"
st.set_page_config(
    page_title="TraderMentorAI",
    page_icon = "C:\\Users\\omera\\Desktop\\STREAMLIT\\streamlit_TradeMentorAi\\images\\Leonardo_Phoenix_Create_a_modern_sleek_logo_for_the_stock_trad_2.jpg", # Updated icon path
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title(TİTLE)