import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from claim_verifier.text_fact_checking import speech_fact_check_webDriver
import tempfile


st.markdown("""
    <style>
    h1, h2, p, button{
        text-align: center;
    }

    .upload-instructions {
        text-align: center;
        margin-top: -10px;
        margin-bottom: 30px;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("<h1>Fake News Detector</h1>", unsafe_allow_html=True)
st.markdown("<h2>Drag and Drop Your Video Anywhere</h2>", unsafe_allow_html=True)
st.markdown("<p class='upload-instructions'>Supported Formats: .mp4, .mov</p>", unsafe_allow_html=True)


file = st.file_uploader("", type=["mp4", "mov"])


if file:
    os.makedirs("fact_check_uploads", exist_ok=True)
    temp_path = os.path.abspath(os.path.join("fact_check_uploads", file.name))
    with open(temp_path, "wb") as f:
        f.write(file.read())

    st.video(file)
    st.write(f"📁 Temp path: {temp_path}")
    st.write(f"📦 Exists: {os.path.exists(temp_path)}")
    st.write(f"📏 Size: {os.path.getsize(temp_path)} bytes")

    if st.button("FACT CHECK"):
        with st.spinner("Transcribing and verifying..."):
            result = speech_fact_check_webDriver(temp_path)
            st.write(result)