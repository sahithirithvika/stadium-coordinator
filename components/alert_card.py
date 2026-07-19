"""
components/alert_card.py

Renders an alert card (.card) with a left-side colored border that
reflects severity level. Badge, title, description, and timestamp
are all displayed.
"""

import html
import streamlit as st

# Severity → (CSS variable for border color, badge CSS class)
_SEVERITY_MAP = {
    "low":      ("var(--color-info)",     "badge-neutral"),
    "medium":   ("var(--color-warning)",  "badge-warning"),
    "high":     ("var(--color-danger)",   "badge-danger"),
    "critical": ("var(--color-critical)", "badge-critical"),
}

# Fallback for unknown severities
_DEFAULT_SEVERITY = ("var(--color-neutral)", "badge-neutral")


def alert_card(
    severity: str,
    title: str,
    description: str,
    timestamp: str,
) -> None:
    """Render a severity-coded alert card.

    Parameters
    ----------
    severity:    "Low", "Medium", "High", or "Critical" (case-insensitive).
    title:       Short alert headline.
    description: Full alert message body.
    timestamp:   Human-readable time string shown at the bottom.
    """
    border_color, badge_class = _SEVERITY_MAP.get(
        severity.lower() if isinstance(severity, str) else "",
        _DEFAULT_SEVERITY,
    )

    title = html.escape(str(title))
    description = html.escape(str(description))
    timestamp = html.escape(str(timestamp))

    html_str = f"""
<div class="card" style="border-left: 4px solid {border_color}; padding-left: 1rem;">
  <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
    <span class="badge {badge_class}">{severity}</span>
    <span class="card-title" style="margin-bottom:0;">{title}</span>
  </div>
  <div class="card-body" style="margin-bottom:0.75rem;">{description}</div>
  <div style="font-size:var(--font-size-xs); color:#475569;">{timestamp}</div>
</div>
"""
    st.markdown(html_str, unsafe_allow_html=True)
