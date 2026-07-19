# Changelog

All notable changes to Stadium Coordinator are documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [1.0.0] — 2024-03-15

### Added
- Home page with live event KPI snapshot and platform navigation
- Mission Control dashboard with 6 tabbed views: Crowd, Gates, Transport, Parking, Weather, Security
- Stakeholder Coordinator with role-filtered views: Security, Medical, Operations, Logistics
- Scenario Simulator with 3 interactive simulations: Crowd Surge, Transport Failure, Weather Emergency
- Executive Reports with risk badge, incident summary, stakeholder summary and AI recommendations
- 9 reusable glassmorphism UI components: MetricCard, StatusBadge, AlertCard, TimelineCard, RecommendationCard, RoleSelector, NavigationCard, ReportCard, ChartContainer
- 10 realistic sample datasets covering all operational domains
- Prompt-first AI integration point via `get_ai_recommendations()` in utils/ai_integration.py
- `build_stadium_context()` aggregating all datasets into one JSON-serializable dict
- CSS glassmorphism dark theme with Inter font and CSS custom properties
- Responsive layout supporting 1024px–2560px viewports
- Streamlit Community Cloud deployment

### Architecture
- Python 3.11+ / Streamlit 1.35+ / Plotly 5.22+ / Pandas 2.2+
- Prompt-first design: single `get_ai_recommendations()` integration point for future Gemini 2.5 Flash
- DataLoadResult pattern: graceful degradation on missing/malformed datasets
