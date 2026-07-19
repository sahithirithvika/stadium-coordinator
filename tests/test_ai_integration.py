"""Unit tests for utils/ai_integration.py"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from utils.ai_integration import get_ai_recommendations


class TestGetAiRecommendations:
    def test_returns_list(self):
        result = get_ai_recommendations({})
        assert isinstance(result, list)

    def test_non_empty(self):
        result = get_ai_recommendations({})
        assert len(result) >= 1

    def test_all_strings(self):
        result = get_ai_recommendations({})
        for item in result:
            assert isinstance(item, str)
            assert len(item.strip()) > 0

    def test_accepts_various_dicts(self):
        for ctx in [{}, {'key': 'val'}, {'a': [1, 2]}, {'n': 99}]:
            result = get_ai_recommendations(ctx)
            assert isinstance(result, list)
            assert len(result) >= 1

    def test_never_raises(self):
        try:
            result = get_ai_recommendations({})
            assert isinstance(result, list)
        except Exception as e:
            pytest.fail(f"Raised unexpectedly: {e}")
