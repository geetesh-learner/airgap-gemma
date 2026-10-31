# Changelog

All notable changes to the Airgap-Gemma project are documented in this file.
Date format strictly adheres to `DD-MM-YYYY`.

## [01-11-2026] - v0.2.0 (Conversational Chat Interface)

### Added
- `feat(ui)`: Interactive multi-turn chat interface using `st.chat_message` and `st.chat_input`.
- `feat(ui)`: Automatic prompt submission on pressing the `Enter` key.
- `feat(inference)`: Real-time token streaming client via `stream_gemma` and `st.write_stream`.
- `feat(theme)`: Obsidian and neon cyan dark theme in `.streamlit/config.toml`.
- `feat(telemetry)`: Sidebar telemetry panel with real-time connectivity status and conversation reset.
- `feat(testing)`: Mock unit tests covering edge cases and offline fallback handling in `tests/test_placeholder.py`.
- `docs(pr)`: Pull request template in `.github/pull_request_template.md`.

## [01-11-2026] - v0.1.0 (Initial Prototype Scaffold)

### Added
- Initial Streamlit MVP scaffold with local Ollama integration.
- Unit testing framework and GitHub Actions CI pipeline.
- Hackathon track metadata and documentation.
