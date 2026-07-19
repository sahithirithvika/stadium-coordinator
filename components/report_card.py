"""
components/report_card.py

Renders a report section card (.card) with a bold, underlined title
region and a body region below it.
"""

import streamlit as st


def report_card(section_title: str, body: str) -> None:
    """Render a report section card with a styled title and body.

    Parameters
    ----------
    section_title: Bold, colored-underline section heading.
    body:          Report content text (supports basic HTML inline tags).
    """
    html = f"""
<div class="card">
  <div style="
    font-family: var(--font-primary);
    font-size: var(--font-size-md);
    font-weight: var(--font-weight-bold);
    color: #F1F5F9;
    padding-bottom: 0.5rem;
    margin-bottom: 0.75rem;
    border-bottom: 2px solid var(--color-primary);
  ">{section_title}</div>
  <div class="card-body">{body}</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)
