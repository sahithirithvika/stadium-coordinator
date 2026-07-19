# Stadium Coordinator 🏟️

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.22%2B-3F4F75?logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![CI](https://github.com/sahithirithvika/stadium-coordinator/actions/workflows/ci.yml/badge.svg)

> **Enterprise-grade operational coordination platform for live stadium events — real-time situational awareness, role-based dashboards, and AI-powered recommendations in one unified interface.**

---

## Problem Statement

Running a live stadium event involves dozens of independent teams — security, transport, medical, vendors, volunteers — operating in silos with no shared situational picture. Incidents escalate because the right person doesn't have the right data at the right time.

Stadium Coordinator solves this by aggregating all operational data streams into a single, role-aware command interface, surfacing AI-generated recommendations before problems become crises.

---

## Solution Architecture

```
┌─────────────────────────────────────────────────┐
│                  Streamlit Frontend              │
│  Home │ Mission Control │ Stakeholder │ Scenario │ Reports │
└────────────────────────┬────────────────────────┘
                         │
         ┌───────────────▼───────────────┐
         │         Page Layer            │
         │  pages/*.py  (render logic)   │
         └───────────────┬───────────────┘
                         │
    ┌────────────────────▼────────────────────┐
    │              Utils Layer                │
    │  data_loader │ context_builder │ AI     │
    └────────────────────┬────────────────────┘
                         │
    ┌────────────────────▼────────────────────┐
    │              Data Layer                 │
    │  10 × CSV / JSON datasets in data/      │
    └─────────────────────────────────────────┘
```

---

## Features

| Page | Description |
|------|-------------|
| **Home** | Role selector, live metric cards, AI recommendation panel |
| **Mission Control** | Real-time crowd density, gate occupancy, transport status, weather overlay |
| **Stakeholder Coordinator** | Role-filtered views for Security, Medical, Transport, Vendors, Volunteers |
| **Scenario Simulator** | Tabletop stress-testing — simulate crowd surges, gate failures, weather events |
| **Executive Reports** | KPI summaries, incident timelines, exportable event reports |

---

## AI Features

- **AI Recommendation Engine** — `utils/ai_integration.py` is a single integration point. Static placeholder recommendations ship today; swap in Gemini 2.5 Flash by adding `GEMINI_API_KEY` to your environment — the function signature stays the same.
- **Context Builder** — `utils/context_builder.py` serialises all 10 live datasets into a JSON-safe prompt context dict ready to be sent to any LLM.
- **Scenario AI Prompts** — the Scenario Simulator page prepares structured prompts for AI-driven what-if analysis.

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend / App | Streamlit | 1.35+ |
| Visualisation | Plotly | 5.22+ |
| Data Processing | Pandas | 2.2+ |
| Language | Python | 3.11+ |
| CI/CD | GitHub Actions | — |
| Testing | pytest + pytest-cov | — |
| Security Scan | Bandit | — |
| Linting | flake8 | — |

---

## Folder Structure

```
stadium-coordinator/
├── app.py                     # Entry point — routing & session state
├── pages/
│   ├── home.py
│   ├── mission_control.py
│   ├── stakeholder_coordinator.py
│   ├── scenario_simulator.py
│   └── executive_reports.py
├── components/                # Reusable UI widgets
│   ├── metric_card.py
│   ├── alert_card.py
│   ├── status_badge.py
│   ├── timeline_card.py
│   ├── recommendation_card.py
│   ├── role_selector.py
│   ├── navigation_card.py
│   ├── report_card.py
│   └── chart_container.py
├── utils/
│   ├── data_loader.py         # Centralised dataset loading
│   ├── context_builder.py     # JSON-safe AI context serialiser
│   ├── ai_integration.py      # AI integration point (Gemini-ready)
│   └── chart_theme.py         # Plotly dark theme constants
├── data/                      # 10 × CSV / JSON operational datasets
├── styles/
│   └── main.css
├── tests/                     # pytest unit & smoke tests
├── .github/workflows/ci.yml   # CI — test + lint + security scan
├── pyproject.toml
├── requirements.txt
└── .env.example
```

---

## Installation

### Local (recommended)

```bash
# 1. Clone
git clone https://github.com/sahithirithvika/stadium-coordinator.git
cd stadium-coordinator

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY when ready

# 5. Run
streamlit run app.py
```

### Docker

```dockerfile
# Build
docker build -t stadium-coordinator .

# Run
docker run -p 8501:8501 --env-file .env stadium-coordinator
```

> A `Dockerfile` is on the future scope list — contributions welcome!

---

## Environment Variables

Copy `.env.example` to `.env` and fill in values. See `.env.example` for the full list.

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Future | Google Gemini API key for live AI recommendations |
| `STREAMLIT_ENV` | No | `development` or `production` |
| `LOG_LEVEL` | No | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

---

## Live Demo

🌐 **[https://stadium-coordinator-eziakajsjq4prgkzhmtwy8.streamlit.app/](https://stadium-coordinator-eziakajsjq4prgkzhmtwy8.streamlit.app/)**

---

## Screenshots

> _Screenshots coming soon — contributions welcome!_

Place screenshots in `assets/` and reference them here:

```markdown
![Home Page](assets/screenshot_home.png)
![Mission Control](assets/screenshot_mission_control.png)
```

---

## Future Scope

- **Gemini 2.5 Flash AI Integration** — Replace placeholder recommendations with live Gemini API calls. The hook in `utils/ai_integration.py` is already in place; add your key and swap the return statement.
- **Real-time Data Ingestion** — WebSocket feeds from turnstile sensors, parking IoT, and transport APIs.
- **Mobile-responsive layout** — Progressive enhancement for field personnel on tablets.
- **Multi-event support** — Tenant-aware data partitioning for venue operators running concurrent events.
- **Docker Compose deployment** — Containerised stack with a reverse proxy and secrets management.
- **Alert Push Notifications** — Email / SMS / Slack integration for critical threshold breaches.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, commit conventions, and the PR checklist.

---

## Security

See [SECURITY.md](SECURITY.md) for our vulnerability reporting policy and supported versions.

---

## Code of Conduct

This project follows the [Contributor Covenant 2.1](CODE_OF_CONDUCT.md).

---

## License

Distributed under the [Apache 2.0 License](LICENSE).

---

## Team

Built with care for the Hack2Skill AI Hackathon.

| Role | Contributor |
|------|------------|
| Lead Developer | [@sahithirithvika](https://github.com/sahithirithvika) |

---

_Stadium Coordinator — because every second counts when 60 000 fans are in the stands._
