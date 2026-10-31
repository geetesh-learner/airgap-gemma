import streamlit as st

from hackathon_toolkit.ollama_client import stream_gemma

st.set_page_config(
    page_title="Airgap Gemma – Prototype 2",
    page_icon="🛡️",
    layout="wide",
)

# Custom micro-styling for chat refinement
st.html("""
<style>
    /* Sleek container styling */
    .stChatMessage {
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    /* Status tag */
    .airgap-tag {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(0, 210, 255, 0.15);
        color: #00d2ff;
        border: 1px solid rgba(0, 210, 255, 0.3);
    }
</style>
""")

# Initialize session state for conversational memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar Controls & Telemetry
with st.sidebar:
    st.title("🛡️ Airgap Gemma")
    st.caption("v0.2.0 • Prototype 2 (Chat Model)")

    st.markdown('<div class="airgap-tag">● 100% AIR-GAPPED OFFLINE</div>', unsafe_allow_html=True)
    st.write("")

    with st.container(border=True):
        st.subheader("System Telemetry")
        st.text("Model:    gemma2:2b")
        st.text("Backend:  Ollama (localhost:11434)")
        st.text("Cloud:    DISABLED (Zero API calls)")
        st.text("Host:     Apple Silicon (Metal)")

    if st.button("Clear Conversation", icon=":material/delete:", width="stretch"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Hacktoberfest 2026 • Problem 8: Gemma Track")
    st.caption("Team Solo-Leveling • Geetesh Jaiswal")

# Main Header
st.title("🛡️ Airgap Gemma – Prototype 2")
st.caption("Real-time local conversational assistant powered by Google Gemma 2 2B")

# Display conversation history
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🛡️"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Suggestion chips when conversation is fresh
selected_suggestion = None
if not st.session_state.messages:
    st.info("👋 **Welcome to Prototype 2!** Experience conversational AI running entirely on your local machine.")
    st.markdown("**Try asking:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔒 Why is offline AI essential for data privacy?", width="stretch"):
            selected_suggestion = "Why is offline AI essential for data privacy?"
    with col2:
        if st.button("⚡ What makes Gemma 2 2B fast on Apple Silicon?", width="stretch"):
            selected_suggestion = "What makes Gemma 2 2B fast on Apple Silicon?"

# Chat Input (pressing Enter triggers automatic submission)
prompt = st.chat_input("Ask prototype 2 anything... (Press Enter to send)")

# Resolve input from either chat_input or suggestion button
active_prompt = prompt or selected_suggestion

if active_prompt:
    # Append and render user message
    st.session_state.messages.append({"role": "user", "content": active_prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(active_prompt)

    # Stream assistant response
    with st.chat_message("assistant", avatar="🛡️"):
        with st.status(":shimmer[Reasoning locally with Gemma 2 2B...]", type="compact") as status:
            response_generator = stream_gemma(active_prompt)
            # Advance once to confirm connection before closing status
            first_chunk = next(response_generator, "")
            status.update(label="Inference active (Gemma 2 2B)", state="complete")

        def combined_stream():
            if first_chunk:
                yield first_chunk
            yield from response_generator

        full_response = st.write_stream(combined_stream())

    # Save to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
