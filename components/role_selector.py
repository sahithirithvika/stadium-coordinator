"""
components/role_selector.py

Renders a horizontal row of role-selection buttons. The active role is
tracked in st.session_state["selected_role"]. Active button uses a
distinct visual style via inline CSS (primary color highlight).
"""

import streamlit as st


def role_selector(roles: list, selected_role: str) -> str:
    """Render a horizontal role-selection button group.

    Parameters
    ----------
    roles:         List of role name strings to display.
    selected_role: The currently active role name.

    Returns
    -------
    str: The currently selected role name after any click interaction.
    """
    if not roles:
        return selected_role

    # Sync with session state if already set
    current = st.session_state.get("selected_role", selected_role)

    cols = st.columns(len(roles))
    for col, role in zip(cols, roles):
        is_active = role == current
        # Inject scoped style for the active button via a unique key container
        if is_active:
            col.markdown(
                f"""
                <style>
                  div[data-testid="column"] button[kind="secondary"]{{}}
                </style>
                """,
                unsafe_allow_html=True,
            )
        with col:
            # Use a visual hint in the label for the active role
            label = f"✦ {role}" if is_active else role
            if st.button(label, key=f"role_btn_{role}", use_container_width=True):
                st.session_state["selected_role"] = role
                current = role
                st.rerun()

    return current
