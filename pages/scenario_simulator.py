"""
pages/scenario_simulator.py

Scenario Simulator — simulate operational disruptions and plan coordinated responses.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from components.recommendation_card import recommendation_card
from components.chart_container import chart_container
from utils.data_loader import load_all_datasets
from utils.context_builder import build_stadium_context
from utils.ai_integration import get_ai_recommendations
from utils.chart_theme import CHART_COLORS, apply_theme


# ---------------------------------------------------------------------------
# Scenario definitions
# ---------------------------------------------------------------------------

_SCENARIO_CONDITIONS: dict[str, list[dict]] = {
    "Heavy Rain": [
        {
            "title": "Weather Alert",
            "body": "Heavy rainfall detected — wind speed 45 km/h, visibility reduced to 3 km. "
                    "Standing zones and exposed concourses are affected. Water pooling reported near Gate D.",
        },
        {
            "title": "Crowd Impact",
            "body": "Fan movement to covered areas increasing crowd density in concourses by an estimated 30%. "
                    "Gate queues slowing due to shelter-seeking behaviour.",
        },
    ],
    "Gate Congestion": [
        {
            "title": "Entry Bottleneck",
            "body": "Gate C queue exceeds safe threshold — occupancy at 94%. "
                    "Ticket scanning throughput has dropped to 220 fans/minute.",
        },
        {
            "title": "Overflow Risk",
            "body": "Adjacent gates A and B absorbing overflow but approaching 80% occupancy. "
                    "Crowd pressure on perimeter barriers is elevated.",
        },
    ],
    "Medical Emergency": [
        {
            "title": "Critical Incident Active",
            "body": "Cardiac event reported in Section B, Row 8. AED deployed, ambulance en route. "
                    "First aid team on scene; all medical stations placed on elevated readiness.",
        },
        {
            "title": "Resource Status",
            "body": "Two of five pitch-side medical stations are currently occupied. "
                    "Additional paramedic cover requested for North Stand.",
        },
    ],
    "VIP Arrival": [
        {
            "title": "VIP Convoy ETA: 12 minutes",
            "body": "High-profile dignitary convoy approaching via East Gate. "
                    "Security escort confirmed; VIP route cleared of general public.",
        },
        {
            "title": "Protocol Activation",
            "body": "VIP lounge on Level 3 confirmed ready. Press pool access restricted. "
                    "Crowd management officers deployed along the transit corridor.",
        },
    ],
    "Power Failure": [
        {
            "title": "Partial Power Outage — Sectors C & D",
            "body": "Mains power failure detected in Sectors C and D. Emergency lighting activated. "
                    "CCTV feeds in affected zones have switched to backup power.",
        },
        {
            "title": "Operational Impact",
            "body": "4 turnstiles at Gate C are offline; manual entry protocols initiated. "
                    "PA system operating on backup generator — crowd announcements unaffected.",
        },
    ],
    "Extra Time": [
        {
            "title": "Match Extended — Extra Time Confirmed",
            "body": "Match has entered extra time (30 additional minutes). "
                    "Transport operators notified; metro and bus schedules adjusted.",
        },
        {
            "title": "Fan Services Extension",
            "body": "Vendor licences extended by 45 minutes. "
                    "Security and medical shift handovers delayed to maintain full coverage through the extended period.",
        },
    ],
}

_SCENARIO_STAKEHOLDERS: dict[str, list[dict]] = {
    "Heavy Rain": [
        {"role": "Security", "actions": ["Deploy additional stewards to covered zones", "Clear standing water near Gate D barriers"]},
        {"role": "Medical", "actions": ["Pre-position hypothermia blankets at first aid stations", "Monitor crowd crush risk in sheltered concourses"]},
        {"role": "Transport", "actions": ["Alert bus operators to potential route delays due to flooding", "Issue fan advisory for early departure"]},
    ],
    "Gate Congestion": [
        {"role": "Security", "actions": ["Open Gate F as overflow entry point", "Deploy additional stewards to Gate C perimeter"]},
        {"role": "Organizer", "actions": ["Broadcast crowd distribution announcement on PA", "Coordinate with ticketing team to expedite scanning"]},
        {"role": "Volunteer", "actions": ["Guide fans to less congested gates A and B", "Manage queue discipline at Gate C"]},
    ],
    "Medical Emergency": [
        {"role": "Medical", "actions": ["Dispatch second paramedic team to Section B", "Clear egress route to ambulance access point"]},
        {"role": "Security", "actions": ["Cordon off Section B Row 8 area", "Escort ambulance through service tunnel"]},
    ],
    "VIP Arrival": [
        {"role": "Security", "actions": ["Clear and secure VIP transit corridor", "Brief all gate security on arrival protocol"]},
        {"role": "Volunteer", "actions": ["Redirect general public away from East Gate", "Assist VIP lounge check-in on Level 3"]},
    ],
    "Power Failure": [
        {"role": "Organizer", "actions": ["Activate manual entry protocol at Gate C", "Notify fans via PA system of sector restrictions"]},
        {"role": "Security", "actions": ["Increase foot patrols in Sectors C and D", "Verify CCTV backup feed integrity"]},
        {"role": "Vendor", "actions": ["Switch POS terminals to offline mode", "Notify affected stalls to operate cash-only temporarily"]},
    ],
    "Extra Time": [
        {"role": "Transport", "actions": ["Extend metro and bus dispatch windows by 45 minutes", "Coordinate with parking on extended stay fee waivers"]},
        {"role": "Vendor", "actions": ["Extend operating hours for food and beverage stalls", "Prepare additional stock for increased demand"]},
    ],
}

_SCENARIO_CHART_DATA: dict[str, pd.DataFrame] = {}


def _get_scenario_chart(scenario: str):
    """Build and return a Plotly figure for the given scenario."""
    if scenario in ("Heavy Rain", "Extra Time"):
        # Line chart — crowd density over simulated time
        df = pd.DataFrame({
            "Minute": [0, 5, 10, 15, 20, 25, 30, 35, 40, 45],
            "North Stand": [62, 65, 70, 74, 78, 83, 87, 85, 82, 80],
            "South Stand": [60, 63, 67, 72, 77, 80, 84, 83, 81, 79],
            "Concourse": [45, 52, 61, 70, 80, 88, 92, 91, 89, 87],
        })
        df_melted = df.melt(id_vars="Minute", var_name="Zone", value_name="Density (%)")
        fig = px.line(
            df_melted,
            x="Minute",
            y="Density (%)",
            color="Zone",
            title=f"Simulated Crowd Density — {scenario}",
            color_discrete_sequence=CHART_COLORS,
        )
    elif scenario == "Gate Congestion":
        df = pd.DataFrame({
            "Gate": ["Gate A", "Gate B", "Gate C", "Gate D", "Gate E", "Gate F", "Gate G", "Gate H"],
            "Occupancy (%)": [78, 80, 94, 72, 35, 5, 68, 75],
        })
        fig = px.bar(
            df,
            x="Gate",
            y="Occupancy (%)",
            title="Simulated Gate Occupancy — Gate Congestion",
            color="Occupancy (%)",
            color_continuous_scale=["#34D399", "#FBBF24", "#EF4444"],
        )
    elif scenario == "Medical Emergency":
        df = pd.DataFrame({
            "Station": ["Gate A FA", "Gate C FA", "Pitch-Side N", "Pitch-Side S", "Main Med Centre"],
            "Capacity Used (%)": [40, 55, 100, 80, 65],
        })
        fig = px.bar(
            df,
            x="Station",
            y="Capacity Used (%)",
            title="First Aid Station Utilisation — Medical Emergency",
            color_discrete_sequence=[CHART_COLORS[4]],
        )
    elif scenario == "VIP Arrival":
        df = pd.DataFrame({
            "Zone": ["East Gate", "VIP Corridor", "VIP Lounge", "Press Area", "General Entry"],
            "Staff Deployed": [12, 8, 6, 4, 20],
        })
        fig = px.bar(
            df,
            x="Zone",
            y="Staff Deployed",
            title="Security Staff Deployment — VIP Arrival",
            color_discrete_sequence=[CHART_COLORS[1]],
        )
    elif scenario == "Power Failure":
        df = pd.DataFrame({
            "Sector": ["Sector A", "Sector B", "Sector C", "Sector D", "Sector E"],
            "Power Status (%)": [100, 100, 0, 0, 95],
        })
        fig = px.bar(
            df,
            x="Sector",
            y="Power Status (%)",
            title="Power Availability by Sector — Power Failure",
            color="Power Status (%)",
            color_continuous_scale=["#EF4444", "#FBBF24", "#34D399"],
        )
    else:
        return None

    apply_theme(fig)
    return fig


def render() -> None:
    """Render the Scenario Simulator page."""

    st.markdown("## 🎭 Scenario Simulator")

    datasets = load_all_datasets()
    context = build_stadium_context(datasets)
    recs = get_ai_recommendations(context)

    # -------------------------------------------------------------------------
    # Scenario selector
    # -------------------------------------------------------------------------
    scenario_options = [
        "-- Select a Scenario --",
        "Heavy Rain",
        "Gate Congestion",
        "Medical Emergency",
        "VIP Arrival",
        "Power Failure",
        "Extra Time",
    ]

    selected = st.selectbox("Select Scenario", scenario_options, index=0)

    if selected == "-- Select a Scenario --":
        st.info("Select a scenario above to begin simulation.")
        return

    # -------------------------------------------------------------------------
    # Scenario context cards
    # -------------------------------------------------------------------------
    st.markdown(f"### 🔍 Simulated Conditions: {selected}")
    conditions = _SCENARIO_CONDITIONS.get(selected, [])
    for condition in conditions:
        st.markdown(
            f"""
