import streamlit as st
import requests
import tempfile
model_name="openai/whisper-large-v3"
API_URL = f"https://router.huggingface.co/hf-inference/models/{model_name}"
headers = {"Authorization": 'Bearer ' + st.secrets["HUGGINGFACE_TOKEN2"]}




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

        payload = {'inputs': tmp.name}
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Check for errors in the response
    st.markdown(response)