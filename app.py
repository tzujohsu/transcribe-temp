import streamlit as st
import whisper
import requests
import tempfile

model = whisper.load_model("turbo")

if st.button("Transcribe Audio"):
    with st.spinner("Transcribing..."):
        response = requests.get(
            "https://dcs-spotify.megaphone.fm/WSJ7365847900.mp3", 
            stream=True
        )
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
            for chunk in response.iter_content(chunk_size=8192):
                tmp.write(chunk)
            tmp.flush()  # Ensure data is fully written

            result = model.transcribe(tmp.name)

    st.markdown(result["text"])