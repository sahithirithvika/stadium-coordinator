# Implementation Plan: Stadium Coordinator

## Overview

Implement the Stadium Coordinator Streamlit application in Python. The build follows a bottom-up order: project scaffold → styling → utilities → sample datasets → reusable component library → page implementations → tests → deployment verification. Each layer depends only on the layer below it, enabling safe incremental integration.

---

## Tasks

- [x] 1. Project Scaffolding
  - [x] 1.1 Create directory structure and entry point
    - Create top-level directories: `pages/`, `components/`, `styles/`, `assets/`, `utils/`, `data/`, `docs/`
    - Create `app.py` with only import statements, sidebar rendering, and page routing; no page logic or component definitions
    - Add a "Page Not Found" fallback branch to the routing logic in `app.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.6_

  - [x] 1.2 Create `requirements.txt` with pinned versions
    - List every required package using exact `==` version notation: `streamlit`, `plotly`, `pandas`, `hypothesis` (for tests), and any other direct dependencies
    - Verify no range-based specifiers (`>=`, `~=`, `^`) are present
    - _Requirements: 1.4, 12.1_

- [x] 2. Styling System
  - [x] 2.1 Create `styles/main.css` with global theme overrides
    - Define CSS custom properties (variables) for all colors, font sizes, border-radii, and shadow values used throughout the app
    - Override Streamlit defaults: page background, sidebar background, main content padding, base font family (`Inter`, `Roboto`, or `DM Sans`), button colors, metric label/value colors
    - Implement the glassmorphism card pattern (backdrop-filter, semi-transparent background, border-radius 8–16px, box-shadow with opacity 0.08–0.30)
    - Ensure layout is correct for viewport widths 1024px–2560px (no horizontal scrollbar)
    - _Requirements: 2.4, 2.5, 2.6, 2.7_

  - [x] 2.2 Create CSS loader in `app.py`
    - Write a helper that reads all `.css` files under `styles/` and injects them via a single `st.markdown` call at the top of `app.py`; no other file may inject CSS
    - _Requirements: 2.5_

- [x] 3. Utility Layer
  - [x] 3.1 Implement `utils/data_loader.py`
    - Define a `DataLoadResult` named tuple or dataclass with fields: `data` (DataFrame or list), `error` (str or None), `dataset_name` (str)
    - Implement `load_dataset(name: str, path: str) -> DataLoadResult` that loads CSV or JSON files using relative paths from the project root
    - Handle missing file (return error with dataset name), malformed data (invalid JSON/CSV syntax), and fewer-than-20-valid-rows conditions — return an error message in each case without raising
    - _Requirements: 9.2, 9.3, 9.5, 9.6, 12.3, 12.5, 12.6_

  - [x] 3.2 Implement `utils/context_builder.py`
    - Implement `build_stadium_context(datasets: dict) -> dict` that aggregates all active dataset values into one dictionary with keys: `crowd_levels`, `gate_occupancy`, `parking`, `metro_status`, `bus_status`, `weather`, `medical_incidents`, `vendor_inventory`, `volunteer_availability`, `security_alerts`
    - Ensure the returned dictionary is JSON-serializable (`json.dumps()` raises no exception); no datetime objects, sets, or custom class instances in the output
    - _Requirements: 11.1, 11.2_

  - [x] 3.3 Implement `utils/ai_integration.py`
    - Implement `get_ai_recommendations(context: dict) -> list[str]` marked with comment `# AI INTEGRATION POINT`
    - Return a list of one or more static placeholder strings; the function signature must not change when Gemini is integrated
    - _Requirements: 11.3, 11.4, 11.5_

  - [x] 3.4 Implement `utils/chart_theme.py`
    - Define a function `get_chart_colors() -> dict` that reads color values from the CSS custom properties declared in `styles/main.css` (or mirrors them as Python constants) so chart construction code never contains hardcoded hex values
    - _Requirements: 10.2, 10.3_

