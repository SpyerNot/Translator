import streamlit as st
import io
import speech_recognition as sr
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from st_audiorecorder import audio_recorder

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
            st.write("Reading audio for transcription...")
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

    except CouldntDecodeError:
        st.error(
            f"Error: Could not decode the audio file. "
            f"The format '{format_to_use}' may be unsupported or the file is corrupt."
        )
    except sr.UnknownValueError:
        st.warning("Speech Recognition could not understand the audio. The speech might be unclear or the file may contain silence.")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google's Speech Recognition service; check your internet connection: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred during transcription: {e}")


st.set_page_config(layout="centered")
st.title("VerbalEyes") #Verbalise!!!!


st.markdown("---")

st.subheader("Option 1: Transcribe an Audio File")
uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV, M4A, etc.)", key="audio_uploader")

st.markdown("<h3 style='text-align: center; color: grey;'>OR</h3>", unsafe_allow_html=True)

st.subheader("Option 2: Record Audio Directly")

recorded_audio_bytes = audio_recorder(
    text="Click to Record",
    recording_color="#e8b62c",
    neutral_color="#6a6a6a",
    icon_name="microphone",
    icon_size="3x",
)

if uploaded_file is not None:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    process_and_transcribe(uploaded_file.read(), source_type="uploaded file", file_extension=file_ext)
elif recorded_audio_bytes:
    process_and_transcribe(recorded_audio_bytes, source_type="recording")

st.sidebar.info("This is the Speech-to-Text page.")
