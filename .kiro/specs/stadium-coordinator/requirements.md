# Requirements Document

## Introduction

Stadium Coordinator is an enterprise-grade operational coordination platform for live stadium events. The platform enables organizers, security teams, medical teams, volunteers, vendors, transport teams, and fans to coordinate actions in real time during live events hosted by organizations such as FIFA, IPL, and the Olympic Games Committee. The system is designed as a prompt-first architecture, avoiding hardcoded decision logic, so that a future AI layer (Google Gemini 2.5 Flash) can analyze the entire stadium situation and generate one coordinated operational plan through a single prompt. This release delivers the application shell: premium UI, navigation, reusable components, realistic placeholder data, and all pages — without actual AI integration.

---

## Glossary

- **Application**: The Stadium Coordinator Streamlit web application.
- **Dashboard**: The Mission Control page that surfaces aggregated stadium health metrics.
- **Stakeholder**: Any role that interacts with the platform — Organizer, Security, Medical, Volunteer, Vendor, Transport, or Fan.
- **Role View**: The dynamically rendered set of widgets (KPIs, tasks, notifications, recommendations) shown when a Stakeholder selects their role in the Stakeholder Coordinator page.
- **Scenario**: A predefined simulated event condition (e.g., Heavy Rain, Gate Congestion, Medical Emergency) used in the Scenario Simulator.
- **AI Placeholder**: A UI element that reserves space for a future Gemini-powered recommendation without containing real AI logic.
- **KPI Card**: A reusable MetricCard component that displays a single key performance indicator with a label, value, and optional trend indicator.
- **Alert**: A time-stamped operational notification indicating an event condition that requires stakeholder attention.
- **Incident**: A recorded operational event (e.g., medical case, security breach) that appears in the Incident Timeline.
- **Executive Report**: A structured summary document covering operational, incident, and stakeholder data for leadership review.
- **Component**: A reusable Python function or Streamlit component that renders a standardized UI element.
- **Sample Dataset**: A realistic, statically defined CSV or JSON file used to populate the UI with representative data.
- **Sidebar**: The Streamlit sidebar used for primary navigation between pages.
- **Page**: A distinct view within the Application, implemented as a separate file under the `pages/` directory.
- **Streamlit Community Cloud**: The target deployment environment for the Application.

---

## Requirements

### Requirement 1: Application Shell and Project Structure

**User Story:** As an organizer, I want the application to be organized into a maintainable, deployment-ready project structure, so that the team can extend it without refactoring the entire codebase.

#### Acceptance Criteria

1. THE Application SHALL organize source code into the following top-level directories: `pages/`, `components/`, `styles/`, `assets/`, `utils/`, `data/`, `docs/`.
2. WHEN the Application starts, THE Application SHALL execute `app.py` as the sole entry point; `app.py` SHALL contain only import statements, sidebar rendering calls, and routing calls — no page-rendering logic or component definitions SHALL reside in `app.py`.
3. THE Application SHALL limit `app.py` to imports, sidebar navigation rendering, and page routing; all page logic and component definitions SHALL reside in files under `pages/` or `components/`.
4. THE Application SHALL include a `requirements.txt` file at the project root that lists every Python package dependency using exact `==` version notation (e.g., `streamlit==1.35.0`); range-based specifiers (`>=`, `~=`, `^`) SHALL NOT be used.
5. THE Application SHALL be deployable to Streamlit Community Cloud without any manual environment configuration beyond providing `requirements.txt`; deployment failures caused by invalid code or missing files are outside the scope of this requirement.
6. WHEN the Application receives a navigation request for an unknown page name, THE Application SHALL render a "Page Not Found" message in the main content area rather than raising an unhandled exception.

---

### Requirement 2: Global Navigation and Theming

**User Story:** As a stakeholder, I want a consistently styled sidebar navigation, so that I can move between pages without losing context.

#### Acceptance Criteria