- [ ] 4. Sample Datasets
  - [-] 4.1 Create `data/crowd_levels.csv`
    - 20–500 rows with columns: `timestamp` (ISO 8601), `zone`, `occupancy_pct` (0–100), `capacity`
    - At least 2 valid time-series data points required for chart rendering
    - _Requirements: 9.1, 9.4, 5.9_

  - [-] 4.2 Create `data/gate_occupancy.csv`
    - 20–500 rows with columns: `gate_id`, `timestamp`, `occupancy_pct` (0–100), `status`
    - _Requirements: 9.1, 9.4, 5.9_

  - [-] 4.3 Create `data/parking.csv`
    - 20–500 rows with columns: `lot_id`, `timestamp`, `utilization_pct` (0–100), `available_spaces`
    - _Requirements: 9.1, 9.4, 5.6_

  - [-] 4.4 Create `data/metro_status.json`
    - 20–500 entries with fields: `line`, `timestamp`, `delay_minutes` (0–999), `status`
    - _Requirements: 9.1, 9.4, 5.6_

  - [-] 4.5 Create `data/bus_status.json`
    - 20–500 entries with fields: `route_id`, `timestamp`, `delay_minutes`, `status`
    - _Requirements: 9.1, 9.4_

  - [~] 4.6 Create `data/weather.json`
    - 20–500 entries with fields: `timestamp`, `condition` (string), `temperature_c`, `humidity_pct`, `wind_kph`
    - _Requirements: 9.1, 9.4, 5.4_

  - [~] 4.7 Create `data/medical_incidents.csv`
    - 20–500 rows with columns: `incident_id`, `timestamp`, `title`, `category`, `severity` (Low/Medium/High/Critical), `description`, `status`
    - _Requirements: 9.1, 9.4, 5.5, 5.6, 8.2_

  - [~] 4.8 Create `data/vendor_inventory.csv`
    - 20–500 rows with columns: `vendor_id`, `name`, `category`, `stock_level_pct` (0–100), `timestamp`
    - _Requirements: 9.1, 9.4, 5.6_

  - [~] 4.9 Create `data/volunteer_availability.csv`
    - 20–500 rows with columns: `volunteer_id`, `role`, `zone`, `status`, `coverage_pct` (0–100), `timestamp`
    - _Requirements: 9.1, 9.4, 5.6_

  - [~] 4.10 Create `data/security_alerts.csv`
    - 20–500 rows with columns: `alert_id`, `timestamp`, `title`, `severity` (Low/Medium/High/Critical), `description`, `status`, `role`
    - Include rows of each severity level to support StatusBadge and risk mapping logic
    - _Requirements: 9.1, 9.4, 5.1, 5.2, 8.5_

- [ ] 5. Component Library
  - [~] 5.1 Implement `components/metric_card.py` — `MetricCard`
    - Accept: `label` (str, max 60 chars), `value` (str or number), `unit` (str, max 20 chars), `delta` (str or number, optional)
    - Render a styled KPI card with visually distinct label, value, unit, and optional trend regions using `st.markdown` and the CSS classes defined in `styles/main.css`
    - _Requirements: 3.1, 5.4, 5.6_

  - [~] 5.2 Implement `components/status_badge.py` — `StatusBadge`
    - Accept: `status` (str)
    - Map recognized values to colors: Operational → green, Warning/Degraded → yellow, Critical → red, unrecognized → gray (render literal text, no exception)
    - _Requirements: 3.2, 3.3_

  - [~] 5.3 Implement `components/alert_card.py` — `AlertCard`
    - Accept: `severity` (Low/Medium/High/Critical), `title` (str, max 100 chars), `description` (str, max 300 chars), `timestamp` (ISO 8601)
    - Render a styled alert row with visually differentiated severity levels
    - _Requirements: 3.4_

  - [~] 5.4 Implement `components/timeline_card.py` — `TimelineCard`
    - Accept: `event_title` (str, max 100 chars), `description` (str, max 300 chars), `timestamp` (ISO 8601)
    - Render a timeline entry with a visible vertical connector line and timestamp label
    - _Requirements: 3.5_

  - [~] 5.5 Implement `components/recommendation_card.py` — `RecommendationCard`
    - Accept: `title` (str, max 100 chars), `body` (str, max 500 chars), `confidence` (number 0–100)
    - Render a recommendation panel with a visible "AI Placeholder" label and confidence score displayed as a percentage
    - Body text must always be sourced from `get_ai_recommendations`; do not hardcode body in this file
    - _Requirements: 3.6, 11.4_

  - [~] 5.6 Implement `components/role_selector.py` — `RoleSelector`
    - Accept: `roles` (list of str), `selected_role` (str)
    - Render a tab or segmented button group; the active role is visually highlighted differently from inactive roles
    - _Requirements: 3.7, 6.1_

  - [~] 5.7 Implement `components/navigation_card.py` — `NavigationCard`
    - Accept: `page_name` (str, max 60 chars), `description` (str, max 120 chars), `icon`
    - Render a styled card that triggers navigation to the named page when activated
    - _Requirements: 3.8_

  - [~] 5.8 Implement `components/report_card.py` — `ReportCard`
    - Accept: `section_title` (str, max 80 chars), `body` (str or rendered HTML)
    - Render with a visually distinct title region and body region
    - _Requirements: 3.9_

  - [~] 5.9 Implement `components/chart_container.py` — `ChartContainer`
    - Accept: `fig` (Plotly figure or None), `title` (str, max 80 chars)
    - Render chart inside a styled card with the title visible above; when `fig` is None render "No data available" — no exception
    - Enforce minimum height 200px, minimum width 300px; enable hover tooltips on all rendered charts
    - _Requirements: 3.10, 10.1, 10.6_

  - [~] 5.10 Checkpoint — component library complete
    - Verify each component module imports no other component module (import isolation)
    - Ensure all tests pass, ask the user if questions arise.
    - _Requirements: 3.11_

