import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import streamlit as st
from claim_verifier.text_fact_checking import speech_fact_check_webDriver, speech_fact_check_serpAPI
from utils import extract_real_url, get_source_name_from_url


def display_individual_claims(results):
    st.title("Fact Check Results")

    st.subheader("Sentence-Level Analysis:")

    if not results:
        st.warning("No claims were extracted or analyzed.")
        return

    for i, entry in enumerate(results, 1):
        with st.expander(f"💬 Claim {i}: {entry.get('claim', '[No claim]')}"):
            verdict = entry.get("verdict", "Unknown").upper()

            # Verdict display
            if verdict == "TRUE":
                st.success("✅ Verdict: TRUE")
                st.write("Supporting links:")

            elif verdict == "FALSE":
                st.error("❌ Verdict: FALSE")
                st.write("Refuting Links:")

            elif verdict == "NO-DATA":
                st.warning("⚠️ This claim is unclear, please fact check manually if necessary.")

            elif verdict == "UNC-CONFLICT":
                st.warning("⚠️ There was a conflict in the evidence found, please evaluate from these sources")

            elif verdict == "UNC-NOT-ENOUGH-DATA":
                st.warning("⚠️ Sorry! Not enough data was found.")

            else:
                st.warning("⚠️ Sorry! This claim was not clear, therefore could not be analysed.")


            # Evidence display
            if verdict == "TRUE":
                links = entry.get("support_links", "No links were found")
                for link in links:
                    if link.startswith("javascript:"):
                        continue

                    real_url = extract_real_url(link)
                    source = get_source_name_from_url(real_url)
                    st.markdown(f"[Read source - {source}]({real_url})", unsafe_allow_html=True)

            elif verdict == "FALSE":
                links = entry.get("refute_links", "No links were found")
                for link in links:
                    if link.startswith("javascript:"):
                        continue

                    real_url = extract_real_url(link)
                    source = get_source_name_from_url(real_url)
                    st.markdown(f"[Read source - {source}]({real_url})", unsafe_allow_html=True)

            elif verdict == "UNC-CONFLICT":
                all_links = [entry.get("support_links", "No supporting links were found"),
                             entry.get("refute_links", "No refute links were found")]

                for link in all_links:
                    if link.startswith("javascript:"):
                        continue

                    real_url = extract_real_url(link)
                    source = get_source_name_from_url(real_url)
                    st.markdown(f"[Read source - {source}]({real_url})", unsafe_allow_html=True)



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
st.markdown("<h2>Drag and Drop Your Video Anywhere</h2>", unsafe_allow_html=True)
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
                final = speech_fact_check_serpAPI(temp_path)
                display_individual_claims(final)

