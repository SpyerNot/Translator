import streamlit as st
import io
import speech_recognition as sr
from pydub import AudioSegment

import os

st.set_page_config(layout="centered")

st.title("Speech-to-Text Converter")
st.markdown("Upload an audio file (e.g., MP3, WAV, M4A) to transcribe.")

uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"], key="audio_uploader")



if uploaded_file is not None:
    st.info("Processing audio file... Please wait.")

    audio_bytes = uploaded_file.read()
    st.audio(audio_bytes, format=uploaded_file.type)

    try:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format=uploaded_file.type.split('/')[-1])

        wav_audio_bytes_io = io.BytesIO()
        audio_segment.export(wav_audio_bytes_io, format="wav")
        wav_audio_bytes_io.seek(0)

        r = sr.Recognizer()

        with sr.AudioFile(wav_audio_bytes_io) as source:
            st.write("Reading audio for transcription...")
            audio_data = r.record(source)

        st.info("Transcribing audio... This may take a moment.")
        
        transcribed_text = r.recognize_google(audio_data)

        st.subheader("Transcribed Text:")
        
        st.text_area("Transcription Result", transcribed_text, height=200, key="transcribed_text_area")
        st.success("Audio transcribed successfully!") #YAYAYAYAYAYAYA

        
        st.download_button(
            label="Download Transcription as TXT",
            data=transcribed_text,
            file_name="transcription.txt",
            mime="text/plain",
            key="download_transcription"
        )

    except sr.UnknownValueError:
        st.warning("Speech Recognition could not understand audio. Please try another file or ensure speech is clear.")
        
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Web Speech API service; check your internet connection: {e}")
        
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.warning("Please ensure all necessary libraries are installed and `ffmpeg` is available on the system.")



else:
    st.info("Please upload an audio file to begin transcription.")

st.sidebar.info("This is the Speech-to-Text page.")
