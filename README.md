<div align="center">

# 🏟️ Stadium Coordinator

**Enterprise-grade operational coordination platform for live stadium events**

*One Situation. Multiple Perspectives. One Coordinated Response.*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.22+-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat)](LICENSE)
[![CI](https://github.com/sahithirithvika/stadium-coordinator/actions/workflows/ci.yml/badge.svg)](https://github.com/sahithirithvika/stadium-coordinator/actions)

[🚀 Live Demo](https://stadium-coordinator-eziakajsjq4prgkzhmtwy8.streamlit.app/) · [📋 Report Bug](https://github.com/sahithirithvika/stadium-coordinator/issues) · [✨ Request Feature](https://github.com/sahithirithvika/stadium-coordinator/issues)

</div>

---

## 🎯 Problem Statement

Stadium events involve **7+ stakeholder groups** (Organizers, Security, Medical, Volunteers, Vendors, Transport, Fans) operating in silos. When an incident occurs — a crowd surge, medical emergency, or transport failure — each team reacts independently. There is **no single coordinated response**.

Current monitoring systems show dashboards. They don't coordinate decisions.

---

## 💡 Solution

Stadium Coordinator provides a **prompt-first coordination platform** that:

1. **Aggregates** all operational data from 10 real-time data streams into one context
2. **Surfaces** role-filtered dashboards for every stakeholder group
3. **Simulates** adverse scenarios with immediate operational impact analysis
4. **Generates** a single AI-powered coordinated action plan via one Gemini API call (future release)

The architecture is designed so adding AI requires changing **exactly one function**.

---

## ✨ Features

| Module | Description |
|--------|-------------|
| 🎛️ **Mission Control** | 6-tab live dashboard: Crowd, Gates, Transport, Parking, Weather, Security |
| 👥 **Stakeholder Coordinator** | Role-filtered views for Security, Medical, Operations, Logistics |
| 🔬 **Scenario Simulator** | Interactive what-if simulations: Crowd Surge, Transport Failure, Weather Emergency |
| 📊 **Executive Reports** | Risk assessment, incident summary, stakeholder KPIs, AI recommendations |
| 🤖 **AI Integration Point** | Single `get_ai_recommendations()` function — drop-in Gemini replacement |

---

## 🤖 AI Features

- **Prompt-First Architecture**: All 10 data streams aggregated into one JSON context via `build_stadium_context()`
- **Single Integration Point**: `get_ai_recommendations(context)` in `utils/ai_integration.py` — replace placeholder with Gemini in one edit
- **Confidence Scores**: Every recommendation displays a confidence percentage
- **Role-Aware Recommendations**: AI output surfaced per stakeholder role
- **Graceful Fallback**: Static recommendations ensure the app works without API keys

---

## 🏗️ Architecture

```
User Request
     │
     ▼
 app.py (Entry Point)
     │
     ├─ Sidebar Navigation (5 pages)
     │
     ├─ utils/data_loader.py ──── 10 CSV/JSON datasets
     │        │
     │        ▼
     ├─ utils/context_builder.py ── build_stadium_context()
     │        │
     │        ▼
     └─ utils/ai_integration.py ── get_ai_recommendations() ← AI INTEGRATION POINT
              │
              ▼
         components/ (9 reusable UI components)
              │
              ▼
         pages/ (5 page modules)
```

---

## 🗂️ Folder Structure

```
stadium-coordinator/
├── app.py                        # Entry point: routing + CSS loader
├── requirements.txt              # Pinned dependencies
├── pyproject.toml               # Project metadata + test config
├── .env.example                 # Environment variable template
├── pages/
│   ├── home.py                  # Landing page
│   ├── mission_control.py       # Live dashboard
│   ├── stakeholder_coordinator.py
│   ├── scenario_simulator.py
│   └── executive_reports.py
├── components/
│   ├── metric_card.py           # KPI card
│   ├── status_badge.py          # Colored status pill
│   ├── alert_card.py            # Severity-coded alert
│   ├── timeline_card.py         # Timeline entry
│   ├── recommendation_card.py   # AI recommendation panel
│   ├── role_selector.py         # Role switcher
│   ├── navigation_card.py       # Page navigation card
│   ├── report_card.py           # Report section card
│   └── chart_container.py       # Plotly chart wrapper
├── utils/
│   ├── data_loader.py           # Dataset loading with graceful errors
│   ├── context_builder.py       # Aggregates all data → JSON context
│   ├── ai_integration.py        # AI INTEGRATION POINT
│   └── chart_theme.py           # Plotly theme constants
├── data/                        # 10 sample datasets (CSV + JSON)
├── styles/
│   └── main.css                 # Glassmorphism dark theme
├── tests/                       # pytest test suite (59 tests)
├── .github/workflows/ci.yml     # GitHub Actions CI
└── docs/                        # Architecture diagrams
```

---

## 🚀 Quick Start

### Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/sahithirithvika/stadium-coordinator.git
cd stadium-coordinator

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your values (optional for base app)

# 5. Run the application
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🌐 Live Demo

**[→ Open Live App](https://stadium-coordinator-eziakajsjq4prgkzhmtwy8.streamlit.app/)**

---

## 🧰 Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11+ | Core language |
| Streamlit | 1.35+ | Web framework |
| Plotly | 5.22+ | Interactive charts |
| Pandas | 2.2+ | Data manipulation |
| Hypothesis | 6.100+ | Property-based testing |
| pytest | Latest | Test runner |
| GitHub Actions | — | CI/CD |

---

## 🔒 Environment Variables

See `.env.example` for all available variables.

```bash
GEMINI_API_KEY=your_key_here    # Future AI integration
STREAMLIT_ENV=development        # Environment mode
LOG_LEVEL=INFO                   # Logging verbosity
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=utils --cov=components --cov-report=term-missing

# Run a specific test file
pytest tests/test_data_loader.py -v
```

Current test suite: **59 tests** across 6 modules.

---

## 🔮 Future Scope

- [ ] **Google Gemini 2.5 Flash** — Replace `get_ai_recommendations()` with live AI coordination
- [ ] **Real-time data** — WebSocket integration with live stadium sensors
- [ ] **Multi-event support** — Manage multiple concurrent events
- [ ] **Mobile PWA** — Progressive Web App for field staff
- [ ] **Export to PDF/Excel** — Full report export
- [ ] **Multi-language** — i18n support for international events
- [ ] **Role-based access control** — Per-stakeholder authentication

---

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a PR.

---

## 🛡️ Security

See [SECURITY.md](SECURITY.md) for our vulnerability reporting policy.

---

## 📄 License

Licensed under the [Apache License 2.0](LICENSE).

---

## 👥 Team

Built with ❤️ for Hack2Skill Build with AI Hackathon.

</div>
