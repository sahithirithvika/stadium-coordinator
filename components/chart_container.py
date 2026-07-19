"""
components/chart_container.py

Wraps a Plotly figure inside a .card frame with a title above it.
Plotly is imported lazily at call time to avoid ImportError if the
package is not yet installed when the module is first loaded.
"""

import streamlit as st


def chart_container(figure, title: str) -> None:
    """Render a Plotly figure inside a glassmorphism card.

    Parameters
    ----------
    figure: A Plotly Figure object, or None.
            If None, a "No data available" message is displayed instead.
    title:  Card heading displayed above the chart.
    """
    # Card header
    st.markdown(
        f"""
<div class="card" style="padding-bottom:0.5rem;">
  <div class="card-title" style="margin-bottom:0.75rem;">{title}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if figure is None:
        st.markdown(
            '<div class="card-body" style="text-align:center; padding:1.5rem 0;">'
            "No data available"
            "</div>",
            unsafe_allow_html=True,
        )
        return

    # Lazy import — only executed when a figure is actually provided
    try:
        import plotly.graph_objects  # noqa: F401 — verify plotly is available
    except ImportError as exc:
        st.error(f"Plotly is not installed: {exc}")
        return

    st.plotly_chart(figure, use_container_width=True)