- [ ] 6. Pages
  - [~] 6.1 Implement `pages/home.py` — Home page
    - Render hero banner with exact tagline: "Coordinating Every Decision. Empowering Every Stakeholder."
    - Render a 4-card grid using `NavigationCard` (Mission Control, Stakeholder Coordinator, Scenario Simulator, Executive Reports); each description ≤ 100 chars
    - Render architecture overview section with labeled elements for all 7 stakeholder roles and a "Coordination Layer" connector
    - Render "Launch Mission Control" button that navigates to Mission Control
    - Render "Recent Event Snapshot" section sourced from datasets (attendance, active alerts count, weather); show fallback message if any dataset is unavailable
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [~] 6.2 Implement `pages/mission_control.py` — Mission Control page
    - Render "Overall Stadium Health" `StatusBadge` (Operational/Degraded/Critical) derived from `security_alerts` dataset
    - Render "Active Alerts" section using `AlertCard`; show "No active alerts" when zero records
    - Render "Current Event Status" panel (event name, phase from {"Pre-Match","Live","Half-Time","Post-Match"}, elapsed time HH:MM:SS)
    - Render `MetricCard` for: Crowd Density, Weather Condition, Transport Status, Emergency Status; show "Data Unavailable" when source missing
    - Render "Incident Timeline" (`TimelineCard`) combined from `medical_incidents` + `security_alerts`, sorted timestamp descending
    - Render 6 KPI `MetricCard` instances: Gate Occupancy %, Parking Utilization %, Metro Delay Minutes, Active Medical Cases, Vendor Stock Level %, Volunteer Coverage %
    - Render AI Recommendation placeholder (`RecommendationCard`) sourced from `get_ai_recommendations`; render even when confidence is 0.0
    - Render "Recent Operational Updates" feed (5 most recent entries; fewer is fine)
    - Render crowd density line/area chart and gate occupancy bar/pie chart using `ChartContainer`; apply "Insufficient data" message when fewer than 2 time-series points
    - _Requirements: 5.1–5.9, 10.1, 10.4, 10.5, 10.6_

  - [~] 6.3 Implement `pages/stakeholder_coordinator.py` — Stakeholder Coordinator page
    - Render `RoleSelector` with exactly 7 roles in order: Organizer, Security, Medical, Volunteer, Vendor, Transport, Fan; default to Organizer
    - On role selection, update all content sections (KPIs, tasks, notifications, recommendations) within one re-run cycle
    - Render ≥ 3 role-specific `MetricCard` instances per role sourced from relevant datasets
    - Render role-specific task list with ≥ 3 items (title max 80 chars, status indicator) per role
    - Render role-specific `AlertCard` notifications filtered by role; show "No active notifications" when empty
    - Render role-specific `RecommendationCard` sourced from `get_ai_recommendations` with role name referenced in context
    - _Requirements: 6.1–6.7_

  - [~] 6.4 Implement `pages/scenario_simulator.py` — Scenario Simulator page
    - Render scenario selection control listing exactly 6 scenarios: Heavy Rain, Gate Congestion, Medical Emergency, VIP Arrival, Power Failure, Extra Time
    - Render 1–5 scenario-specific context cards (title max 80 chars, description max 300 chars) from datasets on selection
    - Render 1–5 AI analysis placeholder `RecommendationCard` instances per scenario (body max 300 chars, confidence int 0–100) sourced from `get_ai_recommendations`
    - Render 1–10 affected-stakeholder panels with 1–5 placeholder action items each
    - Render exactly one Plotly chart via `ChartContainer`: line for Heavy Rain/Extra Time, bar for the other four scenarios
    - Show instructional prompt "Select a scenario above to begin simulation" on first load (no scenario selected)
    - No real AI logic, external API calls, or dynamic decision text
    - _Requirements: 7.1–7.7_

  - [~] 6.5 Implement `pages/executive_reports.py` — Executive Reports page
    - Render "Operational Summary" `ReportCard` (total events, total personnel deployed, total incidents from datasets)
    - Render "Incident Summary" `ReportCard` listing each incident (title, category, severity) from `medical_incidents` + `security_alerts`
    - Render "Recommended Actions" section with ≥ 1 `RecommendationCard` placeholder (description ≤ 200 chars) sourced from `get_ai_recommendations`
    - Render "Stakeholder Summary" `ReportCard` with one row per role (role name + total activity count from datasets)
    - Render "Risk Level" `StatusBadge` derived from `security_alerts`: all Low → Operational; any Medium and no High/Critical → Warning; any High or Critical → Critical
    - Render "Export Report" button that shows "Coming Soon" message without triggering any export, download, or navigation
    - _Requirements: 8.1–8.6_

  - [~] 6.6 Checkpoint — all pages wired
    - Register all 5 pages in `app.py` sidebar navigation in order: Home, Mission Control, Stakeholder Coordinator, Scenario Simulator, Executive Reports
    - Verify page switching preserves session state variables
    - Verify "Page Not Found" fallback renders for an unknown page name
    - Ensure all tests pass, ask the user if questions arise.
    - _Requirements: 2.1, 2.2, 2.3, 1.6_

