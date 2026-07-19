"""Unit tests for utils/chart_theme.py"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
import plotly.graph_objects as go
from utils.chart_theme import (
    CHART_COLORS,
    get_base_layout,
    apply_theme,
    COLOR_SUCCESS,
    COLOR_WARNING,
    COLOR_DANGER,
    COLOR_PRIMARY,
)


class TestConstants:
    def test_chart_colors_is_list(self):
        assert isinstance(CHART_COLORS, list)

    def test_chart_colors_has_six_entries(self):
        assert len(CHART_COLORS) == 6

    def test_chart_colors_are_hex_strings(self):
        for color in CHART_COLORS:
            assert isinstance(color, str), f"Expected str, got {type(color)}"
            assert color.startswith('#'), f"Expected hex color starting with #, got {color}"
            assert len(color) in (7, 9), f"Expected #RRGGBB or #RRGGBBAA, got {color}"

    def test_semantic_colors_are_hex(self):
        for name, color in [
            ('COLOR_SUCCESS', COLOR_SUCCESS),
            ('COLOR_WARNING', COLOR_WARNING),
            ('COLOR_DANGER', COLOR_DANGER),
            ('COLOR_PRIMARY', COLOR_PRIMARY),
        ]:
            assert isinstance(color, str), f"{name} should be str"
            assert color.startswith('#'), f"{name} should be hex, got {color}"

    def test_no_duplicate_colors(self):
        assert len(CHART_COLORS) == len(set(CHART_COLORS)), "CHART_COLORS has duplicates"


class TestGetBaseLayout:
    def test_returns_dict(self):
        assert isinstance(get_base_layout(), dict)

    def test_has_paper_bgcolor(self):
        layout = get_base_layout()
        assert 'paper_bgcolor' in layout

    def test_has_plot_bgcolor(self):
        layout = get_base_layout()
        assert 'plot_bgcolor' in layout

    def test_has_font(self):
        layout = get_base_layout()
        assert 'font' in layout
        assert isinstance(layout['font'], dict)

    def test_has_margin(self):
        layout = get_base_layout()
        assert 'margin' in layout

    def test_has_axis_keys(self):
        layout = get_base_layout()
        assert 'xaxis' in layout
        assert 'yaxis' in layout

    def test_is_idempotent(self):
        """Multiple calls return equivalent dicts."""
        assert get_base_layout() == get_base_layout()


class TestApplyTheme:
    def test_returns_figure(self):
        fig = go.Figure()
        result = apply_theme(fig)
        assert result is not None

    def test_returns_same_figure_object(self):
        fig = go.Figure()
        result = apply_theme(fig)
        assert result is fig

    def test_does_not_raise_on_empty_figure(self):
        apply_theme(go.Figure())

    def test_does_not_raise_on_figure_with_traces(self):
        fig = go.Figure(data=[go.Scatter(x=[1, 2], y=[3, 4])])
        apply_theme(fig)

    def test_applies_bgcolor(self):
        fig = go.Figure()
        apply_theme(fig)
        # After applying theme, layout should have paper_bgcolor set
        assert fig.layout.paper_bgcolor is not None
