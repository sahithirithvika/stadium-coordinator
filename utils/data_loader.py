"""
utils/data_loader.py — Dataset loading utilities.

All dataset loading logic is centralised here. Page files must never load
data inline — they call load_all_datasets() or load_dataset() instead.
"""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass, field

import pandas as pd

BASE_DIR = pathlib.Path(__file__).parent.parent  # project root


@dataclass
class DataLoadResult:
    success: bool
    data: pd.DataFrame | None
    error_message: str | None
    dataset_name: str


def load_dataset(dataset_name: str, relative_path: str) -> DataLoadResult:
    """Load a single CSV or JSON dataset file.

    Returns DataLoadResult with success=False on any error condition;
    never raises an unhandled exception.
    """
    abs_path = BASE_DIR / relative_path

    if not abs_path.exists():
        return DataLoadResult(
            success=False,
            data=None,
            error_message=f"Dataset '{dataset_name}' file not found: {relative_path}",
            dataset_name=dataset_name,
        )

    try:
        suffix = abs_path.suffix.lower()
        if suffix == ".csv":
            df = pd.read_csv(abs_path)
        elif suffix == ".json":
            with open(abs_path, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
            if isinstance(raw, list):
                df = pd.DataFrame(raw)
            elif isinstance(raw, dict):
                df = pd.DataFrame([raw])
            else:
                return DataLoadResult(
                    success=False,
                    data=None,
                    error_message=f"Dataset '{dataset_name}' has unsupported JSON structure.",
                    dataset_name=dataset_name,
                )
        else:
            return DataLoadResult(
                success=False,
                data=None,
                error_message=f"Dataset '{dataset_name}' has unsupported file extension: {suffix}",
                dataset_name=dataset_name,
            )

        if len(df) < 20:
            return DataLoadResult(
                success=False,
                data=None,
                error_message=(
                    f"Dataset '{dataset_name}' has fewer than 20 valid rows "
                    f"({len(df)} found)."
                ),
                dataset_name=dataset_name,
            )

        return DataLoadResult(success=True, data=df, error_message=None, dataset_name=dataset_name)

    except Exception as exc:  # noqa: BLE001
        return DataLoadResult(
            success=False,
            data=None,
            error_message=f"Dataset '{dataset_name}' failed to load: {exc}",
            dataset_name=dataset_name,
        )


_DATASET_REGISTRY: dict[str, str] = {
    "crowd_levels":           "data/crowd_levels.csv",
    "gate_occupancy":         "data/gate_occupancy.csv",
    "parking":                "data/parking.csv",
    "metro_status":           "data/metro_status.json",
    "bus_status":             "data/bus_status.json",
    "weather":                "data/weather.json",
    "medical_incidents":      "data/medical_incidents.csv",
    "vendor_inventory":       "data/vendor_inventory.csv",
    "volunteer_availability": "data/volunteer_availability.csv",
    "security_alerts":        "data/security_alerts.csv",
}


def load_all_datasets() -> dict[str, DataLoadResult]:
    """Load all 10 stadium datasets. Always returns a dict with all 10 keys."""
    return {
        name: load_dataset(name, path)
        for name, path in _DATASET_REGISTRY.items()
    }
