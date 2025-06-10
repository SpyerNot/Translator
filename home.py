import streamlit as st
st.title("Welcome to the translator!")
st.page_link("home.py", label= "Home", icon="🏠")
st.page_link("pages/text to audio.py", label= "Text to audio", icon = "💬")
st.page_link("pages/audio to text.py", label = "Audio to Text", icon = "🎤")
st.divider()
st.write("This is made by group I21")
