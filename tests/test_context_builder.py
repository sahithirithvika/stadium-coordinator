"""Unit tests for utils/context_builder.py"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import json
import pytest
import pandas as pd
from utils.context_builder import build_stadium_context, _sanitize_for_json
from utils.data_loader import DataLoadResult

KEYS = [
    'crowd_levels', 'gate_occupancy', 'parking', 'metro_status', 'bus_status',
    'weather', 'medical_incidents', 'vendor_inventory', 'volunteer_availability',
    'security_alerts'
]


def _ok(k):
    df = pd.DataFrame({'ts': [f'2024-{i:02d}' for i in range(1, 26)], 'v': range(25)})
    return DataLoadResult(success=True, data=df, error_message=None, dataset_name=k)


def _fail(k):
    return DataLoadResult(success=False, data=None, error_message=f'{k} missing', dataset_name=k)


class TestBuildStadiumContext:
    def test_returns_dict(self):
        result = build_stadium_context({k: _ok(k) for k in KEYS})
        assert isinstance(result, dict)

    def test_has_all_10_keys(self):
        result = build_stadium_context({k: _ok(k) for k in KEYS})
        for k in KEYS:
            assert k in result, f"Missing key: {k}"

    def test_json_serializable(self):
        result = build_stadium_context({k: _ok(k) for k in KEYS})
        json.dumps(result)  # must not raise

    def test_successful_datasets_are_lists(self):
        result = build_stadium_context({k: _ok(k) for k in KEYS})
        for k in KEYS:
            assert isinstance(result[k], list), f"{k} should be a list"

    def test_successful_datasets_non_empty(self):
        result = build_stadium_context({k: _ok(k) for k in KEYS})
        for k in KEYS:
            assert len(result[k]) == 25, f"{k} should have 25 records"

    def test_failed_datasets_return_empty_list(self):
        result = build_stadium_context({k: _fail(k) for k in KEYS})
        for k in KEYS:
            assert result[k] == [], f"{k} should be [] on failure"

    def test_empty_input_safe(self):
        result = build_stadium_context({})
        assert len(result) == 10
        for k in KEYS:
            assert result[k] == []
        json.dumps(result)

    def test_mixed_success_failure(self):
        datasets = {k: (_ok(k) if i % 2 == 0 else _fail(k)) for i, k in enumerate(KEYS)}
        result = build_stadium_context(datasets)
        assert len(result) == 10
        json.dumps(result)


class TestSanitizeForJson:
    def test_none_passthrough(self):
        assert _sanitize_for_json(None) is None

    def test_string_passthrough(self):
        assert _sanitize_for_json('hello') == 'hello'

    def test_int_passthrough(self):
        assert _sanitize_for_json(42) == 42

    def test_bool_passthrough(self):
        assert _sanitize_for_json(True) is True
        assert _sanitize_for_json(False) is False

    def test_nan_becomes_none(self):
        assert _sanitize_for_json(float('nan')) is None

    def test_inf_becomes_none(self):
        assert _sanitize_for_json(float('inf')) is None
        assert _sanitize_for_json(float('-inf')) is None

    def test_set_becomes_list(self):
        result = _sanitize_for_json({1, 2, 3})
        assert isinstance(result, list)
        assert sorted(result) == [1, 2, 3]

    def test_dict_recurses(self):
        result = _sanitize_for_json({'a': float('nan'), 'b': 1})
        assert result['a'] is None
        assert result['b'] == 1

    def test_list_recurses(self):
        result = _sanitize_for_json([float('nan'), 'ok', 5])
        assert result[0] is None
        assert result[1] == 'ok'
        assert result[2] == 5
