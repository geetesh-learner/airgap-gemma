import streamlit as st

from hackathon_toolkit.ollama_client import query_gemma

st.set_page_config(
    page_title="Airgap Gemma – Prototype 1",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ Airgap Gemma – Prototype 1")
st.caption("Local, offline AI assistant powered by Google Gemma 2 2B (Ollama)")

# Welcome banner
st.info("👋 **Welcome to Prototype 1!** This assistant operates 100% locally and offline. No data leaves your machine.")

# Input area
prompt = st.text_area(
    "Enter your prompt for prototype 1:",
    height=140,
    placeholder="e.g. Explain how air-gapped offline AI protects sensitive user data."
)

col1, col2 = st.columns([1, 4])
with col1:
    submit_btn = st.button("Run Inference", type="primary")

if submit_btn:
    if not prompt.strip():
        st.warning("Please enter a prompt before running.")
    else:
        with st.spinner("prototype 1 is reasoning locally via Gemma 2 2B..."):
            response = query_gemma(prompt)
            if response.startswith("ERROR_"):
                st.error(f"Inference issue: {response}")
            else:
                st.success("**Response from prototype 1:**")
                st.markdown(response)
