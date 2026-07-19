"""
components/timeline_card.py

Renders a single timeline entry using the .timeline-entry and
.timeline-connector CSS classes defined in styles/main.css.
"""

import html
import streamlit as st


def timeline_card(event_title: str, description: str, timestamp: str) -> None:
    """Render a timeline entry with a dot marker and vertical connector line.

    Parameters
    ----------
    event_title: Headline for this timeline event.
    description: Supporting detail text below the title.
    timestamp:   Time string displayed at the top-right of the entry.
    """
    event_title = html.escape(str(event_title))
    description = html.escape(str(description))
    timestamp = html.escape(str(timestamp))

    html_str = f"""
<div class="timeline-entry">
  <div class="timeline-connector"></div>
  <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.25rem;">
    <span class="card-title" style="margin-bottom:0;">{event_title}</span>
    <span style="font-size:var(--font-size-xs); color:#475569; white-space:nowrap; margin-left:1rem;">{timestamp}</span>
  </div>
  <div class="card-body">{description}</div>
</div>
"""
    st.markdown(html_str, unsafe_allow_html=True)
