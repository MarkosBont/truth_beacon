import streamlit as st
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