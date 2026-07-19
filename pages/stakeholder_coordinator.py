"""
pages/stakeholder_coordinator.py — Stakeholder Coordinator Page

Role-filtered operational dashboard. The role selector at the top filters
the displayed data and alerts to the perspective of:
  - Security
  - Medical
  - Operations
  - Logistics
"""

import streamlit as st

from components import (
    metric_card,
    alert_card,
    status_badge,
    role_selector,
    timeline_card,
    recommendation_card,
)
from utils.data_loader import load_all_datasets
from utils.context_builder import build_stadium_context
from utils.ai_integration import get_ai_recommendations


_ROLES = ["Security", "Medical", "Operations", "Logistics"]


def _render_security(datasets: dict) -> None:
    st.markdown("### Security Dashboard")

    alerts_result = datasets.get("security_alerts")
    if alerts_result and alerts_result.success and alerts_result.data is not None:
        df = alerts_result.data

        # Filter to active / escalated
        if "status" in df.columns:
            active = df[df["status"].isin(["Active", "Escalated"])]
        else:
            active = df

        cols = st.columns(3)
        with cols[0]:
            metric_card("Total Alerts", str(len(df)))
        with cols[1]:
            metric_card("Active / Escalated", str(len(active)))
        with cols[2]:
            critical_count = int(df["severity"].eq("Critical").sum()) if "severity" in df.columns else 0
            metric_card("Critical", str(critical_count))

        st.markdown("#### Active Security Alerts")
        display = active.head(10) if len(active) > 10 else active
        for _, row in display.iterrows():
            alert_card(
                severity=str(row.get("severity", "Low")),
                title=str(row.get("title", "Alert")),
                description=str(row.get("description", "")),
                timestamp=str(row.get("timestamp", "")),
            )
    else:
        st.warning("Security data unavailable.")


def _render_medical(datasets: dict) -> None:
    st.markdown("### Medical Dashboard")

    med_result = datasets.get("medical_incidents")
    if med_result and med_result.success and med_result.data is not None:
        df = med_result.data

        escalated = df[df["status"] == "Escalated"] if "status" in df.columns else df

        cols = st.columns(3)
        with cols[0]:
            metric_card("Total Incidents", str(len(df)))
        with cols[1]:
            metric_card("Escalated", str(len(escalated)))
        with cols[2]:
            critical_count = int(df["severity"].eq("Critical").sum()) if "severity" in df.columns else 0
            metric_card("Critical", str(critical_count))

        # Category breakdown
        if "category" in df.columns:
            st.markdown("#### Incidents by Category")
            cats = df["category"].value_counts()
            cat_cols = st.columns(min(len(cats), 4))
            for i, (cat, count) in enumerate(cats.items()):
                with cat_cols[i % 4]:
                    metric_card(cat, str(count))

        st.markdown("#### Incident Timeline")
        display = df.head(15) if len(df) > 15 else df
        for _, row in display.iterrows():
            timeline_card(
                event_title=str(row.get("title", "Incident")),
                description=str(row.get("description", "")),
                timestamp=str(row.get("timestamp", "")),
            )
    else:
        st.warning("Medical incident data unavailable.")


def _render_operations(datasets: dict) -> None:
    st.markdown("### Operations Dashboard")

    gate_result = datasets.get("gate_occupancy")
    crowd_result = datasets.get("crowd_levels")

    if gate_result and gate_result.success and gate_result.data is not None:
        df = gate_result.data
        if "timestamp" in df.columns:
            latest_ts = df["timestamp"].max()
            latest = df[df["timestamp"] == latest_ts]

            st.markdown("#### Gate Status Overview")
            for _, row in latest.iterrows():
                c1, c2, c3 = st.columns([2, 1, 3])
                with c1:
                    st.write(f"**{row.get('gate_id', '—')}**")
                with c2:
                    status_badge(str(row.get("status", "—")))
                with c3:
                    occ = row.get("occupancy_pct", 0)
                    q = row.get("queue_length", 0)
                    st.write(f"Occupancy: {occ:.0f}% · Queue: {q}")

    if crowd_result and crowd_result.success and crowd_result.data is not None:
        df = crowd_result.data
        if "timestamp" in df.columns and "density_pct" in df.columns:
            latest_ts = df["timestamp"].max()
            latest = df[df["timestamp"] == latest_ts]
            avg = latest["density_pct"].mean()
            max_section = latest.loc[latest["density_pct"].idxmax(), "section"]
            max_val = latest["density_pct"].max()

            cols = st.columns(2)
            with cols[0]:
                metric_card("Avg Crowd Density", f"{avg:.1f}", unit="%")
            with cols[1]:
                metric_card("Busiest Section", max_section, unit=f" ({max_val:.0f}%)")

    vol_result = datasets.get("volunteer_availability")
    if vol_result and vol_result.success and vol_result.data is not None:
        df = vol_result.data
        st.markdown("#### Volunteer Status")
        if "status" in df.columns:
            on_duty = len(df[df["status"] == "On Duty"])
            on_break = len(df[df["status"] == "Break"])
            unavailable = len(df[df["status"] == "Unavailable"])
            cols = st.columns(3)
            with cols[0]:
                metric_card("On Duty", str(on_duty))
            with cols[1]:
                metric_card("On Break", str(on_break))
            with cols[2]:
                metric_card("Unavailable", str(unavailable))