1. THE Application SHALL render a sidebar that lists all five pages in this order: Home, Mission Control, Stakeholder Coordinator, Scenario Simulator, Executive Reports; each page SHALL be represented as a selectable navigation item.
2. WHEN a user selects a page from the sidebar, THE Application SHALL display that page's content within 500 milliseconds, preserving all existing session state variables set before the page switch.
3. WHEN the Application first loads, THE Application SHALL display the Home page content by default before any explicit sidebar selection occurs.
4. THE Application SHALL apply a custom CSS theme that explicitly overrides the following default Streamlit styles: page background color, sidebar background color, default padding on main content, base font family, default button background and text colors, and default metric label and value colors.
5. THE Application SHALL load all custom CSS from one or more dedicated `.css` files under the `styles/` directory; no CSS SHALL be injected via `st.markdown` calls or inline style strings in page or component files.
6. THE Application SHALL use Inter, Roboto, or DM Sans as the primary font family; all card components SHALL use a border-radius between 8px and 16px; all card shadow styles SHALL use a box-shadow with opacity between 0.08 and 0.30.
7. THE Application SHALL render correctly on viewport widths from 1024px to 2560px such that no horizontal scrollbar appears and both the sidebar and main content area remain fully visible and unclipped.

---

### Requirement 3: Reusable UI Component Library

**User Story:** As a developer, I want a library of reusable UI components, so that every page uses consistent visual elements without duplicating markup.

#### Acceptance Criteria

1. THE Application SHALL implement a `MetricCard` component that accepts a label (string, max 60 chars), value (string or number), unit (string, max 20 chars), and optional delta/trend (string or number), and renders a styled KPI card with visually distinct label, value, and optional trend regions.
2. THE Application SHALL implement a `StatusBadge` component that accepts a status string from the set {"Operational", "Warning", "Critical", "Degraded", "Unknown"} and renders a color-coded badge; green for Operational, yellow for Warning or Degraded, red for Critical, and gray for any unrecognized status.
3. WHEN the `StatusBadge` receives a status string not in the recognized set, THE Application SHALL render a gray badge with the literal status text rather than raising an exception.
4. THE Application SHALL implement an `AlertCard` component that accepts a severity level from {"Low", "Medium", "High", "Critical"}, a title (string, max 100 chars), a description (string, max 300 chars), and a timestamp in ISO 8601 format, and renders a styled alert row with visually differentiated severity levels.
5. THE Application SHALL implement a `TimelineCard` component that accepts an event title (string, max 100 chars), a description (string, max 300 chars), and a timestamp in ISO 8601 format, and renders a timeline entry with a visible vertical connector line and a timestamp label.
6. THE Application SHALL implement a `RecommendationCard` component that accepts a title (string, max 100 chars), body text (string, max 500 chars), and a confidence score placeholder (number in range 0–100), and renders a recommendation panel with a visible "AI Placeholder" label and the confidence score displayed as a percentage.
7. THE Application SHALL implement a `RoleSelector` component that accepts a list of role name strings and a currently selected role string, and renders a tab or segmented button group where the active role is visually highlighted differently from inactive roles.
8. THE Application SHALL implement a `NavigationCard` component that accepts a page name (string, max 60 chars), a description (string, max 120 chars), and an icon, renders a styled card, and triggers navigation to the named page when the card is activated.
9. THE Application SHALL implement a `ReportCard` component that accepts a section title (string, max 80 chars) and body content (string or rendered HTML), and renders a styled card with a visually distinct title region and body region.
10. THE Application SHALL implement a `ChartContainer` component that accepts a Plotly figure and a title (string, max 80 chars), renders the chart inside a styled card frame with the title visible above the chart; WHEN a None figure is passed, THE Application SHALL render an "No data available" message inside the card instead of raising an exception.
11. THE Application SHALL define each component in its own module file under the `components/` directory; no component module SHALL import from another component module (import isolation).

---

### Requirement 4: Home Page

**User Story:** As a first-time visitor, I want a visually compelling home page, so that I immediately understand the platform's purpose and can navigate to key features.

#### Acceptance Criteria

1. THE Application SHALL render a hero banner at the top of the Home page containing the exact tagline "Coordinating Every Decision. Empowering Every Stakeholder."
2. THE Application SHALL render a grid of exactly 4 feature cards on the Home page, each using the `NavigationCard` component, with one card per page: Mission Control, Stakeholder Coordinator, Scenario Simulator, and Executive Reports; each card description SHALL NOT exceed 100 characters.
3. THE Application SHALL render an architecture overview section on the Home page that contains labeled visual elements for each of the 7 stakeholder roles (Organizer, Security, Medical, Volunteer, Vendor, Transport, Fan) and a labeled "Coordination Layer" element connecting them.
4. THE Application SHALL render a "Launch Mission Control" button on the Home page that navigates the user to the Mission Control page; the button SHALL always render successfully regardless of any other component's render state on the page.
5. WHEN the Home page loads, THE Application SHALL render a "Recent Event Snapshot" section displaying at minimum the following three metrics sourced from Sample Datasets: current attendance figure, active alerts count, and current weather status.
6. WHEN any Sample Dataset required by the Home page is unavailable, THE Application SHALL render the "Recent Event Snapshot" section with a visible fallback message (e.g., "Data currently unavailable") rather than hiding the section or raising an unhandled exception.

