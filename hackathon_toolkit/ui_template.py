# Minimal Modular Streamlit Interface Boilerplate
# DBC Compliance: DBC-006

import streamlit as st
from ollama_client import query_gemma

st.set_page_config(page_title="Hackathon MVP", layout="wide")

st.title("🚀 Project Name (Replace with Problem Title)")
st.caption("Powered by Google Gemma 2 & Ollama (100% Local Inference)")

# Initialize persistent session state
if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input & Parameters")
    user_input = st.text_area("Enter problem input / data:", height=200)
    trigger = st.button("Run Analysis", type="primary")

with col2:
    st.subheader("AI Analysis / Structured Output")
    if trigger:
        if not user_input.strip():
            st.warning("Please provide input data before running.")
        else:
            with st.spinner("Processing locally on Apple M5..."):
                response = query_gemma(user_input)
                st.session_state.history.append({"input": user_input, "output": response})
                st.success("Execution Completed")
                st.write(response)
