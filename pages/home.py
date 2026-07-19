"""
pages/home.py — Home Page

Renders the Stadium Coordinator landing page with:
  - Hero banner with tagline and subtitle
  - Five navigation cards (one per page)
  - Live KPI summary row (total attendance, active alerts, parking utilisation, weather)
"""

import streamlit as st

from components import (
    metric_card,
    navigation_card,
)
from utils.data_loader import load_all_datasets


def render() -> None:
    """Render the Home page."""

    # -----------------------------------------------------------------------
    # Hero Banner
    # -----------------------------------------------------------------------
    st.markdown(
        """
<div class="hero-banner">
  <div class="hero-tagline">🏟️ Stadium Coordinator</div>
  <div class="hero-subtitle">
    One Situation. Multiple Perspectives. One Coordinated Response.<br>
    Enterprise-grade operational intelligence for live stadium events.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # Quick-access KPI row
    # -----------------------------------------------------------------------
    datasets = load_all_datasets()

    # Total current attendance from crowd_levels (sum of current_count at latest timestamp)
    total_attendance = "—"
    crowd_result = datasets.get("crowd_levels")
    if crowd_result and crowd_result.success and crowd_result.data is not None:
        df = crowd_result.data
        if "timestamp" in df.columns and "current_count" in df.columns:
            latest_ts = df["timestamp"].max()
            latest = df[df["timestamp"] == latest_ts]
            total_attendance = f"{int(latest['current_count'].sum()):,}"

    # Active security alerts
    active_alerts = "—"
    alerts_result = datasets.get("security_alerts")
    if alerts_result and alerts_result.success and alerts_result.data is not None:
        df = alerts_result.data
        if "status" in df.columns:
            active_alerts = str(len(df[df["status"].isin(["Active", "Escalated", "Monitoring"])]))

    # Average parking utilisation
    avg_parking = "—"
    parking_result = datasets.get("parking")
    if parking_result and parking_result.success and parking_result.data is not None:
        df = parking_result.data
        if "utilization_pct" in df.columns:
            avg_parking = f"{df['utilization_pct'].mean():.0f}%"

    # Latest weather condition
    weather_val = "—"
    weather_result = datasets.get("weather")
    if weather_result and weather_result.success and weather_result.data is not None:
        df = weather_result.data
        if "timestamp" in df.columns and "condition" in df.columns and "temperature_c" in df.columns:
            latest_ts = df["timestamp"].max()
            row = df[df["timestamp"] == latest_ts].iloc[0]
            weather_val = f"{row['condition']}, {row['temperature_c']}°C"

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        metric_card("Total Attendance", total_attendance, unit="")
    with kpi_cols[1]:
        metric_card("Active Alerts", active_alerts, unit="")
    with kpi_cols[2]:
        metric_card("Avg Parking Util", avg_parking, unit="")
    with kpi_cols[3]:
        metric_card("Current Weather", weather_val, unit="")

    st.markdown("---")

    # -----------------------------------------------------------------------
    # Navigation Cards — 5 pages in a 2-3 layout
    # -----------------------------------------------------------------------
    st.markdown(
        '<div class="card-title" style="margin-bottom:1rem;">Platform Modules</div>',
        unsafe_allow_html=True,
    )

    row1 = st.columns(2)
    row2 = st.columns(3)

    nav_items = [
        (
            "mission_control",
            "Mission Control",
            "Real-time crowd density, gate occupancy, transport, parking and weather overview.",
            "🎛️",
        ),
        (
            "stakeholder_coordinator",
            "Stakeholder Coordinator",
            "Role-filtered views for Security, Medical, Operations and Logistics teams.",
            "👥",
        ),
        (
            "scenario_simulator",
            "Scenario Simulator",
            "Run what-if scenarios — crowd surge, transport failure, weather emergencies.",
            "🔬",
        ),
        (
            "executive_reports",
            "Executive Reports",
            "Auto-generated post-event summaries with KPI scorecards and incident timelines.",
            "📊",
        ),
    ]

    for i, (page_name, title, desc, icon) in enumerate(nav_items):
        col = row1[i] if i < 2 else row2[i - 2]
        with col:
            navigation_card(page_name=page_name, title=title, description=desc, icon=icon)
