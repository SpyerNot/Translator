import streamlit as st
from gtts import gTTS
import tempfile

st.title("🗣️ Text to Speech (gTTS)")

text = st.text_area("Enter text to convert to audio:")

if st.button("Convert and Play"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Converting text to speech..."):
            tts = gTTS(text)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                tts.save(tmpfile.name)
                st.audio(tmpfile.name, format='audio/mp3')
