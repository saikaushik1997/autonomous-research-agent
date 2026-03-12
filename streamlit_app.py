import streamlit as st
import requests
import time

API_URL = "https://autonomous-research-agent.onrender.com"

# cold start problem on the research web service
def warmup_api(retries: int = 5, wait: int = 10) -> bool:
    for attempt in range(retries):
        try:
            r = requests.get(f"{API_URL}/health", timeout=10)
            if r.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(wait)
    return False

st.set_page_config(page_title="Research Agent", page_icon="🔬")
st.title("🔬 Research Agent")

namespace = st.text_input("Namespace", value="gibbs-2.pdf")
topic = st.text_area("Topic", placeholder="e.g. Gibbs sampling for multiple sequence alignment")

if st.button("Research", type="primary", disabled=not topic):
    with st.spinner("Warming up..."):
        if not warmup_api(retries=3, wait=5):
            st.error("API unavailable.")
            st.stop()

    with st.spinner("Researching..."):
        try:
            r = requests.post(
                f"{API_URL}/api/v1/research",
                json={"topic": topic, "namespace": namespace},
                timeout=120
            )
            r.raise_for_status()
            result = r.json()
            st.divider()
            st.markdown(result["report"])
            st.caption(f"{result['messages_count']} messages")
        except requests.exceptions.Timeout:
            st.error("Timed out — try a more specific topic.")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed: {e}")