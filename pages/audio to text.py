import streamlit as st
import io
import speech_recognition as sr
from pydub import AudioSegment

from st_audiorec import st_audiorec #YAYAYAYAYAYA

def process_and_transcribe(audio_bytes, source_type, file_extension=None):
    st.info(f"Processing audio from {source_type}... Please wait.")
    st.audio(audio_bytes)

    try:
        format_to_use = file_extension if file_extension else "wav"
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format_to_use)
        
        wav_audio_bytes_io = io.BytesIO()
        audio_segment.export(wav_audio_bytes_io, format="wav")
        wav_audio_bytes_io.seek(0)

        r = sr.Recognizer()
        with sr.AudioFile(wav_audio_bytes_io) as source:
            audio_data = r.record(source)

        st.info("Transcribing audio... This may take a moment.")
        transcribed_text = r.recognize_google(audio_data)

        st.subheader("Transcribed Text:")
        st.text_area("Transcription Result", transcribed_text, height=200, key=f"transcribed_text_{source_type}")
        st.success("Audio transcribed successfully!")

        st.download_button(
            label="Download Transcription as TXT",
            data=transcribed_text,
            file_name="transcription.txt",
            mime="text/plain",
            key=f"download_{source_type}"
        )

    except sr.UnknownValueError:
        st.warning("Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google's API: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


st.set_page_config(layout="centered")
st.title("VerbalEyes")
st.markdown("### See with Sound, Speak with Text")
st.markdown("---")

st.subheader("Option 1: Transcribe an Audio File")
uploaded_file = st.file_uploader("Upload an audio file", key="audio_uploader")

if uploaded_file is not None:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    process_and_transcribe(uploaded_file.read(), source_type="uploaded_file", file_extension=file_ext)


st.markdown("<h3 style='text-align: center; color: grey;'>OR</h3>", unsafe_allow_html=True)


st.subheader("Option 2: Record Audio Directly")

wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    process_and_transcribe(wav_audio_data, source_type="recording")