---

### Requirement 5: Mission Control Dashboard

**User Story:** As an organizer, I want a real-time operational dashboard, so that I can monitor all stadium conditions at a glance and identify issues that need coordination.

#### Acceptance Criteria

1. THE Application SHALL render an "Overall Stadium Health" indicator on the Mission Control page using the `StatusBadge` component with one of the following discrete values: "Operational", "Degraded", or "Critical", derived from the Security Alerts sample dataset.
2. THE Application SHALL render an "Active Alerts" section on the Mission Control page using the `AlertCard` component, populated with data from the Security Alerts sample dataset; WHEN the dataset contains zero active alerts, THE Application SHALL render a message indicating no active alerts rather than an empty section.
3. THE Application SHALL render a "Current Event Status" panel on the Mission Control page showing event name (max 100 characters), event phase from the closed set {"Pre-Match", "Live", "Half-Time", "Post-Match"}, and elapsed time in HH:MM:SS format, sourced from Sample Datasets.
4. THE Application SHALL render `MetricCard` components on the Mission Control page for: Crowd Density, Weather Condition, Transport Status, and Emergency Status, each sourced from the corresponding Sample Dataset; WHEN a dataset value is unavailable, the corresponding MetricCard SHALL display "Data Unavailable" as its value.
5. THE Application SHALL render an "Incident Timeline" on the Mission Control page using the `TimelineCard` component, populated with combined data from the Medical Incidents and Security Alerts sample datasets, sorted by timestamp descending.
6. THE Application SHALL render KPI cards on the Mission Control page for exactly the following six metrics using the `MetricCard` component: Gate Occupancy % (range 0–100), Parking Utilization % (range 0–100), Metro Delay Minutes (range 0–999), Active Medical Cases (range 0–9999), Vendor Stock Level % (range 0–100), Volunteer Coverage % (range 0–100); each sourced from the corresponding Sample Dataset.
7. THE Application SHALL render an AI Recommendation placeholder panel on the Mission Control page using the `RecommendationCard` component with placeholder body text and a placeholder confidence score as a numeric value between 0.0 and 1.0 inclusive; the panel SHALL be rendered regardless of whether the confidence score value is 0.0.
8. THE Application SHALL render a "Recent Operational Updates" feed on the Mission Control page showing the five most recent entries from Sample Datasets sorted by timestamp descending; WHEN fewer than five entries exist, THE Application SHALL render all available entries without error.
9. THE Application SHALL render exactly two Plotly charts on the Mission Control page using the `ChartContainer` component: (a) a line or area chart showing crowd density (y-axis, 0–100%) over time (x-axis, labeled timestamps) sourced from the Crowd Levels dataset, and (b) a bar or pie chart showing gate occupancy distribution (y-axis or segment values, 0–100% per gate) sourced from the Gate Occupancy dataset.

---

### Requirement 6: Stakeholder Coordinator

**User Story:** As any stakeholder, I want a role-specific view that shows only the information and tasks relevant to my responsibilities, so that I can act quickly without filtering through irrelevant data.

#### Acceptance Criteria

1. THE Application SHALL render the `RoleSelector` component at the top of the Stakeholder Coordinator page with exactly the following 7 roles in order: Organizer, Security, Medical, Volunteer, Vendor, Transport, Fan.
2. WHEN a user selects a role using the `RoleSelector`, THE Application SHALL update all displayed content sections (KPIs, tasks, notifications, recommendations) to reflect that role's data within one Streamlit re-run cycle; page reloads triggered by other system events during role switching are permitted.
3. THE Application SHALL render at least 3 role-specific KPI cards for each role using the `MetricCard` component, with each card sourced from the Sample Dataset relevant to that role.
4. THE Application SHALL render a role-specific task list for each role showing at least 3 actionable task items, each with a task title (max 80 chars) and status indicator, defined in the Sample Datasets.
5. THE Application SHALL render a role-specific notifications panel for each role using the `AlertCard` component, showing alerts filtered by role relevance from the Sample Datasets; WHEN no alerts exist for a role, THE Application SHALL render a "No active notifications" message.
6. THE Application SHALL render a role-specific AI Recommendation placeholder for each role using the `RecommendationCard` component with placeholder body text that references the selected role by name.
7. WHEN the Stakeholder Coordinator page first loads and no role has been explicitly selected by the user, THE Application SHALL highlight Organizer as the active role in the `RoleSelector` component; the role-specific content sections SHALL update and render upon the user's first interaction with the `RoleSelector`.

