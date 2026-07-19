"""
pages/executive_reports.py

Executive Reports — high-level summaries and exportable reports for leadership.
"""

import streamlit as st

from components.status_badge import status_badge
from components.report_card import report_card
from components.recommendation_card import recommendation_card
from utils.data_loader import load_all_datasets
from utils.context_builder import build_stadium_context
from utils.ai_integration import get_ai_recommendations


def render() -> None:
    """Render the Executive Reports page."""

    st.markdown("## 📊 Executive Reports")

    datasets = load_all_datasets()
    context = build_stadium_context(datasets)
    recs = get_ai_recommendations(context)

    security_result = datasets.get("security_alerts")
    medical_result = datasets.get("medical_incidents")
    crowd_result = datasets.get("crowd_levels")
    volunteer_result = datasets.get("volunteer_availability")
    vendor_result = datasets.get("vendor_inventory")
    metro_result = datasets.get("metro_status")
    gate_result = datasets.get("gate_occupancy")

    # -------------------------------------------------------------------------
    # Risk Status Badge
    # -------------------------------------------------------------------------
    risk = "Operational"
    if security_result and security_result.success:
        df_sec = security_result.data
        active_sec = df_sec[df_sec["status"].isin(["Active", "Escalated"])]
        if not active_sec.empty:
            if active_sec["severity"].isin(["Critical", "High"]).any():
                risk = "Critical"
            elif active_sec["severity"].isin(["Medium"]).any():
                risk = "Warning"

    st.markdown("**Operational Risk Level:**")
    status_badge(risk)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Operational Summary report_card
    # -------------------------------------------------------------------------
    total_incidents = 0
    if medical_result and medical_result.success:
        total_incidents = len(medical_result.data)
    elif not (medical_result and medical_result.success):
        if medical_result:
            st.warning(medical_result.error_message)

    op_summary_body = (
        f"<strong>Total Events:</strong> 1 &nbsp;|&nbsp; "
        f"<strong>Personnel Deployed:</strong> 247 &nbsp;|&nbsp; "
        f"<strong>Total Incidents:</strong> {total_incidents}"
    )
    report_card("Operational Summary", op_summary_body)

    # -------------------------------------------------------------------------
    # Incident Summary report_card — first 10 medical incidents
    # -------------------------------------------------------------------------
    if medical_result and medical_result.success:
        try:
            df_med = medical_result.data.head(10)
            rows_html = ""
            for _, row in df_med.iterrows():
                severity_color = {
                    "Critical": "#EF4444",
                    "High": "#F87171",
                    "Medium": "#FBBF24",
                    "Low": "#34D399",
                }.get(str(row.get("severity", "")), "#6B7280")
                rows_html += (
                    f"<tr>"
                    f"<td style='padding:0.3rem 0.5rem; color:#F1F5F9;'>{row.get('title', '')}</td>"
                    f"<td style='padding:0.3rem 0.5rem; color:#94A3B8;'>{row.get('category', '')}</td>"
                    f"<td style='padding:0.3rem 0.5rem; color:{severity_color};'>{row.get('severity', '')}</td>"
                    f"</tr>"
                )
            incident_table = (
                "<table style='width:100%; border-collapse:collapse; font-size:0.85rem;'>"
                "<thead><tr>"
                "<th style='text-align:left; padding:0.3rem 0.5rem; color:#64748B; border-bottom:1px solid rgba(255,255,255,0.1);'>Title</th>"
                "<th style='text-align:left; padding:0.3rem 0.5rem; color:#64748B; border-bottom:1px solid rgba(255,255,255,0.1);'>Category</th>"
                "<th style='text-align:left; padding:0.3rem 0.5rem; color:#64748B; border-bottom:1px solid rgba(255,255,255,0.1);'>Severity</th>"
                "</tr></thead>"
                f"<tbody>{rows_html}</tbody>"
                "</table>"
            )
            report_card("Incident Summary (First 10 Medical Incidents)", incident_table)
        except Exception as exc:
            report_card("Incident Summary", f"Could not load incident data: {exc}")
    else:
        msg = medical_result.error_message if medical_result else "Medical data unavailable."
        st.warning(msg)
        report_card("Incident Summary", "No incident data available.")

    # -------------------------------------------------------------------------
    # Stakeholder Summary report_card
    # -------------------------------------------------------------------------
    stakeholder_rows = ""

    # Organizer
    try:
        total_att = "N/A"
        if crowd_result and crowd_result.success:
            df = crowd_result.data
            latest_ts = df["timestamp"].max()
            total_att = f"{int(df[df['timestamp'] == latest_ts]['current_count'].sum()):,}"
        stakeholder_rows += f"<tr><td>🏟️ Organizer</td><td>Attendance tracked: {total_att}</td></tr>"
    except Exception:
        stakeholder_rows += "<tr><td>🏟️ Organizer</td><td>N/A</td></tr>"

    # Security
    try:
        sec_count = "N/A"
        if security_result and security_result.success:
            sec_count = str(len(security_result.data))
        stakeholder_rows += f"<tr><td>🔒 Security</td><td>Total alerts logged: {sec_count}</td></tr>"
    except Exception:
        stakeholder_rows += "<tr><td>🔒 Security</td><td>N/A</td></tr>"

    # Medical
    try:
        med_count = "N/A"
        if medical_result and medical_result.success:
            med_count = str(len(medical_result.data))
        stakeholder_rows += f"<tr><td>🏥 Medical</td><td>Total incidents: {med_count}</td></tr>"
    except Exception:
        stakeholder_rows += "<tr><td>🏥 Medical</td><td>N/A</td></tr>"

    # Volunteer
    try:
        vol_count = "N/A"
        if volunteer_result and volunteer_result.success:
            vol_count = str(len(volunteer_result.data))
        stakeholder_rows += f"<tr><td>🙋 Volunteer</td><td>Volunteer records: {vol_count}</td></tr>"
    except Exception:
        stakeholder_rows += "<tr><td>🙋 Volunteer</td><td>N/A</td></tr>"

    # Vendor
    try:
        vnd_count = "N/A"
        if vendor_result and vendor_result.success:
            vnd_count = str(len(vendor_result.data))
        stakeholder_rows += f"<tr><td>🛒 Vendor</td><td>Vendor records: {vnd_count}</td></tr>"
    except Exception:
        stakeholder_rows += "<tr><td>🛒 Vendor</td><td>N/A</td></tr>"

    # Transport
    try:
        metro_count = "N/A"
        if metro_result and metro_result.success:
            df = metro_result.data
            latest_ts = df["timestamp"].max()
            delayed = int((df[df["timestamp"] == latest_ts]["status"] == "Delayed").sum())
            metro_count = f"{delayed} delayed lines"
        stakeholder_rows += f"<tr><td>🚌 Transport</td><td>Metro status: {metro_count}</td></tr>"
    except Exception:
        stakeholder_rows += "<tr><td>🚌 Transport</td><td>N/A</td></tr>"

    # Fan
    try:
        gate_count = "N/A"
        if gate_result and gate_result.success:
            df = gate_result.data
            latest_ts = df["timestamp"].max()
            open_gates = int((df[df["timestamp"] == latest_ts]["status"] == "Open").sum())
            gate_count = f"{open_gates} gates open"
        stakeholder_rows += f"<tr><td>⭐ Fan</td><td>Entry: {gate_count}</td></tr>"
    except Exception:
        stakeholder_rows += "<tr><td>⭐ Fan</td><td>N/A</td></tr>"

    stakeholder_table = (
        "<table style='width:100%; border-collapse:collapse; font-size:0.85rem;'>"
        "<thead><tr>"
        "<th style='text-align:left; padding:0.3rem 0.5rem; color:#64748B; border-bottom:1px solid rgba(255,255,255,0.1);'>Role</th>"
        "<th style='text-align:left; padding:0.3rem 0.5rem; color:#64748B; border-bottom:1px solid rgba(255,255,255,0.1);'>Activity</th>"
        "</tr></thead>"
        f"<tbody style='color:#94A3B8;'>"
        + "".join(
            f"<tr><td style='padding:0.3rem 0.5rem;'>{r}</td></tr>"
            for r in stakeholder_rows.replace("</tr>", "\n").replace("<tr>", "").split("\n")
            if r.strip()
        )
        + "</tbody></table>"
    )

    # Rebuild table cleanly
    stakeholder_table_clean = (
        "<table style='width:100%; border-collapse:collapse; font-size:0.85rem;'>"
        "<thead><tr>"
        "<th style='text-align:left; padding:0.3rem 0.5rem; color:#64748B; border-bottom:1px solid rgba(255,255,255,0.1);'>Role</th>"
        "<th style='text-align:left; padding:0.3rem 0.5rem; color:#64748B; border-bottom:1px solid rgba(255,255,255,0.1);'>Activity</th>"
        "</tr></thead>"
        f"<tbody>{stakeholder_rows}</tbody>"
        "</table>"
    )
    report_card("Stakeholder Activity Summary", stakeholder_table_clean)

    st.markdown("---")
    st.markdown("### 🤖 AI Recommendations")

    # -------------------------------------------------------------------------
    # 3 Recommendation Cards
    # -------------------------------------------------------------------------
    rcol1, rcol2, rcol3 = st.columns(3)
    with rcol1:
        recommendation_card(
            title="Recommended Action 1",
            body=recs[0] if len(recs) > 0 else "No recommendation available.",
            confidence=73,
        )
    with rcol2:
        recommendation_card(
            title="Recommended Action 2",
            body=recs[1] if len(recs) > 1 else "No recommendation available.",
            confidence=76,
        )
    with rcol3:
        recommendation_card(
            title="Recommended Action 3",
            body=recs[2 % len(recs)] if recs else "No recommendation available.",
            confidence=79,
        )

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Export Button
    # -------------------------------------------------------------------------
    if st.button("📥 Export Report"):
        st.info("📄 Export feature coming soon!")
