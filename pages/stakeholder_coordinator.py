"""
pages/stakeholder_coordinator.py

Stakeholder Coordinator — role-based dashboards for every team on the ground.
"""

import streamlit as st

from components.metric_card import metric_card
from components.alert_card import alert_card
from components.recommendation_card import recommendation_card
from components.role_selector import role_selector
from utils.data_loader import load_all_datasets
from utils.context_builder import build_stadium_context
from utils.ai_integration import get_ai_recommendations


ROLES = ["Organizer", "Security", "Medical", "Volunteer", "Vendor", "Transport", "Fan"]

# Static task lists per role
_ROLE_TASKS: dict[str, list[str]] = {
    "Organizer": [
        "Review gate occupancy status for all active gates",
        "Confirm volunteer deployment across all zones",
        "Verify vendor restocking schedule before half-time",
        "Approve emergency response plan updates",
    ],
    "Security": [
        "Conduct perimeter sweep of North and East stands",
        "Review CCTV footage for flagged zones",
        "Brief stewards on VIP arrival protocol",
        "Escalate unresolved access control incidents",
    ],
    "Medical": [
        "Confirm first aid staff are stationed at all gates",
        "Restock medical supplies at Pitch-Side Station",
        "Log and close resolved incidents in the system",
        "Prepare heat exhaustion response kits for standing zones",
    ],
    "Volunteer": [
        "Check in with team lead at Gate A information desk",
        "Assist crowd flow management at Section C entry",
        "Distribute event programs to arriving fans",
        "Report any safety concerns to the duty coordinator",
    ],
    "Vendor": [
        "Audit stock levels at all food stalls before kick-off",
        "Coordinate beverage delivery to Section D and E",
        "Submit sales report for the first half",
        "Ensure contactless payment terminals are operational",
    ],
    "Transport": [
        "Monitor metro line delays and update signage",
        "Coordinate additional bus services for peak exit time",
        "Liaise with parking attendants on Zone A capacity",
        "Confirm shuttle schedule for VIP drop-off zone",
    ],
    "Fan": [
        "Check seat location on the stadium map",
        "Review prohibited items list before entry",
        "Note nearest first aid and emergency exits",
        "Follow crowd management instructions from stewards",
    ],
}

# Security alert role relevance keywords
_ROLE_ALERT_KEYWORDS: dict[str, list[str]] = {
    "Organizer": ["Crowd", "Access", "Threat", "VIP", "Perimeter"],
    "Security": ["Threat", "Access", "Perimeter", "VIP", "Crowd"],
    "Medical": [],  # medical shows all active alerts for situational awareness
    "Volunteer": ["Crowd", "Access"],
    "Vendor": [],
    "Transport": [],
    "Fan": ["Crowd"],
}


