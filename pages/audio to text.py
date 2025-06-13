import streamlit as st
import io
import speech_recognition as sr
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

st.set_page_config(layout="centered")

st.title("Audio-to-Text Converter")
st.markdown("Upload any audio file (MP3, WAV, M4A, OGG, FLAC, etc.) to transcribe.")

uploaded_file = st.file_uploader("Upload an audio file", key="audio_uploader")

if uploaded_file is not None:
    with st.spinner("Processing audio file... Please wait."):
        audio_bytes = uploaded_file.read()
        st.audio(audio_bytes, format=uploaded_file.type)

        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            try:
                audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format=file_extension)
            except CouldntDecodeError:
                st.error(
                    f"Error: Could not decode the audio file. "
                    f"The format '{file_extension}' may be unsupported or the file is corrupt. "
                    "Please try a different file or format (e.g., MP3, WAV, M4A)."
                )
                st.stop()

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
            st.success("Audio transcribed successfully!")


            
            st.download_button(
                label="Download Transcription as TXT",
                data=transcribed_text,
                file_name="transcription.txt",
                mime="text/plain",
                key="download_transcription"
            )

        except sr.UnknownValueError:
            st.warning("Speech Recognition could not understand the audio. The speech might be unclear or the file may contain silence.")

        
        except sr.RequestError as e:
            st.error(f"Could not request results from Google's Speech Recognition service; check your internet connection: {e}")


        
        except Exception as e:
            st.error(f"An unexpected error occurred during transcription: {e}")

else:
    st.info("Please upload an audio file to begin transcription.")


st.sidebar.info("This is the Speech-to-Text page.")
