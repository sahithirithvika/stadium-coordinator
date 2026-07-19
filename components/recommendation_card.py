"""
components/recommendation_card.py

Renders an AI recommendation card. Always shows an "🤖 AI Placeholder"
badge (.ai-placeholder-label) and a confidence percentage. The body text
is always caller-supplied — nothing is hardcoded here.
"""

import streamlit as st


def recommendation_card(title: str, body: str, confidence: float) -> None:
    """Render an AI recommendation card.

    Parameters
    ----------
    title:      Recommendation headline.
    body:       Recommendation detail text. Must be provided by the caller.
    confidence: Float 0–100 representing model confidence percentage.
    """
    html = f"""
<div class="card">
  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.75rem;">
    <span class="card-title" style="margin-bottom:0;">{title}</span>
    <span class="ai-placeholder-label">🤖 AI Placeholder</span>
  </div>
  <div class="card-body" style="margin-bottom:0.75rem;">{body}</div>
  <div style="font-size:var(--font-size-xs); color:#64748B;">
    {confidence:.0f}% confidence
  </div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)
