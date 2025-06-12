
import streamlit as st
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import os

st.title("🗣️ Text to Speech Converter")

text = st.text_area("Enter text you want to convert to speech:")

if st.button("Convert and Play"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Converting to speech..."):
            # Initialize TTS engine
            engine = pyttsx3.init()
            temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            engine.save_to_file(text, temp_wav.name)
            engine.runAndWait()

            st.success("Conversion complete!")

            audio_bytes = open(temp_wav.name, 'rb').read()
            st.audio(audio_bytes, format='audio/wav')

            # Clean up
            temp_wav.close()
            os.remove(temp_wav.name)

