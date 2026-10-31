# Airgap Gemma

> 100% Local, Offline Conversational AI with Google Gemma 2 2B.

Built for **Hacktoberfest 2026 Hack Day – Track 8: Build Anything with Gemma**.

---

## 🎯 Project Overview

**Airgap Gemma** is a private, air-gapped conversational AI assistant. It requires **zero cloud API keys, zero external internet connectivity, and zero third-party telemetry**. All prompt processing and inference execute completely on-device via local Ollama.

---

## 🚀 Key Features

- **Conversational Chat Interface**: Multi-turn dialogue with memory retained in session state.
- **Natural Enter-Key Submission**: Instant prompt submission using `st.chat_input` (press Enter to send).
- **Real-Time Token Streaming**: Low-latency token-by-token generation with local Gemma 2 2B.
- **Zero-Cloud Guarantee**: Complies strictly with the hackathon zero-external-AI policy.
- **Telemetry Sidebar**: Real-time system status, local hardware verification, and one-click chat reset.
- **Modern Obsidian & Cyan Theme**: Curated dark theme configured via `.streamlit/config.toml`.

---

## 🛠️ Getting Started

### 1. Prerequisites
Ensure Ollama is installed and running with `gemma2:2b`:
```bash
ollama run gemma2:2b
```

### 2. Local Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Testing & Linting (Rule 3 Compliance)

Run all local verifications before committing:
```bash
# Run full unit test suite
pytest -q

# Run Ruff linter
ruff check .
```

---

## 👥 Team
- **Team**: Solo-Leveling
- **Member**: Geetesh Jaiswal ([@geetesh-learner](https://github.com/geetesh-learner))
- **Track**: Problem 8 – Build Anything with Gemma (Local AI Innovation Challenge)