def _get_role_metrics(role: str, datasets: dict) -> list[tuple]:
    """Return a list of (label, value, unit) tuples for the given role."""
    metrics = []

    crowd_result = datasets.get("crowd_levels")
    gate_result = datasets.get("gate_occupancy")
    parking_result = datasets.get("parking")
    metro_result = datasets.get("metro_status")
    medical_result = datasets.get("medical_incidents")
    vendor_result = datasets.get("vendor_inventory")
    volunteer_result = datasets.get("volunteer_availability")
    security_result = datasets.get("security_alerts")
    weather_result = datasets.get("weather")

    if role == "Organizer":
        # Total attendance, active alerts, avg crowd density
        if crowd_result and crowd_result.success:
            try:
                df = crowd_result.data
                latest_ts = df["timestamp"].max()
                total = int(df[df["timestamp"] == latest_ts]["current_count"].sum())
                metrics.append(("Total Attendance", f"{total:,}", ""))
                avg_density = df[df["timestamp"] == latest_ts]["density_pct"].mean()
                metrics.append(("Avg Crowd Density", f"{avg_density:.1f}", "%"))
            except Exception:
                metrics.append(("Total Attendance", "N/A", ""))
                metrics.append(("Avg Crowd Density", "N/A", ""))
        if security_result and security_result.success:
            try:
                df = security_result.data
                active = int((df["status"] == "Active").sum())
                metrics.append(("Active Alerts", active, ""))
            except Exception:
                metrics.append(("Active Alerts", "N/A", ""))

    elif role == "Security":
        if security_result and security_result.success:
            try:
                df = security_result.data
                active = int(df["status"].isin(["Active", "Escalated"]).sum())
                metrics.append(("Active/Escalated", active, ""))
                resolved = int((df["status"] == "Resolved").sum())
                metrics.append(("Resolved Incidents", resolved, ""))
                critical = int(df["severity"].isin(["Critical", "High"]).sum())
                metrics.append(("Critical/High", critical, ""))
            except Exception:
                metrics += [("Active/Escalated", "N/A", ""), ("Resolved", "N/A", ""), ("Critical/High", "N/A", "")]

    elif role == "Medical":
        if medical_result and medical_result.success:
            try:
                df = medical_result.data
                total = len(df)
                metrics.append(("Total Incidents", total, ""))
                escalated = int((df["status"] == "Escalated").sum())
                metrics.append(("Escalated", escalated, ""))
                critical = int(df["severity"].isin(["Critical", "High"]).sum())
                metrics.append(("Critical/High", critical, ""))
            except Exception:
                metrics += [("Total Incidents", "N/A", ""), ("Escalated", "N/A", ""), ("Critical/High", "N/A", "")]

    elif role == "Volunteer":
        if volunteer_result and volunteer_result.success:
            try:
                df = volunteer_result.data
                on_duty = int((df["status"] == "On Duty").sum())
                metrics.append(("On Duty", on_duty, ""))
                avg_cov = df["coverage_pct"].mean()
                metrics.append(("Avg Coverage", f"{avg_cov:.1f}", "%"))
                available = int((df["status"] == "Available").sum())
                metrics.append(("Available", available, ""))
            except Exception:
                metrics += [("On Duty", "N/A", ""), ("Avg Coverage", "N/A", ""), ("Available", "N/A", "")]

    elif role == "Vendor":
        if vendor_result and vendor_result.success:
            try:
                df = vendor_result.data
                avg_stock = df["stock_level_pct"].mean()
                metrics.append(("Avg Stock Level", f"{avg_stock:.1f}", "%"))
                total_sold = int(df["items_sold"].sum())
                metrics.append(("Total Items Sold", f"{total_sold:,}", ""))
                low_stock = int((df["stock_level_pct"] < 20).sum())
                metrics.append(("Low Stock Stalls", low_stock, ""))
            except Exception:
                metrics += [("Avg Stock Level", "N/A", ""), ("Total Items Sold", "N/A", ""), ("Low Stock", "N/A", "")]

    elif role == "Transport":
        if metro_result and metro_result.success:
            try:
                df = metro_result.data
                latest_ts = df["timestamp"].max()
                df_latest = df[df["timestamp"] == latest_ts]
                delayed = int((df_latest["status"] == "Delayed").sum())
                metrics.append(("Delayed Lines", delayed, ""))
                avg_delay = df_latest["delay_minutes"].mean()
                metrics.append(("Avg Delay", f"{avg_delay:.1f}", " min"))
            except Exception:
                metrics += [("Delayed Lines", "N/A", ""), ("Avg Delay", "N/A", "")]
        if parking_result and parking_result.success:
            try:
                df = parking_result.data
                latest_ts = df["timestamp"].max()
                avg_park = df[df["timestamp"] == latest_ts]["utilization_pct"].mean()
                metrics.append(("Parking Util", f"{avg_park:.1f}", "%"))
            except Exception:
                metrics.append(("Parking Util", "N/A", ""))

    elif role == "Fan":
        if weather_result and weather_result.success:
            try:
                row = weather_result.data.iloc[-1]
                metrics.append(("Weather", str(row.get("condition", "N/A")), f" {row.get('temperature_c', '')}°C"))
            except Exception:
                metrics.append(("Weather", "N/A", ""))
        if crowd_result and crowd_result.success:
            try:
                df = crowd_result.data
                latest_ts = df["timestamp"].max()
                avg_density = df[df["timestamp"] == latest_ts]["density_pct"].mean()
                metrics.append(("Crowd Density", f"{avg_density:.1f}", "%"))
            except Exception:
                metrics.append(("Crowd Density", "N/A", ""))
        if gate_result and gate_result.success:
            try:
                df = gate_result.data
                latest_ts = df["timestamp"].max()
                open_gates = int((df[df["timestamp"] == latest_ts]["status"] == "Open").sum())
                metrics.append(("Open Gates", open_gates, ""))
            except Exception:
                metrics.append(("Open Gates", "N/A", ""))

    # Pad to at least 3
    while len(metrics) < 3:
        metrics.append(("N/A", "—", ""))

    return metrics[:3]


