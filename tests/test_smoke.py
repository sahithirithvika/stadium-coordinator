"""Smoke tests: verify all modules and data files are intact."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest


class TestModuleImports:
    def test_data_loader_imports(self):
        from utils import data_loader
        assert hasattr(data_loader, 'load_all_datasets')
        assert hasattr(data_loader, 'load_dataset')
        assert hasattr(data_loader, 'DataLoadResult')

    def test_context_builder_imports(self):
        from utils import context_builder
        assert hasattr(context_builder, 'build_stadium_context')

    def test_ai_integration_imports(self):
        from utils import ai_integration
        assert hasattr(ai_integration, 'get_ai_recommendations')

    def test_chart_theme_imports(self):
        from utils import chart_theme
        assert hasattr(chart_theme, 'CHART_COLORS')
        assert hasattr(chart_theme, 'apply_theme')
        assert hasattr(chart_theme, 'get_base_layout')

    def test_all_components_importable(self):
        component_names = [
            'metric_card', 'status_badge', 'alert_card', 'timeline_card',
            'recommendation_card', 'role_selector', 'navigation_card',
            'report_card', 'chart_container'
        ]
        for name in component_names:
            module = __import__(f'components.{name}', fromlist=[name])
            assert module is not None, f"Could not import components.{name}"


class TestDataFilesExist:
    DATA_FILES = [
        'crowd_levels.csv', 'gate_occupancy.csv', 'parking.csv',
        'medical_incidents.csv', 'security_alerts.csv', 'vendor_inventory.csv',
        'volunteer_availability.csv', 'metro_status.json', 'bus_status.json',
        'weather.json'
    ]

    def test_all_data_files_exist(self):
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        for filename in self.DATA_FILES:
            path = os.path.join(data_dir, filename)
            assert os.path.exists(path), f"Missing data file: {filename}"

    def test_data_files_non_empty(self):
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        for filename in self.DATA_FILES:
            path = os.path.join(data_dir, filename)
            if os.path.exists(path):
                assert os.path.getsize(path) > 100, f"Suspiciously small data file: {filename}"