- [ ] 7. Property-Based Tests (Hypothesis)
  - [~] 7.1 Write property test for StatusBadge color mapping
    - **Property 1: Unrecognized status strings always render gray without exception**
    - Use `hypothesis.strategies.text()` filtered to exclude the 5 recognized status strings
    - Verify the badge renders a gray-class element and never raises
    - **Validates: Requirements 3.2, 3.3**

  - [ ]* 7.2 Write property test for DataLoadResult error propagation
    - **Property 2: Any dataset with fewer than 20 valid rows always produces a non-None error and never raises an unhandled exception**
    - Generate synthetic CSVs with 0–19 rows using Hypothesis
    - Assert `DataLoadResult.error` is not None and `DataLoadResult.data` is empty or None
    - **Validates: Requirements 9.3, 9.6**

  - [ ]* 7.3 Write property test for build_stadium_context JSON-serializability
    - **Property 3: The output of `build_stadium_context` is always JSON-serializable for any valid dataset input**
    - Use Hypothesis to generate varied dataset dicts (with string/int/float values, empty lists, None values)
    - Assert `json.dumps(result)` raises no exception
    - **Validates: Requirements 11.1, 11.2**

  - [ ]* 7.4 Write property test for MetricCard input tolerance
    - **Property 4: MetricCard renders without exception for any label ≤ 60 chars, any numeric or string value, and any unit ≤ 20 chars**
    - Use `st.testing` or render-to-string approach with Hypothesis-generated inputs
    - Assert no exception is raised for all valid input combinations
    - **Validates: Requirements 3.1**

  - [ ]* 7.5 Write property test for AlertCard severity rendering
    - **Property 5: AlertCard always renders a visually differentiated element for any severity in {Low, Medium, High, Critical} and any valid title/description/timestamp combination**
    - Use Hypothesis `sampled_from` for severity, `text` strategies for other fields
    - Assert output HTML/markdown contains a severity-specific CSS class
    - **Validates: Requirements 3.4**

  - [ ]* 7.6 Write property test for risk level derivation (Executive Reports)
    - **Property 6: Risk level mapping is monotone — a dataset whose maximum severity is S always maps to the same or higher risk level as any dataset whose maximum severity is ≤ S**
    - Generate random `security_alerts` datasets with varying severity distributions
    - Assert mapping (all Low → Operational; any Medium, no High/Critical → Warning; any High or Critical → Critical) is consistent
    - **Validates: Requirements 8.5**

  - [ ]* 7.7 Write property test for get_ai_recommendations return contract
    - **Property 7: `get_ai_recommendations` always returns a non-empty list of strings for any valid stadium context dictionary**
    - Use Hypothesis to generate arbitrary context dicts with string keys and JSON-serializable values
    - Assert `isinstance(result, list)`, `len(result) >= 1`, and all elements are `str`
    - **Validates: Requirements 11.3, 11.4**

