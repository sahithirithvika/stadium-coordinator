"""
components/metric_card.py

Renders a glassmorphism KPI card using .card, .kpi-label, and .kpi-value
CSS classes defined in styles/main.css.
"""

import streamlit as st


def metric_card(label: str, value, unit: str = "", delta=None) -> None:
    """Render a styled KPI card.

    Parameters
    ----------
    label:  Short uppercase label displayed above the value.
    value:  The primary metric value (number or string).
    unit:   Optional unit string appended to the value (e.g. "%", "mph").
    delta:  Optional trend indicator.
            - Positive number or string starting with "+" → green delta.
            - Negative number or string starting with "-" → red delta.
            - None (default) → no delta row rendered.
    """
    # Determine delta HTML
    delta_html = ""
    if delta is not None:
        delta_str = str(delta)
        is_positive = (
            (isinstance(delta, (int, float)) and delta >= 0)
            or delta_str.startswith("+")
        )
        is_negative = (
            (isinstance(delta, (int, float)) and delta < 0)
            or delta_str.startswith("-")
        )
        if is_positive:
            delta_html = (
                f'<div class="kpi-delta-positive">▲ {delta_str}</div>'
            )
        elif is_negative:
            delta_html = (
                f'<div class="kpi-delta-negative">▼ {delta_str}</div>'
            )
        else:
            # Neutral delta — render with neutral color
            delta_html = (
                f'<div style="font-size:var(--font-size-sm);color:#94A3B8;">'
                f'{delta_str}</div>'
            )

    value_display = f"{value}{unit}" if unit else str(value)

    html = f"""
<div class="card">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value_display}</div>
  {delta_html}
</div>
"""
    st.markdown(html, unsafe_allow_html=True)
