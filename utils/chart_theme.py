"""
Chart theme constants mirroring CSS custom properties from styles/main.css.
All chart construction code must import from this module — no hardcoded hex values in chart code.
"""

# ---------------------------------------------------------------------------
# Chart color palette — mirrors --chart-color-* CSS custom properties
# ---------------------------------------------------------------------------

CHART_COLORS = [
    "#4F8EF7",  # --chart-color-1
    "#7C5CFC",  # --chart-color-2
    "#34D399",  # --chart-color-3
    "#FBBF24",  # --chart-color-4
    "#F87171",  # --chart-color-5
    "#60A5FA",  # --chart-color-6
]

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------

CHART_BG = "rgba(0,0,0,0)"
CHART_PAPER_BG = "rgba(0,0,0,0)"
CHART_GRIDCOLOR = "rgba(255,255,255,0.08)"
CHART_FONT_COLOR = "#E2E8F0"

# ---------------------------------------------------------------------------
# Semantic colors — mirrors CSS semantic color custom properties
# ---------------------------------------------------------------------------

COLOR_SUCCESS = "#34D399"   # --color-success
COLOR_WARNING = "#FBBF24"   # --color-warning
COLOR_DANGER = "#F87171"    # --color-danger
COLOR_CRITICAL = "#EF4444"  # --color-critical
COLOR_INFO = "#60A5FA"      # --color-info
COLOR_NEUTRAL = "#6B7280"   # --color-neutral
COLOR_PRIMARY = "#4F8EF7"   # --color-primary


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------

def get_base_layout() -> dict:
    """Return a Plotly layout dict applying the stadium dark theme."""
    return {
        "paper_bgcolor": CHART_BG,
        "plot_bgcolor": CHART_BG,
        "font": {"color": CHART_FONT_COLOR, "family": "Inter, Roboto, DM Sans, sans-serif"},
        "xaxis": {"gridcolor": CHART_GRIDCOLOR, "zerolinecolor": CHART_GRIDCOLOR},
        "yaxis": {"gridcolor": CHART_GRIDCOLOR, "zerolinecolor": CHART_GRIDCOLOR},
        "legend": {"bgcolor": "rgba(0,0,0,0)", "bordercolor": "rgba(255,255,255,0.1)"},
        "margin": {"l": 40, "r": 20, "t": 40, "b": 40},
    }


def apply_theme(fig):
    """Apply the base stadium theme to a Plotly figure and return it."""
    fig.update_layout(**get_base_layout())
    return fig