- [ ] 8. Integration Tests
  - [~] 8.1 Write startup integration tests
    - Test that `streamlit run app.py` equivalent (import + module load) succeeds when all 10 dataset files are present
    - Test that startup succeeds and renders inline error messages (not an exception) when one or more dataset files are missing
    - _Requirements: 12.4, 12.6, 9.3_

  - [ ]* 8.2 Write page-render integration tests
    - Test that all 5 pages (Home, Mission Control, Stakeholder Coordinator, Scenario Simulator, Executive Reports) render without raising exceptions using `streamlit.testing.v1.AppTest` or equivalent
    - Assert each page contains at least one expected element (e.g., the hero tagline on Home, the StatusBadge on Mission Control)
    - _Requirements: 4.1, 5.1, 6.1, 7.1, 8.1_

  - [ ]* 8.3 Write session state preservation test
    - Navigate programmatically between pages twice and assert that session state variables set before switching are still present after switching
    - _Requirements: 2.2_

- [ ] 9. Deployment Verification
  - [~] 9.1 Verify `requirements.txt` completeness
    - Import every module used in `app.py`, all pages, all components, and all utils; confirm each top-level package appears in `requirements.txt` with an exact `==` version
    - Flag any range-based specifier or missing entry
    - _Requirements: 1.4, 12.1_

  - [~] 9.2 Audit all file paths for absolute-path violations
    - Grep all Python files for patterns: `/home/`, `/Users/`, `C:\`, `~/`, `os.path.abspath` with non-relative base
    - Ensure every data, asset, and CSS path uses `pathlib.Path(__file__).parent` or project-root-relative construction
    - _Requirements: 12.3, 12.5_

  - [ ]* 9.3 Smoke test — `streamlit run app.py`
    - Run `streamlit run app.py --server.headless true` and assert process reaches ready state within 30 seconds without error output
    - _Requirements: 12.4_

- [~] 10. Final Checkpoint
  - Ensure all non-optional tests pass and all pages render without unhandled exceptions.
  - Confirm sidebar lists all 5 pages in the correct order.
  - Ask the user if questions arise before closing out.

---

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP delivery.
- All tasks reference specific requirements for traceability.
- Dataset files (tasks 4.x) can be created in parallel with each other.
- Component files (tasks 5.x) can be created in parallel with each other once the styling system (task 2.1) is complete.
- Pages (tasks 6.x) depend on the full component library and all datasets.
- Property tests (tasks 7.x) depend on the utilities they test.
- Integration tests (tasks 8.x) depend on all pages being complete.
- No component module may import from another component module (import isolation — requirement 3.11).
- All `RecommendationCard` body text must come from `get_ai_recommendations`; never hardcoded in page or component files.
- No hardcoded hex colors in chart construction code — use `get_chart_colors()` exclusively.

---

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["2.1"] },
    { "id": 2, "tasks": ["2.2", "3.1", "3.2", "3.3", "3.4"] },
    { "id": 3, "tasks": ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "4.8", "4.9", "4.10"] },
    { "id": 4, "tasks": ["5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9"] },
    { "id": 5, "tasks": ["6.1", "6.2", "6.3", "6.4", "6.5"] },
    { "id": 6, "tasks": ["6.6", "7.1", "7.2", "7.3", "7.4", "7.5", "7.6", "7.7", "8.1"] },
    { "id": 7, "tasks": ["8.2", "8.3", "9.1", "9.2"] },
    { "id": 8, "tasks": ["9.3"] }
  ]
}
```
