import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import streamlit as st
from claim_verifier.text_fact_checking import speech_fact_check_webDriver, speech_fact_check_serpAPI
from claim_verifier.llm_fact_check import full_llm_fact_check
from streamlit_utils.utils import display_individual_claims, display_individual_claims_from_llm


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


st.markdown("<h1>Truth Beacon</h1>", unsafe_allow_html=True)
st.markdown("<h2>Drag and Drop Your Video Below</h2>", unsafe_allow_html=True)
st.markdown("<p class='upload-instructions'>Supported Formats: .mp4 .mov</p>", unsafe_allow_html=True)


file = st.file_uploader("file", type=["mp4", "mov"], label_visibility="hidden")


if file:
    os.makedirs("fact_check_uploads", exist_ok=True)
    temp_path = os.path.abspath(os.path.join("fact_check_uploads", file.name))
    with open(temp_path, "wb") as f:
        f.write(file.read())

    video = st.video(file)

    if video:
        if st.button("FACT CHECK"):
            with st.spinner("Transcribing and verifying..."):
                final = full_llm_fact_check(temp_path)
                display_individual_claims_from_llm(final)