def _render_logistics(datasets: dict) -> None:
    st.markdown("### Logistics Dashboard")

    vendor_result = datasets.get("vendor_inventory")
    parking_result = datasets.get("parking")

    if vendor_result and vendor_result.success and vendor_result.data is not None:
        df = vendor_result.data

        if "stock_level_pct" in df.columns:
            low_stock = df[df["stock_level_pct"] < 25]
            avg_stock = df["stock_level_pct"].mean()

            cols = st.columns(3)
            with cols[0]:
                metric_card("Total Vendors", str(len(df)))
            with cols[1]:
                metric_card("Avg Stock Level", f"{avg_stock:.0f}", unit="%")
            with cols[2]:
                metric_card("Low Stock (<25%)", str(len(low_stock)))

            if len(low_stock) > 0:
                st.markdown("#### ⚠️ Low Stock Vendors")
                for _, row in low_stock.iterrows():
                    alert_card(
                        severity="High",
                        title=str(row.get("vendor_name", "Vendor")),
                        description=f"Stock at {row['stock_level_pct']:.0f}% — {row.get('section', '')}",
                        timestamp=str(row.get("timestamp", "")),
                    )

    if parking_result and parking_result.success and parking_result.data is not None:
        df = parking_result.data
        if "timestamp" in df.columns:
            latest_ts = df["timestamp"].max()
            latest = df[df["timestamp"] == latest_ts]

            st.markdown("#### Parking Zones")
            for _, row in latest.iterrows():
                c1, c2, c3 = st.columns([2, 2, 2])
                with c1:
                    st.write(f"**{row.get('zone', '—')}**")
                with c2:
                    util = row.get("utilization_pct", 0)
                    label = "Critical" if util >= 95 else ("Warning" if util >= 80 else "Operational")
                    status_badge(label)
                with c3:
                    avail = row.get("available_spaces", 0)
                    st.write(f"{util:.0f}% full · {avail} spaces left")


def render() -> None:
    """Render the Stakeholder Coordinator page."""

    st.markdown(
        '<div class="card-title" style="font-size:1.5rem; margin-bottom:1rem;">👥 Stakeholder Coordinator</div>',
        unsafe_allow_html=True,
    )

    # Role selector
    selected = role_selector(_ROLES, st.session_state.get("selected_role", "Security"))

    st.markdown("---")

    datasets = load_all_datasets()

    # Role-filtered content
    if selected == "Security":
        _render_security(datasets)
    elif selected == "Medical":
        _render_medical(datasets)
    elif selected == "Operations":
        _render_operations(datasets)
    elif selected == "Logistics":
        _render_logistics(datasets)

    # -----------------------------------------------------------------------
    # AI Recommendations (always shown, role label used in title)
    # -----------------------------------------------------------------------
    st.markdown("---")
    st.markdown(f"#### AI Recommendations for {selected}")

    context = build_stadium_context(datasets)
    recommendations = get_ai_recommendations(context)

    # Show up to 3 recommendations
    for i, rec in enumerate(recommendations[:3], 1):
        recommendation_card(
            title=f"Recommendation {i}",
            body=rec,
            confidence=85.0 - (i - 1) * 5.0,
        )
