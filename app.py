import streamlit as st
from datetime import datetime

# Import the streaming helper that talks to the local Gemma model
from hackathon_toolkit.ollama_client import stream_gemma

# ----------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Airgap Gemma – Interactive UI",
    page_icon="🛡️",
    layout="wide",
)

# ----------------------------------------------------------------------
# Custom micro‑styling (makes the chat look premium)
# ----------------------------------------------------------------------
st.html("""
<style>
    /* Chat bubbles */
    .stChatMessage {
        border-radius: 10px;
        margin-bottom: 0.5rem;
        padding: 0.75rem 1rem;
        background: #0e1117;          /* dark‑mode‑friendly */
        color: #e1e1e0;
    }
    .stChatMessage[data-role=\"assistant\"] {
        background: #1e2a38;
    }
    .stChatMessage[data-role=\"user\"] {
        background: #2b3c4d;
    }
    /* Timestamp tag */
    .msg‑ts {
        font-size: 0.75rem;
        color: #a0a0a0;
        margin-top: 0.25rem;
        text-align: right;
    }
    .airgap‑tag {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(0,210,255,.15);
        color: #00d2ff;
        border: 1px solid rgba(0,210,255,.3);
    }
</style>
""")

# ----------------------------------------------------------------------
# Initialise session state for memory (stores role, content, timestamp)
# ----------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []   # each entry: {"role": ..., "content": ..., "ts": ...}

# ----------------------------------------------------------------------
# Sidebar – telemetry & controls
# ----------------------------------------------------------------------
with st.sidebar:
    st.title("🛡️ Airgap Gemma")
    st.caption("v0.2.0 • Interactive UI")

    st.markdown(
        '<div class="airgap-tag">● 100% AIR‑GAPPED OFFLINE</div>',
        unsafe_allow_html=True,
    )
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
    st.caption("Hacktoberfest 2026 • Problem 8: Gemma Track")
    st.caption("Team Solo‑Leveling • Geetesh Jaiswal")

# ----------------------------------------------------------------------
# Main header
# ----------------------------------------------------------------------
st.title("🛡️ Airgap Gemma – Interactive UI")
st.caption(
    "Real‑time local conversational assistant powered by Google Gemma 2 2B"
)

# ----------------------------------------------------------------------
# Render conversation history (stacked bubbles, each with a timestamp)
# ----------------------------------------------------------------------
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🛡️"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        st.markdown(
            f'<div class="msg‑ts">{msg["ts"]}</div>',
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------------------
# Suggestion chips (shown only when chat is empty)
# ----------------------------------------------------------------------
selected_suggestion = None
if not st.session_state.messages:
    st.info(
        "👋 **Welcome!** Experience a premium, locally‑run AI chat "
        "with timestamps on every turn."
    )
    st.markdown("**Try asking:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "🔒 Why is offline AI essential for data privacy?",
            width="stretch",
        ):
            selected_suggestion = "Why is offline AI essential for data privacy?"
    with col2:
        if st.button(
            "⚡ What makes Gemma 2 2B fast on Apple Silicon?",
            width="stretch",
        ):
            selected_suggestion = "What makes Gemma 2 2B fast on Apple Silicon?"

# ----------------------------------------------------------------------
# Chat input (Enter to submit)
# ----------------------------------------------------------------------
prompt = st.chat_input("Ask anything… (Press Enter to send)")

# Resolve input from text box or a suggestion chip
active_prompt = prompt or selected_suggestion

if active_prompt:
    # ----- USER TURN -------------------------------------------------
    ts_user = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    st.session_state.messages.append(
        {"role": "user", "content": active_prompt, "ts": ts_user}
    )
    with st.chat_message("user", avatar="👤"):
        st.markdown(active_prompt)
        st.markdown(f'<div class="msg‑ts">{ts_user}</div>', unsafe_allow_html=True)

    # ----- ASSISTANT TURN (streaming) -------------------------------
    with st.chat_message("assistant", avatar="🛡️"):
        with st.status(
            ":shimmer[Reasoning locally with Gemma 2 2B…]",
            type="compact",
        ) as status:
            response_gen = stream_gemma(active_prompt)
            # Pull the first chunk to verify the model is responsive
            first_chunk = next(response_gen, "")
            status.update(label="Inference active (Gemma 2 2B)", state="complete")

        def combined_stream():
            if first_chunk:
                yield first_chunk
            yield from response_gen

        full_response = st.write_stream(combined_stream())

    # ----- SAVE ASSISTANT MESSAGE ------------------------------------
    ts_assist = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response, "ts": ts_assist}
    )
    # Render timestamp for the assistant message (already shown by the loop,
    # but we add it here so the latest message appears instantly)
    with st.chat_message("assistant", avatar="🛡️"):
        st.markdown(full_response)
        st.markdown(f'<div class="msg‑ts">{ts_assist}</div>', unsafe_allow_html=True)

