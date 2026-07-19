"""
pages/scenario_simulator.py — Scenario Simulator Page

Enables operators to run what-if simulations by adjusting parameters for
three pre-built scenarios:
  1. Crowd Surge — simulate elevated crowd density across sections
  2. Transport Failure — disable metro / bus lines and model attendance impact
  3. Weather Emergency — model the effect of severe weather on operations

Each scenario shows projected KPI impact and AI recommendations based on
the simulated context.
"""

import streamlit as st

from components import (
    metric_card,
    recommendation_card,
    alert_card,
)
from utils.data_loader import load_all_datasets
from utils.context_builder import build_stadium_context
from utils.ai_integration import get_ai_recommendations


_SCENARIO_OPTIONS = [
    "Crowd Surge",
    "Transport Failure",
    "Weather Emergency",
]


def _simulate_crowd_surge(datasets: dict, surge_pct: float) -> dict:
    """Return a modified datasets dict with crowd density elevated by surge_pct."""
    import copy

    sim = copy.deepcopy(datasets)
    crowd_result = sim.get("crowd_levels")
    if crowd_result and crowd_result.success and crowd_result.data is not None:
        df = crowd_result.data.copy()
        if "density_pct" in df.columns and "current_count" in df.columns and "capacity" in df.columns:
            df["density_pct"] = (df["density_pct"] * (1 + surge_pct / 100)).clip(upper=100)
            df["current_count"] = (df["capacity"] * df["density_pct"] / 100).astype(int)
            crowd_result.data = df
    return sim


def _simulate_transport_failure(datasets: dict, metro_lines_down: int, bus_routes_down: int) -> dict:
    """Return modified datasets dict with specified number of transport services cancelled."""
    import copy

    sim = copy.deepcopy(datasets)

    metro_result = sim.get("metro_status")
    if metro_result and metro_result.success and metro_result.data is not None:
        df = metro_result.data.copy()
        if "status" in df.columns:
            lines = df["line"].unique()[:metro_lines_down]
            df.loc[df["line"].isin(lines), "status"] = "Suspended"
            df.loc[df["line"].isin(lines), "delay_minutes"] = 60
            metro_result.data = df

    bus_result = sim.get("bus_status")
    if bus_result and bus_result.success and bus_result.data is not None:
        df = bus_result.data.copy()
        if "status" in df.columns:
            routes = df["route"].unique()[:bus_routes_down]
            df.loc[df["route"].isin(routes), "status"] = "Cancelled"
            df.loc[df["route"].isin(routes), "occupancy_pct"] = 0
            bus_result.data = df

    return sim


def _simulate_weather_emergency(datasets: dict, condition: str, wind_kph: float) -> dict:
    """Return modified datasets dict with worst-case weather values."""
    import copy

    sim = copy.deepcopy(datasets)
    weather_result = sim.get("weather")
    if weather_result and weather_result.success and weather_result.data is not None:
        df = weather_result.data.copy()
        # Override the latest row
        if "timestamp" in df.columns:
            latest_ts = df["timestamp"].max()
            mask = df["timestamp"] == latest_ts
            df.loc[mask, "condition"] = condition
            df.loc[mask, "wind_kph"] = wind_kph
            df.loc[mask, "visibility_km"] = 2.0 if condition in ("Heavy Rain", "Thunderstorm") else 5.0
            df.loc[mask, "humidity_pct"] = 98
            df.loc[mask, "forecast_2h"] = (
                f"Emergency weather: {condition} with {wind_kph} kph winds — "
                "activate shelter protocols and consider evacuation staging."
            )
            weather_result.data = df

    return sim


