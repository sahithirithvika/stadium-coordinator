"""Shared pytest fixtures for Stadium Coordinator tests."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
import pandas as pd
from utils.data_loader import DataLoadResult


DATASET_KEYS = [
    'crowd_levels', 'gate_occupancy', 'parking', 'metro_status', 'bus_status',
    'weather', 'medical_incidents', 'vendor_inventory', 'volunteer_availability',
    'security_alerts'
]


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'timestamp': [f'2024-03-15T{i:02d}:00:00' for i in range(25)],
        'value': range(25),
        'label': [f'item_{i}' for i in range(25)],
    })


@pytest.fixture
def success_result(sample_df):
    return DataLoadResult(
        success=True, data=sample_df, error_message=None, dataset_name='test'
    )


@pytest.fixture
def failure_result():
    return DataLoadResult(
        success=False, data=None, error_message='Dataset not found', dataset_name='test'
    )


@pytest.fixture
def all_success_datasets(sample_df):
    return {
        key: DataLoadResult(success=True, data=sample_df.copy(), error_message=None, dataset_name=key)
        for key in DATASET_KEYS
    }


@pytest.fixture
def all_failure_datasets():
    return {
        key: DataLoadResult(success=False, data=None, error_message=f'{key} not found', dataset_name=key)
        for key in DATASET_KEYS
    }
