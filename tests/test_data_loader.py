"""Unit tests for utils/data_loader.py"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
import pandas as pd
from utils.data_loader import DataLoadResult, load_dataset, load_all_datasets


class TestDataLoadResult:
    def test_success_fields(self):
        df = pd.DataFrame({'a': range(25)})
        r = DataLoadResult(success=True, data=df, error_message=None, dataset_name='test')
        assert r.success is True
        assert r.data is not None
        assert r.error_message is None
        assert r.dataset_name == 'test'

    def test_failure_fields(self):
        r = DataLoadResult(success=False, data=None, error_message='not found', dataset_name='x')
        assert r.success is False
        assert r.data is None
        assert r.error_message == 'not found'


class TestLoadDataset:
    def test_missing_file_returns_failure(self):
        result = load_dataset('test_ds', 'data/nonexistent_xyz_abc.csv')
        assert result.success is False
        assert result.data is None
        assert result.error_message is not None

    def test_returns_dataloadresult_type(self):
        result = load_dataset('test', 'data/crowd_levels.csv')
        assert isinstance(result, DataLoadResult)

    def test_never_raises(self):
        for path in ['', 'bad/path.csv', 'data/../../etc/passwd']:
            result = load_dataset('test', path)
            assert isinstance(result, DataLoadResult)

    def test_successful_load_has_dataframe(self):
        result = load_dataset('crowd_levels', 'data/crowd_levels.csv')
        if result.success:
            assert isinstance(result.data, pd.DataFrame)
            assert len(result.data) >= 20

    def test_error_message_contains_dataset_name(self):
        result = load_dataset('my_unique_dataset', 'data/nonexistent.csv')
        assert result.success is False


class TestLoadAllDatasets:
    EXPECTED_KEYS = [
        'crowd_levels', 'gate_occupancy', 'parking', 'metro_status', 'bus_status',
        'weather', 'medical_incidents', 'vendor_inventory', 'volunteer_availability',
        'security_alerts'
    ]

    def test_returns_dict(self):
        result = load_all_datasets()
        assert isinstance(result, dict)

    def test_has_exactly_10_keys(self):
        result = load_all_datasets()
        assert len(result) == 10

    def test_all_expected_keys_present(self):
        result = load_all_datasets()
        for key in self.EXPECTED_KEYS:
            assert key in result, f"Missing dataset key: {key}"

    def test_all_values_are_dataloadresult(self):
        result = load_all_datasets()
        for key, value in result.items():
            assert isinstance(value, DataLoadResult), f"Key {key} wrong type"

    def test_successful_datasets_have_dataframes(self):
        result = load_all_datasets()
        for key, value in result.items():
            if value.success:
                assert value.data is not None
                assert isinstance(value.data, pd.DataFrame)

    def test_failed_datasets_have_error_messages(self):
        result = load_all_datasets()
        for key, value in result.items():
            if not value.success:
                assert value.error_message is not None