---

### Requirement 7: Scenario Simulator

**User Story:** As an organizer, I want to simulate adverse event scenarios, so that I can understand how the coordination system would respond and prepare stakeholders for real incidents.

#### Acceptance Criteria

1. THE Application SHALL render a scenario selection control on the Scenario Simulator page listing exactly the following 6 scenarios: Heavy Rain, Gate Congestion, Medical Emergency, VIP Arrival, Power Failure, Extra Time.
2. WHEN a user selects a scenario, THE Application SHALL render between 1 and 5 scenario-specific context cards describing the simulated conditions, each with a title (max 80 chars) and description (max 300 chars), using data defined in the Sample Datasets.
3. WHEN a user selects a scenario, THE Application SHALL render between 1 and 5 AI analysis placeholder cards using the `RecommendationCard` component, each with scenario-appropriate placeholder body text (max 300 chars) and a placeholder confidence score as an integer in the range 0–100.
4. WHEN a user selects a scenario, THE Application SHALL render between 1 and 10 affected stakeholder panels indicating which roles are impacted, each panel showing 1 to 5 placeholder action items for that role.
5. WHEN a user selects a scenario, THE Application SHALL render exactly one Plotly chart using the `ChartContainer` component illustrating the simulated impact; the chart type SHALL be a line chart for time-series scenarios (Heavy Rain, Extra Time) and a bar chart for distribution scenarios (Gate Congestion, Medical Emergency, VIP Arrival, Power Failure).
6. THE Application SHALL NOT execute any real AI logic, make any external API calls, or produce dynamically generated decision text within the Scenario Simulator.
7. WHEN the Scenario Simulator page first loads and no scenario has been selected, THE Application SHALL render an instructional prompt (e.g., "Select a scenario above to begin simulation") in the main content area rather than an empty page.

---

### Requirement 8: Executive Reports

**User Story:** As an executive, I want a structured report summarizing operational performance, so that I can make informed decisions after the event.

#### Acceptance Criteria

1. THE Application SHALL render an "Operational Summary" section on the Executive Reports page using the `ReportCard` component, displaying at minimum: total events count, total personnel deployed count, and total incidents count, sourced from Sample Datasets.
2. THE Application SHALL render an "Incident Summary" section on the Executive Reports page using the `ReportCard` component, listing each incident from the Medical Incidents and Security Alerts sample datasets with at minimum: incident title, category, and severity per row.
3. THE Application SHALL render a "Recommended Actions" section on the Executive Reports page using the `RecommendationCard` component with at least 1 placeholder action item; each item's description SHALL NOT exceed 200 characters.
4. THE Application SHALL render a "Stakeholder Summary" section on the Executive Reports page using the `ReportCard` component with one row per distinct stakeholder role, each row showing the role name and a total activity count sourced from Sample Datasets.
5. THE Application SHALL render a "Risk Level" indicator on the Executive Reports page using the `StatusBadge` component, derived from the Security Alerts sample dataset using the following mapping: "Operational" if all alerts are Low severity; "Warning" if any alert is Medium severity and none are High or Critical; "Critical" if any alert is High or Critical severity.
6. WHEN a user clicks the "Export Report" button on the Executive Reports page, THE Application SHALL display a "Coming Soon" message to the user and SHALL NOT trigger any export operation, file download, or navigation.

---

### Requirement 9: Sample Datasets

**User Story:** As a developer, I want realistic sample datasets pre-loaded in the application, so that every page renders meaningful content without a live data source.

#### Acceptance Criteria

1. THE Application SHALL include a CSV or JSON file in the `data/` directory for each of the following 10 datasets: Crowd Levels, Gate Occupancy, Parking, Metro Status, Bus Status, Weather, Medical Incidents, Vendor Inventory, Volunteer Availability, Security Alerts.
2. THE Application SHALL load each dataset using a dedicated utility function defined in the `utils/` directory; no dataset loading logic SHALL appear inline within page files.
3. WHEN a dataset file is missing or unreadable, THE Application SHALL render an inline error message in place of the affected component identifying the dataset by name, without impacting the rendering of other components on the page or raising an unhandled exception.
4. THE Sample Datasets SHALL contain between 20 and 500 rows of realistic, non-duplicate data per dataset; each row SHALL include all fields required by the page components that consume that dataset.
5. THE Application SHALL define all data loading and transformation logic in the `utils/` directory, keeping page files free of raw data manipulation code.
6. WHEN a dataset file exists but contains malformed data (invalid JSON/CSV syntax) or fewer than 20 valid rows, THE Application SHALL render an inline error message in place of the affected component identifying the dataset name and the reason (malformed or insufficient data), without raising an unhandled exception.

