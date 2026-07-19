"""
components/navigation_card.py

Renders a clickable navigation card (.card). Clicking the embedded button
sets st.session_state["page"] to page_name and calls st.rerun() to
navigate immediately.
"""

import streamlit as st


def navigation_card(
    page_name: str,
    title: str,
    description: str,
    icon: str,
) -> None:
    """Render a styled navigation card that navigates on click.

    Parameters
    ----------
    page_name:   The session state page key to navigate to on click.
    title:       Card headline text.
    description: Short description displayed beneath the title.
    icon:        Emoji or icon character shown prominently on the card.
    """
    # Render the decorative card shell via HTML
    st.markdown(
        f"""
<div class="card" style="padding-bottom:0.75rem;">
  <div style="font-size:2rem; margin-bottom:0.5rem;">{icon}</div>
  <div class="card-title">{title}</div>
  <div class="card-body" style="margin-bottom:0.75rem;">{description}</div>
</div>
""",
        unsafe_allow_html=True,
    )
    # Functional button sits directly below the card shell
    if st.button(f"Go to {title}", key=f"nav_card_{page_name}", use_container_width=True):
        st.session_state["page"] = page_name
        st.rerun()
