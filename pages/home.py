"""
pages/home.py

Home page — entry point for the Stadium Coordinator app.
"""

import streamlit as st

from components.metric_card import metric_card
from components.navigation_card import navigation_card
from utils.data_loader import load_all_datasets


def render() -> None:
    """Render the Home page."""

    # -------------------------------------------------------------------------
    # Hero Banner
    # -------------------------------------------------------------------------
    st.markdown(
        '<div class="hero-banner">'
        "Coordinating Every Decision. Empowering Every Stakeholder."
        "</div>",
        unsafe_allow_html=True,
    )

    if st.button("🚀 Launch Mission Control", use_container_width=False):
        st.session_state["page"] = "mission_control"
        st.rerun()

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Navigation Cards
    # -------------------------------------------------------------------------
    st.markdown("### Navigate the Platform")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        navigation_card(
            page_name="mission_control",
            title="Mission Control",
            description="Real-time operational overview for event coordinators.",
            icon="🎯",
        )
    with col2:
        navigation_card(
            page_name="stakeholder_coordinator",
            title="Stakeholder Coordinator",
            description="Role-based dashboards for every team on the ground.",
            icon="👥",
        )
    with col3:
        navigation_card(
            page_name="scenario_simulator",
            title="Scenario Simulator",
            description="Simulate disruptions and plan coordinated responses.",
            icon="🎭",
        )
    with col4:
        navigation_card(
            page_name="executive_reports",
            title="Executive Reports",
            description="High-level summaries and exportable reports for leadership.",
            icon="📊",
        )

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Architecture Overview
    # -------------------------------------------------------------------------
    st.markdown("### Platform Architecture")
    st.markdown(
        """
<div class="card">
  <div class="card-title">Stakeholder Roles → AI Coordination Layer</div>
  <div style="display:flex; flex-wrap:wrap; gap:0.5rem; margin:1rem 0;">
    <span class="badge badge-neutral">🏟️ Organizer</span>
    <span class="badge badge-neutral">🔒 Security</span>
    <span class="badge badge-neutral">🏥 Medical</span>
    <span class="badge badge-neutral">🙋 Volunteer</span>
    <span class="badge badge-neutral">🛒 Vendor</span>
    <span class="badge badge-neutral">🚌 Transport</span>
    <span class="badge badge-neutral">⭐ Fan</span>
  </div>
  <div class="card-body" style="margin-bottom:0.5rem;">
    All 7 stakeholder roles feed live operational data into the
    <strong>AI Coordination Layer</strong>, which surfaces prioritised
    recommendations across Mission Control, Scenario Simulator, and
    Executive Reports — keeping every team aligned in real time.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Recent Event Snapshot
    # -------------------------------------------------------------------------
    st.markdown("### Recent Event Snapshot")

    datasets = load_all_datasets()

    crowd_result = datasets.get("crowd_levels")
    security_result = datasets.get("security_alerts")
    weather_result = datasets.get("weather")

    col_a, col_b, col_c = st.columns(3)

    # -- Total Attendance --
    with col_a:
        if crowd_result and crowd_result.success:
            try:
                df_crowd = crowd_result.data
                latest_ts = df_crowd["timestamp"].max()
                total_attendance = int(
                    df_crowd[df_crowd["timestamp"] == latest_ts]["current_count"].sum()
                )
                metric_card("Total Attendance", f"{total_attendance:,}", unit="")
            except Exception:
                st.warning("Could not compute attendance from crowd data.")
        else:
            msg = crowd_result.error_message if crowd_result else "Crowd data unavailable."
            st.warning(f"Attendance data unavailable: {msg}")

    # -- Active Alerts --
    with col_b:
        if security_result and security_result.success:
            try:
                df_sec = security_result.data
                active_count = int((df_sec["status"] == "Active").sum())
                metric_card("Active Alerts", active_count)
            except Exception:
                st.warning("Could not compute active alert count.")
        else:
            msg = security_result.error_message if security_result else "Security data unavailable."
            st.warning(f"Alert data unavailable: {msg}")

    # -- Weather --
    with col_c:
        if weather_result and weather_result.success:
            try:
                df_weather = weather_result.data
                latest_weather = df_weather.iloc[-1]
                condition = latest_weather.get("condition", "N/A")
                temp = latest_weather.get("temperature_c", "N/A")
                metric_card("Weather", f"{condition}", unit=f" · {temp}°C")
            except Exception:
                st.warning("Could not read weather data.")
        else:
            msg = weather_result.error_message if weather_result else "Weather data unavailable."
            st.warning(f"Weather data unavailable: {msg}")
