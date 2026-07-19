"""
pages/mission_control.py

Mission Control — real-time operational overview for event coordinators.
"""

import streamlit as st
import plotly.express as px

from components.metric_card import metric_card
from components.status_badge import status_badge
from components.alert_card import alert_card
from components.timeline_card import timeline_card
from components.recommendation_card import recommendation_card
from components.chart_container import chart_container
from utils.data_loader import load_all_datasets
from utils.context_builder import build_stadium_context
from utils.ai_integration import get_ai_recommendations
from utils.chart_theme import CHART_COLORS, apply_theme


def render() -> None:
    """Render the Mission Control page."""

    st.markdown("## 🎯 Mission Control")

    # -------------------------------------------------------------------------
    # Load data
    # -------------------------------------------------------------------------
    datasets = load_all_datasets()

    crowd_result = datasets.get("crowd_levels")
    gate_result = datasets.get("gate_occupancy")
    parking_result = datasets.get("parking")
    metro_result = datasets.get("metro_status")
    medical_result = datasets.get("medical_incidents")
    vendor_result = datasets.get("vendor_inventory")
    volunteer_result = datasets.get("volunteer_availability")
    security_result = datasets.get("security_alerts")
    weather_result = datasets.get("weather")

    context = build_stadium_context(datasets)
    recs = get_ai_recommendations(context)

    # -------------------------------------------------------------------------
    # System Health Badge
    # -------------------------------------------------------------------------
    health = "Operational"
    if security_result and security_result.success:
        df_sec = security_result.data
        active_sec = df_sec[df_sec["status"].isin(["Active", "Escalated"])]
        if not active_sec.empty:
            if active_sec["severity"].isin(["Critical", "High"]).any():
                health = "Critical"
            elif active_sec["severity"].isin(["Medium"]).any():
                health = "Degraded"

    st.markdown("**System Health:**", unsafe_allow_html=False)
    status_badge(health)

    # -------------------------------------------------------------------------
    # Event Status Panel
    # -------------------------------------------------------------------------
    st.markdown(
        """
<div class="card" style="margin:1rem 0;">
  <div style="display:flex; align-items:center; gap:1rem;">
    <span class="card-title" style="margin-bottom:0;">UEFA Champions League Final</span>
    <span class="badge badge-danger">🔴 LIVE</span>
    <span style="font-family:monospace; font-size:1.1rem; color:#F1F5F9;">01:23:45</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------------
    # Top 4 KPIs
    # -------------------------------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if crowd_result and crowd_result.success:
            try:
                df_c = crowd_result.data
                latest_ts = df_c["timestamp"].max()
                avg_density = df_c[df_c["timestamp"] == latest_ts]["density_pct"].mean()
                metric_card("Crowd Density", f"{avg_density:.1f}", unit="%")
            except Exception:
                metric_card("Crowd Density", "N/A")
        else:
            st.warning(crowd_result.error_message if crowd_result else "Crowd data unavailable.")
            metric_card("Crowd Density", "N/A")

    with c2:
        if weather_result and weather_result.success:
            try:
                df_w = weather_result.data
                row = df_w.iloc[-1]
                condition = row.get("condition", "N/A")
                temp = row.get("temperature_c", "N/A")
                metric_card("Weather", f"{condition}", unit=f" {temp}°C")
            except Exception:
                metric_card("Weather", "N/A")
        else:
            st.warning(weather_result.error_message if weather_result else "Weather data unavailable.")
            metric_card("Weather", "N/A")

    with c3:
        if metro_result and metro_result.success:
            try:
                df_m = metro_result.data
                latest_ts = df_m["timestamp"].max()
                delayed_count = int(
                    (df_m[df_m["timestamp"] == latest_ts]["status"] == "Delayed").sum()
                )
                metric_card("Transport", delayed_count, unit=" delayed lines")
            except Exception:
                metric_card("Transport", "N/A")
        else:
            st.warning(metro_result.error_message if metro_result else "Metro data unavailable.")
            metric_card("Transport", "N/A")

    with c4:
        if medical_result and medical_result.success:
            try:
                df_med = medical_result.data
                open_count = int(
                    df_med["status"].isin(["Escalated", "Open"]).sum()
                )
                metric_card("Emergency", open_count, unit=" open incidents")
            except Exception:
                metric_card("Emergency", "N/A")
        else:
            st.warning(medical_result.error_message if medical_result else "Medical data unavailable.")
            metric_card("Emergency", "N/A")

    st.markdown("---")
    st.markdown("### Key Performance Indicators")

    # -------------------------------------------------------------------------
    # 6 KPI metric cards
    # -------------------------------------------------------------------------
    k1, k2, k3, k4, k5, k6 = st.columns(6)

    with k1:
        if gate_result and gate_result.success:
            try:
                df_g = gate_result.data
                latest_ts = df_g["timestamp"].max()
                avg_occ = df_g[df_g["timestamp"] == latest_ts]["occupancy_pct"].mean()
                metric_card("Gate Occupancy", f"{avg_occ:.1f}", unit="%")
            except Exception:
                metric_card("Gate Occupancy", "N/A")
        else:
            metric_card("Gate Occupancy", "N/A")

    with k2:
        if parking_result and parking_result.success:
            try:
                df_p = parking_result.data
                latest_ts = df_p["timestamp"].max()
                avg_park = df_p[df_p["timestamp"] == latest_ts]["utilization_pct"].mean()
                metric_card("Parking Util", f"{avg_park:.1f}", unit="%")
            except Exception:
                metric_card("Parking Util", "N/A")
        else:
            metric_card("Parking Util", "N/A")

    with k3:
        if metro_result and metro_result.success:
            try:
                df_m = metro_result.data
                latest_ts = df_m["timestamp"].max()
                avg_delay = df_m[df_m["timestamp"] == latest_ts]["delay_minutes"].mean()
                metric_card("Metro Delay", f"{avg_delay:.1f}", unit=" min")
            except Exception:
                metric_card("Metro Delay", "N/A")
        else:
            metric_card("Metro Delay", "N/A")

    with k4:
        if medical_result and medical_result.success:
            try:
                metric_card("Medical Cases", len(medical_result.data))
            except Exception:
                metric_card("Medical Cases", "N/A")
        else:
            metric_card("Medical Cases", "N/A")

    with k5:
        if vendor_result and vendor_result.success:
            try:
                df_v = vendor_result.data
                avg_stock = df_v["stock_level_pct"].mean()
                metric_card("Vendor Stock", f"{avg_stock:.1f}", unit="%")
            except Exception:
                metric_card("Vendor Stock", "N/A")
        else:
            metric_card("Vendor Stock", "N/A")

    with k6:
        if volunteer_result and volunteer_result.success:
            try:
                df_vol = volunteer_result.data
                avg_coverage = df_vol["coverage_pct"].mean()
                metric_card("Volunteer Coverage", f"{avg_coverage:.1f}", unit="%")
            except Exception:
                metric_card("Volunteer Coverage", "N/A")
        else:
            metric_card("Volunteer Coverage", "N/A")

    st.markdown("---")
    st.markdown("### Live Charts")

    # -------------------------------------------------------------------------
    # Charts row
    # -------------------------------------------------------------------------
    chart_col_left, chart_col_right = st.columns([6, 4])

    with chart_col_left:
        if crowd_result and crowd_result.success:
            try:
                df_c = crowd_result.data.copy()
                df_grouped = (
                    df_c.groupby("timestamp")["density_pct"]
                    .mean()
                    .reset_index()
                )
                df_grouped.columns = ["timestamp", "avg_density_pct"]
                fig_area = px.area(
                    df_grouped,
                    x="timestamp",
                    y="avg_density_pct",
                    title="Crowd Density Over Time",
                    color_discrete_sequence=[CHART_COLORS[0]],
                    labels={"avg_density_pct": "Avg Density (%)", "timestamp": "Time"},
                )
                apply_theme(fig_area)
                chart_container(fig_area, "Crowd Density Trend")
            except Exception as exc:
                chart_container(None, f"Crowd Density Trend (error: {exc})")
        else:
            chart_container(None, "Crowd Density Trend")

    with chart_col_right:
        if gate_result and gate_result.success:
            try:
                df_g = gate_result.data.copy()
                latest_ts = df_g["timestamp"].max()
                df_latest = df_g[df_g["timestamp"] == latest_ts]
                fig_bar = px.bar(
                    df_latest,
                    x="gate_id",
                    y="occupancy_pct",
                    title="Gate Occupancy",
                    color_discrete_sequence=[CHART_COLORS[1]],
                    labels={"occupancy_pct": "Occupancy (%)", "gate_id": "Gate"},
                )
                apply_theme(fig_bar)
                chart_container(fig_bar, "Gate Occupancy (Latest)")
            except Exception as exc:
                chart_container(None, f"Gate Occupancy (error: {exc})")
        else:
            chart_container(None, "Gate Occupancy (Latest)")

    st.markdown("---")
    st.markdown("### Active Alerts")

    # -------------------------------------------------------------------------
    # Active Alerts
    # -------------------------------------------------------------------------
    if security_result and security_result.success:
        try:
            df_sec = security_result.data
            active_alerts = df_sec[df_sec["status"] == "Active"]
            if active_alerts.empty:
                st.success("No active alerts.")
            else:
                for _, row in active_alerts.iterrows():
                    alert_card(
                        severity=str(row.get("severity", "Low")),
                        title=str(row.get("title", "")),
                        description=str(row.get("description", "")),
                        timestamp=str(row.get("timestamp", "")),
                    )
        except Exception as exc:
            st.warning(f"Could not render active alerts: {exc}")
    else:
        msg = security_result.error_message if security_result else "Security data unavailable."
        st.warning(msg)

    st.markdown("---")
    st.markdown("### Incident Timeline")

    # -------------------------------------------------------------------------
    # Incident Timeline — top 10 across medical + security
    # -------------------------------------------------------------------------
    import pandas as pd

    timeline_frames = []
    if medical_result and medical_result.success:
        df_med = medical_result.data[["timestamp", "title", "description"]].copy()
        df_med["source"] = "Medical"
        timeline_frames.append(df_med)
    if security_result and security_result.success:
        df_sec_tl = security_result.data[["timestamp", "title", "description"]].copy()
        df_sec_tl["source"] = "Security"
        timeline_frames.append(df_sec_tl)

    if timeline_frames:
        df_timeline = pd.concat(timeline_frames, ignore_index=True)
        df_timeline = df_timeline.sort_values("timestamp", ascending=False).head(10)
        for _, row in df_timeline.iterrows():
            timeline_card(
                event_title=f"[{row['source']}] {row['title']}",
                description=str(row.get("description", "")),
                timestamp=str(row.get("timestamp", "")),
            )
    else:
        st.info("No timeline data available.")

    st.markdown("---")
    st.markdown("### AI Recommendation")

    # -------------------------------------------------------------------------
    # Recommendation Card
    # -------------------------------------------------------------------------
    if recs:
        recommendation_card(
            title="AI Operational Recommendation",
            body=recs[0],
            confidence=78,
        )

    st.markdown("---")
    st.markdown("### Recent Operational Updates")

    # -------------------------------------------------------------------------
    # Recent Operational Updates — top 5 combined
    # -------------------------------------------------------------------------
    update_frames = []
    if security_result and security_result.success:
        df_su = security_result.data[["timestamp", "title", "severity", "status"]].copy()
        df_su["source"] = "Security"
        update_frames.append(df_su)
    if medical_result and medical_result.success:
        df_mu = medical_result.data[["timestamp", "title", "severity", "status"]].copy()
        df_mu["source"] = "Medical"
        update_frames.append(df_mu)

    if update_frames:
        df_updates = pd.concat(update_frames, ignore_index=True)
        df_updates = df_updates.sort_values("timestamp", ascending=False).head(5)
        for _, row in df_updates.iterrows():
            severity_color = {
                "Critical": "#EF4444",
                "High": "#F87171",
                "Medium": "#FBBF24",
                "Low": "#34D399",
            }.get(str(row.get("severity", "")), "#6B7280")
            st.markdown(
                f"""
<div class="card" style="border-left: 3px solid {severity_color}; padding-left: 0.75rem; margin-bottom: 0.5rem;">
  <div style="display:flex; justify-content:space-between;">
    <strong style="color:#F1F5F9;">[{row['source']}] {row['title']}</strong>
    <span style="font-size:0.75rem; color:#64748B;">{row['timestamp']}</span>
  </div>
  <div style="font-size:0.8rem; color:#94A3B8; margin-top:0.25rem;">
    Severity: {row['severity']} &nbsp;|&nbsp; Status: {row['status']}
  </div>
</div>
""",
                unsafe_allow_html=True,
            )
    else:
        st.info("No recent operational updates.")
