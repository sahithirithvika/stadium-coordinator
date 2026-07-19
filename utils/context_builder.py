"""
utils/context_builder.py

Aggregates all active Sample Dataset values into a single JSON-serializable
dictionary for the prompt-first AI integration layer (Requirement 11).
"""

import json
import math
from datetime import datetime
from typing import Any

# Guard against pandas being unavailable
try:
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False


# Ordered list of the 10 dataset keys used throughout the application.
DATASET_KEYS = [
    "crowd_levels",
    "gate_occupancy",
    "parking",
    "metro_status",
    "bus_status",
    "weather",
    "medical_incidents",
    "vendor_inventory",
    "volunteer_availability",
    "security_alerts",
]


def _sanitize_for_json(obj: Any) -> Any:
    """Recursively converts non-JSON-serializable values into safe equivalents.

    Conversions applied:
    - datetime             → ISO 8601 string via .isoformat()
    - pandas Timestamp     → ISO 8601 string via .isoformat()
    - float NaN / ±Inf    → None
    - set                  → sorted list (elements also sanitized)
    - dict                 → dict with sanitized keys and values
    - list / tuple         → list with sanitized elements
    - Any other type that
      is not str/int/bool/
      NoneType              → str()
    """
    # None and JSON-native scalars are fine as-is
    if obj is None:
        return None
    if isinstance(obj, bool):
        # bool must come before int because bool is a subclass of int
        return obj
    if isinstance(obj, int):
        return obj

    # Float — guard against NaN and infinity
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj

    # Strings are already serializable
    if isinstance(obj, str):
        return obj

    # datetime (and subclasses, including date) → ISO string
    if isinstance(obj, datetime):
        return obj.isoformat()

    # pandas Timestamp (only if pandas is installed)
    if _PANDAS_AVAILABLE and isinstance(obj, pd.Timestamp):
        return obj.isoformat()

    # pandas NA / NaT values → None
    if _PANDAS_AVAILABLE:
        try:
            if pd.isna(obj):
                return None
        except (TypeError, ValueError):
            pass

    # set → sorted list (sort tolerantly — mixed types fall back to str sort)
    if isinstance(obj, set):
        sanitized_items = [_sanitize_for_json(v) for v in obj]
        try:
            return sorted(sanitized_items)
        except TypeError:
            return sorted(sanitized_items, key=str)

    # dict → recurse over keys and values
    if isinstance(obj, dict):
        return {str(k): _sanitize_for_json(v) for k, v in obj.items()}

    # list / tuple → recurse
    if isinstance(obj, (list, tuple)):
        return [_sanitize_for_json(v) for v in obj]

    # Fallback: convert anything else to its string representation
    return str(obj)


def build_stadium_context(datasets: dict) -> dict:
    """Aggregate all active dataset values into one JSON-serializable dictionary.

    Parameters
    ----------
    datasets : dict
        A mapping of ``{dataset_name: DataLoadResult}`` as returned by
        ``data_loader.load_all_datasets()``.  Each ``DataLoadResult`` is
        expected to have:
        - ``.success`` (bool)   — True when the dataset loaded without errors
        - ``.data``             — a ``pandas.DataFrame`` when success is True

    Returns
    -------
    dict
        Exactly 10 keys (see ``DATASET_KEYS``).  For each key:
        - If the corresponding ``DataLoadResult.success`` is ``True``, the
          value is a list of record dicts converted via
          ``DataFrame.to_dict(orient='records')``, with all values sanitized
          so that ``json.dumps(result)`` succeeds with no custom encoder.
        - If ``DataLoadResult.success`` is ``False`` (or the key is absent
          from *datasets*), the value is an empty list ``[]``.
    """
    context: dict = {}

    for key in DATASET_KEYS:
        result = datasets.get(key)

        if result is not None and getattr(result, "success", False):
            # Convert DataFrame rows to plain dicts
            try:
                if _PANDAS_AVAILABLE and isinstance(result.data, pd.DataFrame):
                    records = result.data.to_dict(orient="records")
                elif isinstance(result.data, list):
                    records = result.data
                else:
                    records = []
            except Exception:
                records = []

            # Deep-sanitize every record so json.dumps() never fails
            context[key] = _sanitize_for_json(records)
        else:
            context[key] = []

    # Guarantee all 10 keys are present even if datasets dict was sparse
    for key in DATASET_KEYS:
        if key not in context:
            context[key] = []

    # Final validation: ensure json.dumps succeeds (raises if sanitization
    # missed an edge case — surfaces bugs early rather than at AI call time)
    json.dumps(context)

    return context
