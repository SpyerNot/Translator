import streamlit as st
import io
import speech_recognition as sr
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError


from streamlit_webrtc import webrtc_streamer, AudioProcessorBase

class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self._frames = []

    def recv(self, frame):
        self._frames.append(frame)
        return frame

    def on_ended(self):
        if not self._frames:
            return

        sound = AudioSegment.empty()
        for frame in self._frames:
            sound += AudioSegment(
                data=frame.to_ndarray().tobytes(),
                sample_width=frame.format.bytes,
                frame_rate=frame.sample_rate,
                channels=len(frame.layout.channels),
            )
        self._frames = []
        
        st.session_state["audio_buffer"] = sound


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
        st.error(f"Error: Could not decode the audio file.")
    except sr.UnknownValueError:
        st.warning("Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google's API: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


st.set_page_config(layout="centered")

st.subheader("Option 1: Transcribe an Audio File")
uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV, M4A, etc.)", key="audio_uploader")

st.markdown("<h3 style='text-align: center; color: grey;'>OR</h3>", unsafe_allow_html=True)

st.subheader("Option 2: Record Audio Directly")

webrtc_streamer(
    key="audio-recorder",
    audio_processor_factory=AudioRecorder,
    media_stream_constraints={"video": False, "audio": True},
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


if uploaded_file is not None:
    
    file_ext = uploaded_file.name.split('.')[-1].lower()
    process_and_transcribe(uploaded_file.read(), source_type="uploaded file", file_extension=file_ext)

elif "audio_buffer" in st.session_state:
    
    st.info("Recording complete. Transcribing now...")
    
    recorded_audio_segment = st.session_state["audio_buffer"]
    
    wav_bytes_io = io.BytesIO()
    recorded_audio_segment.export(wav_bytes_io, format="wav")
    
    process_and_transcribe(wav_bytes_io.getvalue(), source_type="recording")
    
    del st.session_state["audio_buffer"]


st.sidebar.info("This is the Speech-to-Text page.")