<div class="card" style="border-left: 4px solid #4F8EF7; padding-left: 1rem;">
  <div class="card-title">{condition['title']}</div>
  <div class="card-body">{condition['body']}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### 🤖 AI Recommendations")

    # -------------------------------------------------------------------------
    # Recommendation Cards
    # -------------------------------------------------------------------------
    rec_col1, rec_col2 = st.columns(2)
    with rec_col1:
        recommendation_card(
            title=f"Primary Action — {selected}",
            body=recs[0] if len(recs) > 0 else "No recommendation available.",
            confidence=75,
        )
    with rec_col2:
        recommendation_card(
            title=f"Secondary Action — {selected}",
            body=recs[1] if len(recs) > 1 else "No recommendation available.",
            confidence=68,
        )

    st.markdown("---")
    st.markdown("### 👥 Affected Stakeholders & Actions")

    # -------------------------------------------------------------------------
    # Affected stakeholders panel
    # -------------------------------------------------------------------------
    stakeholders = _SCENARIO_STAKEHOLDERS.get(selected, [])
    if stakeholders:
        cols = st.columns(len(stakeholders))
        for col, stakeholder in zip(cols, stakeholders):
            with col:
                actions_html = "".join(
                    f'<li style="margin-bottom:0.35rem;">{action}</li>'
                    for action in stakeholder["actions"]
                )
                col.markdown(
                    f"""
<div class="card">
  <div class="card-title">{stakeholder['role']}</div>
  <ul style="margin:0; padding-left:1.2rem; color:#94A3B8; font-size:0.85rem;">
    {actions_html}
  </ul>
</div>
""",
                    unsafe_allow_html=True,
                )

    st.markdown("---")
    st.markdown("### 📊 Scenario Impact Chart")

    # -------------------------------------------------------------------------
    # Chart
    # -------------------------------------------------------------------------
    fig = _get_scenario_chart(selected)
    chart_container(fig, f"Scenario Analysis — {selected}")
