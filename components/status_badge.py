"""
components/status_badge.py

Renders an inline status badge using badge CSS classes defined in
styles/main.css. Never raises — unknown statuses fall back to badge-neutral.
"""

import streamlit as st

# Mapping of known status strings (case-insensitive) to CSS badge classes
_STATUS_CLASS_MAP = {
    "operational": "badge-success",
    "warning":     "badge-warning",
    "degraded":    "badge-warning",
    "critical":    "badge-critical",
}


def status_badge(status: str) -> None:
    """Render a colored status badge pill.

    Parameters
    ----------
    status: One of "Operational", "Warning", "Degraded", "Critical",
            or any other string (renders as neutral).
    """
    if not isinstance(status, str):
        status = str(status)

    css_class = _STATUS_CLASS_MAP.get(status.lower(), "badge-neutral")

    html = f'<span class="badge {css_class}">{status}</span>'
    st.markdown(html, unsafe_allow_html=True)