def render() -> None:
    """Render the Scenario Simulator page."""

    st.markdown(
        '<div class="card-title" style="font-size:1.5rem; margin-bottom:1rem;">🔬 Scenario Simulator</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="card-body" style="margin-bottom:1.5rem;">'
        "Adjust scenario parameters to model operational impacts and receive simulated AI recommendations. "
        "All changes are local to this page — no live data is modified."
        "</div>",
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # Scenario selector
    # -----------------------------------------------------------------------
    scenario = st.selectbox("Select Scenario", _SCENARIO_OPTIONS, index=0)

    datasets = load_all_datasets()

    st.markdown("---")

    # -----------------------------------------------------------------------
    # Scenario 1 — Crowd Surge
    # -----------------------------------------------------------------------
    if scenario == "Crowd Surge":
        st.markdown("#### ⚠️ Crowd Surge Simulation")

        surge_pct = st.slider(
            "Crowd density increase (%)",
            min_value=5,
            max_value=50,
            value=20,
            step=5,
            help="Apply this percentage increase on top of current crowd density.",
        )

        sim_datasets = _simulate_crowd_surge(datasets, surge_pct)

        # Compare before / after
        baseline_result = datasets.get("crowd_levels")
        simulated_result = sim_datasets.get("crowd_levels")

        if (
            baseline_result and baseline_result.success
            and simulated_result and simulated_result.success
        ):
            b_df = baseline_result.data
            s_df = simulated_result.data

            if "timestamp" in b_df.columns and "density_pct" in b_df.columns:
                latest_ts = b_df["timestamp"].max()
                b_latest = b_df[b_df["timestamp"] == latest_ts]
                s_latest = s_df[s_df["timestamp"] == latest_ts]

                b_avg = b_latest["density_pct"].mean()
                s_avg = s_latest["density_pct"].mean()
                b_total = int(b_latest["current_count"].sum())
                s_total = int(s_latest["current_count"].sum())

                cols = st.columns(4)
                with cols[0]:
                    metric_card("Baseline Avg Density", f"{b_avg:.1f}", unit="%")
                with cols[1]:
                    metric_card("Simulated Avg Density", f"{s_avg:.1f}", unit="%", delta=f"+{surge_pct}%")
                with cols[2]:
                    metric_card("Baseline Attendance", f"{b_total:,}")
                with cols[3]:
                    metric_card("Simulated Attendance", f"{s_total:,}", delta=f"+{s_total - b_total:,}")

                # Sections exceeding 90%
                over_90 = s_latest[s_latest["density_pct"] >= 90]
                if len(over_90) > 0:
                    st.markdown("#### Critical Sections (≥90% density)")
                    for _, row in over_90.iterrows():
                        alert_card(
                            severity="Critical",
                            title=str(row.get("section", "Section")),
                            description=f"Projected density: {row['density_pct']:.1f}% — immediate action required.",
                            timestamp=str(row.get("timestamp", "")),
                        )

        # AI recommendations for simulated context
        context = build_stadium_context(sim_datasets)
        recommendations = get_ai_recommendations(context)
        st.markdown("#### Simulated AI Recommendations")
        for i, rec in enumerate(recommendations[:4], 1):
            recommendation_card(title=f"Recommendation {i}", body=rec, confidence=80.0 - i * 3)

    # -----------------------------------------------------------------------
    # Scenario 2 — Transport Failure
    # -----------------------------------------------------------------------
    elif scenario == "Transport Failure":
        st.markdown("#### 🚇 Transport Failure Simulation")

        col_a, col_b = st.columns(2)
        with col_a:
            metro_down = st.slider("Metro lines suspended", 0, 4, 2, step=1)
        with col_b:
            bus_down = st.slider("Bus routes cancelled", 0, 5, 2, step=1)

        sim_datasets = _simulate_transport_failure(datasets, metro_down, bus_down)

        # Show transport status after simulation
        metro_result = sim_datasets.get("metro_status")
        bus_result = sim_datasets.get("bus_status")

        cols = st.columns(2)
        with cols[0]:
            metric_card("Metro Lines Suspended", str(metro_down))
        with cols[1]:
            metric_card("Bus Routes Cancelled", str(bus_down))

        if metro_result and metro_result.success and metro_result.data is not None:
            df = metro_result.data
            if "timestamp" in df.columns:
                latest_ts = df["timestamp"].max()
                latest = df[df["timestamp"] == latest_ts]
                st.markdown("#### Simulated Metro Status")
                for _, row in latest.iterrows():
                    from components import status_badge
                    c1, c2 = st.columns([3, 2])
                    with c1:
                        st.write(f"**{row['line']}**")
                    with c2:
                        status_badge(str(row.get("status", "—")))

        if bus_result and bus_result.success and bus_result.data is not None:
            df = bus_result.data
            if "timestamp" in df.columns:
                latest_ts = df["timestamp"].max()
                latest = df[df["timestamp"] == latest_ts]
                st.markdown("#### Simulated Bus Status")
                for _, row in latest.iterrows():
                    from components import status_badge
                    c1, c2 = st.columns([3, 2])
                    with c1:
                        st.write(f"**{row['route']}**")
                    with c2:
                        status_badge(str(row.get("status", "—")))

        context = build_stadium_context(sim_datasets)
        recommendations = get_ai_recommendations(context)
        st.markdown("#### Simulated AI Recommendations")
        for i, rec in enumerate(recommendations[:4], 1):
            recommendation_card(title=f"Recommendation {i}", body=rec, confidence=78.0 - i * 3)

    # -----------------------------------------------------------------------
    # Scenario 3 — Weather Emergency
    # -----------------------------------------------------------------------
    elif scenario == "Weather Emergency":
        st.markdown("#### ⛈️ Weather Emergency Simulation")

        weather_condition = st.selectbox(
            "Simulated weather condition",
            ["Heavy Rain", "Thunderstorm", "High Winds", "Fog"],
            index=0,
        )
        wind_speed = st.slider("Wind speed (kph)", 30, 120, 60, step=10)

        sim_datasets = _simulate_weather_emergency(datasets, weather_condition, float(wind_speed))

        cols = st.columns(3)
        with cols[0]:
            metric_card("Condition", weather_condition)
        with cols[1]:
            metric_card("Wind Speed", str(wind_speed), unit=" kph")
        with cols[2]:
            metric_card("Visibility", "2.0" if weather_condition in ("Heavy Rain", "Thunderstorm") else "5.0", unit=" km")

        alert_card(
            severity="Critical",
            title=f"Weather Emergency: {weather_condition}",
            description=(
                f"Simulated {weather_condition} conditions at {wind_speed} kph. "
                "Review evacuation procedures, activate shelter protocols, "
                "and coordinate with medical teams for weather-related incidents."
            ),
            timestamp="Simulated",
        )

        context = build_stadium_context(sim_datasets)
        recommendations = get_ai_recommendations(context)
        st.markdown("#### Simulated AI Recommendations")
        for i, rec in enumerate(recommendations[:4], 1):
            recommendation_card(title=f"Recommendation {i}", body=rec, confidence=82.0 - i * 3)
