"""
Stadium Coordinator — Application Entry Point

This file contains only:
  - Import statements
  - CSS loader (styles/)
  - Session state initialization
  - Sidebar navigation rendering
  - Page routing logic

No page-rendering logic or component definitions reside here.
"""

import pathlib
import logging
import os
import streamlit as st

logging.basicConfig(
    level=getattr(logging, os.environ.get("LOG_LEVEL", "INFO"), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("stadium_coordinator")

# ---------------------------------------------------------------------------
# CSS Loader — inject all .css files from styles/ via a single st.markdown call
# ---------------------------------------------------------------------------

def _load_css() -> None:
    """Read every .css file under styles/ and inject via one st.markdown call."""
    styles_dir = pathlib.Path(__file__).parent / "styles"
    css_parts = []
    if styles_dir.exists():
        for css_file in sorted(styles_dir.glob("*.css")):
            css_parts.append(css_file.read_text(encoding="utf-8"))
    if css_parts:
        combined = "\n".join(css_parts)
        st.markdown(f"<style>{combined}</style>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Page module lazy imports — wrapped in try/except so app.py doesn't crash
# before page files exist
# ---------------------------------------------------------------------------

def _import_page(module_name: str):
    """Lazily import a page module; return None if the module does not exist yet."""
    try:
        import importlib
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        return None


# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------

def _init_session_state() -> None:
    """Initialize all required session state keys with their default values."""
    defaults = {
        "page": "home",
        "selected_role": "Organizer",
        "selected_scenario": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------

# Ordered page definitions: (display_label, session_state_key)
_PAGES = [
    ("Home", "home"),
    ("Mission Control", "mission_control"),
    ("Stakeholder Coordinator", "stakeholder_coordinator"),
    ("Scenario Simulator", "scenario_simulator"),
    ("Executive Reports", "executive_reports"),
]


def _render_sidebar() -> None:
    """Render the sidebar navigation listing all 5 pages in order."""
    with st.sidebar:
        st.title("Stadium Coordinator")
        st.markdown("---")
        for label, key in _PAGES:
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state["page"] = key
                st.rerun()
        st.markdown("---")
        st.caption("Enterprise Operational Platform")


# ---------------------------------------------------------------------------
# Page routing
# ---------------------------------------------------------------------------

def _route_page() -> None:
    """Route to the correct page module based on session state, or render
    a 'Page Not Found' message for unknown page keys."""
    current_page = st.session_state.get("page", "home")

    if current_page == "home":
        module = _import_page("pages.home")
        if module:
            module.render()
        else:
            st.info("Home page is coming soon.")

    elif current_page == "mission_control":
        module = _import_page("pages.mission_control")
        if module:
            module.render()
        else:
            st.info("Mission Control page is coming soon.")

    elif current_page == "stakeholder_coordinator":
        module = _import_page("pages.stakeholder_coordinator")
        if module:
            module.render()
        else:
            st.info("Stakeholder Coordinator page is coming soon.")

    elif current_page == "scenario_simulator":
        module = _import_page("pages.scenario_simulator")
        if module:
            module.render()
        else:
            st.info("Scenario Simulator page is coming soon.")

    elif current_page == "executive_reports":
        module = _import_page("pages.executive_reports")
        if module:
            module.render()
        else:
            st.info("Executive Reports page is coming soon.")

    else:
        st.error(f"Page Not Found: '{current_page}' is not a recognized page.")


# ---------------------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Stadium Coordinator",
    page_icon="🏟️",
    layout="wide",
    initial_sidebar_state="expanded",
)

logger.info("Stadium Coordinator starting up")
_load_css()
_init_session_state()
_render_sidebar()
_route_page()
