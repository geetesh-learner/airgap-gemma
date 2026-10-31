# Airgap Gemma (Prototype 1)

> 100% Local, Offline AI Innovation with Google Gemma 2 2B.

Built for **Hacktoberfest 2026 Hack Day – Track 8: Build Anything with Gemma**.

---

## 🎯 Project Overview

**Airgap Gemma** demonstrates a truly local, air-gapped generative AI assistant. It requires **zero cloud API keys, zero external internet connectivity, and zero third-party telemetry**. All prompt processing and inference execute completely on-device via local Ollama.

---

## 🚀 Features (Prototype 1)

- **AI Name**: `prototype 1`
- **Core Engine**: Google Gemma 2 2B (`gemma2:2b`) running via local Ollama (`http://localhost:11434`)
- **Zero-Cloud Guarantee**: Complies strictly with the hackathon zero-external-AI policy
- **Defensive Error Handling**: Graceful fallback and connection status checks
- **Interactive UI**: Streamlit interface designed for local experimentation

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

### 3. Run Prototype 1
```bash
streamlit run app.py
```

---

## 🧪 Testing & CI

Run linting and tests locally before committing:
```bash
ruff check .
pytest -q
```

---

## 👥 Team
- **Team**: Solo-Leveling
- **Member**: Geetesh Jaiswal ([@geetesh-learner](https://github.com/geetesh-learner))
- **Track**: Problem 8 – Build Anything with Gemma (Local AI Innovation Challenge)