def render() -> None:
    """Render the Stakeholder Coordinator page."""

    st.markdown("## 👥 Stakeholder Coordinator")

    datasets = load_all_datasets()
    context = build_stadium_context(datasets)
    recs = get_ai_recommendations(context)

    # -------------------------------------------------------------------------
    # Role selector
    # -------------------------------------------------------------------------
    selected_role = role_selector(ROLES, st.session_state.get("selected_role", "Organizer"))
    st.session_state["selected_role"] = selected_role

    st.markdown(f"### {selected_role} Dashboard")

    # -------------------------------------------------------------------------
    # 3-column layout: Key Metrics | Task List | Notifications
    # -------------------------------------------------------------------------
    col_metrics, col_tasks, col_notifs = st.columns(3)

    with col_metrics:
        st.markdown("#### Key Metrics")
        role_metrics = _get_role_metrics(selected_role, datasets)
        for label, value, unit in role_metrics:
            metric_card(label, value, unit=unit)

    with col_tasks:
        st.markdown("#### Task List")
        tasks = _ROLE_TASKS.get(selected_role, [])
        for i, task in enumerate(tasks, 1):
            st.markdown(
                f"""
<div class="card" style="padding:0.6rem 0.8rem; margin-bottom:0.4rem;">
  <span style="color:#64748B; font-size:0.8rem; margin-right:0.4rem;">#{i}</span>
  <span class="card-body" style="font-size:0.9rem;">{task}</span>
</div>
""",
                unsafe_allow_html=True,
            )

    with col_notifs:
        st.markdown("#### Notifications")
        security_result = datasets.get("security_alerts")
        if security_result and security_result.success:
            try:
                df_sec = security_result.data
                active_alerts = df_sec[df_sec["status"].isin(["Active", "Escalated"])]
                keywords = _ROLE_ALERT_KEYWORDS.get(selected_role, [])

                if keywords:
                    mask = active_alerts["category"].isin(keywords)
                    relevant = active_alerts[mask]
                else:
                    relevant = active_alerts

                if relevant.empty:
                    st.markdown(
                        '<div class="card-body" style="color:#64748B;">No active notifications.</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    for _, row in relevant.iterrows():
                        alert_card(
                            severity=str(row.get("severity", "Low")),
                            title=str(row.get("title", "")),
                            description=str(row.get("description", "")),
                            timestamp=str(row.get("timestamp", "")),
                        )
            except Exception as exc:
                st.warning(f"Could not load notifications: {exc}")
        else:
            msg = security_result.error_message if security_result else "Security data unavailable."
            st.warning(msg)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # AI Recommendation for selected role
    # -------------------------------------------------------------------------
    role_index = ROLES.index(selected_role) if selected_role in ROLES else 0
    rec_body = recs[role_index % len(recs)] if recs else "No recommendation available."
    recommendation_card(
        title=f"AI Recommendation for {selected_role}",
        body=rec_body,
        confidence=72,
    )