---

### Requirement 10: Plotly Visualizations

**User Story:** As an organizer, I want interactive charts, so that I can explore stadium metrics in detail without switching to a separate analytics tool.

#### Acceptance Criteria

1. THE Application SHALL render all Plotly charts using the `ChartContainer` component; each rendered chart SHALL display a visible title above the chart area and occupy a minimum height of 200px and a minimum width of 300px.
2. THE Application SHALL use Plotly Express or Plotly Graph Objects exclusively to create all charts; no other charting library SHALL be imported or used.
3. THE Application SHALL apply chart colors exclusively from CSS custom properties already declared in the application's theme CSS file; no hardcoded hex color values SHALL appear in chart construction code.
4. THE Application SHALL include across all pages at least one line or area chart, at least one bar chart, and at least one gauge or indicator chart.
5. WHEN sample data for a time-series chart contains fewer than 2 valid data points, THE Application SHALL render a message inside the `ChartContainer` that includes the phrase "Insufficient data" rather than rendering an empty or broken chart; charts with exactly 2 valid data points SHALL render normally.
6. THE Application SHALL enable hover tooltips on all Plotly charts so that hovering over a data point displays at minimum the x-axis value and y-axis value for that point.

---

### Requirement 11: Prompt-First Architecture Readiness

**User Story:** As a developer, I want the application's data structures and component interfaces to be designed for a single Gemini prompt integration, so that adding AI analysis later requires only one integration point.

#### Acceptance Criteria

1. THE Application SHALL define a single utility function in `utils/` named `build_stadium_context` that aggregates all active Sample Dataset values into one Python dictionary containing at minimum one key per active Sample Dataset category (crowd_levels, gate_occupancy, parking, metro_status, bus_status, weather, medical_incidents, vendor_inventory, volunteer_availability, security_alerts).
2. THE Application SHALL structure the output of `build_stadium_context` so that calling `json.dumps()` on it with no custom encoder raises no exception; the dictionary SHALL NOT contain datetime objects, sets, or custom class instances.
3. THE Application SHALL define a function in `utils/` named `get_ai_recommendations` marked with a comment `# AI INTEGRATION POINT` that accepts a single argument (the stadium context dictionary) and returns a list of one or more static placeholder strings; the function signature SHALL NOT change when Gemini is integrated — only the return logic SHALL change.
4. THE Application SHALL ensure that all `RecommendationCard` components source their content exclusively from the return value of `get_ai_recommendations`; no `RecommendationCard` SHALL hardcode its body text directly in page or component files.
5. THE Application SHALL NOT contain any conditional expression that maps a crowd or sensor metric value to a specific named operational action (e.g., `if crowd_pct > 80: action = "evacuate gate 3"`) outside of the `get_ai_recommendations` function.

---

### Requirement 12: Deployment Readiness

**User Story:** As a DevOps engineer, I want the application to be deployable to Streamlit Community Cloud without manual configuration, so that the team can publish it immediately after development.

#### Acceptance Criteria

1. THE Application SHALL include a `requirements.txt` file at the project root listing every required Python package using exact `==` version notation (e.g., `streamlit==1.35.0`).
2. THE Application SHALL NOT require any environment variables, `.env` files, secrets files, or external configuration files to be present for the initial deployment that uses only Sample Datasets; Gemini API key configuration is explicitly deferred to a future release.
3. THE Application SHALL NOT contain any absolute file paths, home-directory-relative paths (e.g., `~/`), or Windows drive-letter paths (e.g., `C:\`) in any data-loading, asset-loading, or CSS-loading code.
4. WHEN all packages listed in `requirements.txt` are installed, THE Application SHALL start successfully by running `streamlit run app.py` from the project root and reach a ready state within 30 seconds on a standard cloud instance.
5. WHEN the Application starts successfully, THE Application SHALL resolve all Sample Dataset file paths using paths relative to the project root directory, such that the application functions identically whether the project is cloned into any directory name or deployed to Streamlit Community Cloud.
6. WHEN a Sample Dataset file is missing at startup, THE Application SHALL start successfully and render inline error messages for affected components rather than failing to start entirely.
