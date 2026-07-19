"""
pages/mission_control.py — Mission Control Page

Real-time operational dashboard displaying:
  - Crowd density by section (bar chart + KPIs)
  - Gate occupancy status table
  - Transport status (metro + bus)
  - Parking utilisation (bar chart)
  - Weather timeline
  - Security alert feed
"""

import streamlit as st

from components import (
    metric_card,
    status_badge,
    alert_card,
    chart_container,
)
from utils.data_loader import load_all_datasets
from utils.chart_theme import (
    apply_theme,
    CHART_COLORS,
    COLOR_SUCCESS,
    COLOR_WARNING,
    COLOR_DANGER,
)


def _crowd_chart(df):
    """Return a Plotly bar chart of current crowd density by section."""
    try:
        import plotly.graph_objects as go
    except ImportError:
        return None

    if "timestamp" not in df.columns or "density_pct" not in df.columns:
        return None

    latest_ts = df["timestamp"].max()
    latest = df[df["timestamp"] == latest_ts].copy()
    latest = latest.sort_values("density_pct", ascending=False)

    colors = []
    for pct in latest["density_pct"]:
        if pct >= 85:
            colors.append(COLOR_DANGER)
        elif pct >= 70:
            colors.append(COLOR_WARNING)
        else:
            colors.append(COLOR_SUCCESS)

    fig = go.Figure(
        go.Bar(
            x=latest["section"],
            y=latest["density_pct"],
            marker_color=colors,
            text=[f"{v:.0f}%" for v in latest["density_pct"]],
            textposition="outside",
        )
    )
    fig.update_layout(
        yaxis=dict(range=[0, 110], title="Density %"),
        xaxis_title="Section",
        showlegend=False,
    )
    return apply_theme(fig)


def _parking_chart(df):
    """Return a Plotly bar chart of parking utilisation by zone at the latest timestamp."""
    try:
        import plotly.graph_objects as go
    except ImportError:
        return None

    if "timestamp" not in df.columns or "utilization_pct" not in df.columns:
        return None

    latest_ts = df["timestamp"].max()
    latest = df[df["timestamp"] == latest_ts].copy()

    colors = []
    for pct in latest["utilization_pct"]:
        if pct >= 90:
            colors.append(COLOR_DANGER)
        elif pct >= 75:
            colors.append(COLOR_WARNING)
        else:
            colors.append(COLOR_SUCCESS)

    fig = go.Figure(
        go.Bar(
            x=latest["zone"],
            y=latest["utilization_pct"],
            marker_color=colors,
            text=[f"{v:.0f}%" for v in latest["utilization_pct"]],
            textposition="outside",
        )
    )
    fig.update_layout(
        yaxis=dict(range=[0, 110], title="Utilisation %"),
        xaxis_title="Zone",
        showlegend=False,
    )
    return apply_theme(fig)


def render() -> None:
    """Render the Mission Control page."""

    st.markdown(
        '<div class="card-title" style="font-size:1.5rem; margin-bottom:1.5rem;">🎛️ Mission Control</div>',
        unsafe_allow_html=True,
    )

    datasets = load_all_datasets()

    # -----------------------------------------------------------------------
    # Tab layout
    # -----------------------------------------------------------------------
    tab_crowd, tab_gates, tab_transport, tab_parking, tab_weather, tab_security = st.tabs(
        ["Crowd", "Gates", "Transport", "Parking", "Weather", "Security"]
    )

    # -----------------------------------------------------------------------
    # Tab: Crowd
    # -----------------------------------------------------------------------
    with tab_crowd:
        crowd_result = datasets.get("crowd_levels")
        if crowd_result and crowd_result.success and crowd_result.data is not None:
            df = crowd_result.data

            # KPI row
            if "timestamp" in df.columns and "current_count" in df.columns and "density_pct" in df.columns:
                latest_ts = df["timestamp"].max()
                latest = df[df["timestamp"] == latest_ts]
                total = int(latest["current_count"].sum())
                avg_density = latest["density_pct"].mean()
                max_density = latest["density_pct"].max()
                max_section = latest.loc[latest["density_pct"].idxmax(), "section"]

                cols = st.columns(3)
                with cols[0]:
                    metric_card("Total Attendance", f"{total:,}")
                with cols[1]:
                    metric_card("Avg Density", f"{avg_density:.1f}", unit="%")
                with cols[2]:
                    metric_card("Peak Section", max_section, unit=f" ({max_density:.0f}%)")

            chart_container(_crowd_chart(df), "Crowd Density by Section")
        else:
            st.warning("Crowd data unavailable.")

    # -----------------------------------------------------------------------
    # Tab: Gates
    # -----------------------------------------------------------------------
    with tab_gates:
        gate_result = datasets.get("gate_occupancy")
        if gate_result and gate_result.success and gate_result.data is not None:
            df = gate_result.data
            if "timestamp" in df.columns:
                latest_ts = df["timestamp"].max()
                latest = df[df["timestamp"] == latest_ts].copy()

                open_count = len(latest[latest["status"] == "Open"])
                congested_count = len(latest[latest["status"] == "Congested"])
                closed_count = len(latest[latest["status"] == "Closed"])

                cols = st.columns(3)
                with cols[0]:
                    metric_card("Open Gates", str(open_count))
                with cols[1]:
                    metric_card("Congested Gates", str(congested_count))
                with cols[2]:
                    metric_card("Closed Gates", str(closed_count))

                st.markdown("#### Gate Status")
                for _, row in latest.iterrows():
                    c1, c2, c3 = st.columns([2, 1, 2])
                    with c1:
                        st.write(f"**{row['gate_id']}**")
                    with c2:
                        status_badge(row["status"])
                    with c3:
                        occ = row.get("occupancy_pct", 0)
                        queue = row.get("queue_length", 0)
                        st.write(f"{occ:.0f}% occupancy · {queue} in queue")
        else:
            st.warning("Gate data unavailable.")

    # -----------------------------------------------------------------------
    # Tab: Transport
    # -----------------------------------------------------------------------
    with tab_transport:
        metro_result = datasets.get("metro_status")
        bus_result = datasets.get("bus_status")

        st.markdown("#### Metro Lines")
        if metro_result and metro_result.success and metro_result.data is not None:
            df = metro_result.data
            if "timestamp" in df.columns:
                latest_ts = df["timestamp"].max()
                latest = df[df["timestamp"] == latest_ts]
                for _, row in latest.iterrows():
                    c1, c2, c3 = st.columns([3, 1, 2])
                    with c1:
                        st.write(f"**{row['line']}**")
                    with c2:
                        status_badge(row["status"])
                    with c3:
                        delay = row.get("delay_minutes", 0)
                        next_arr = row.get("next_arrival", "—")
                        if delay > 0:
                            st.write(f"+{delay} min delay · Next: {next_arr}")
                        else:
                            st.write(f"On time · Next: {next_arr}")
        else:
            st.warning("Metro data unavailable.")

        st.markdown("#### Bus Routes")
        if bus_result and bus_result.success and bus_result.data is not None:
            df = bus_result.data
            if "timestamp" in df.columns:
                latest_ts = df["timestamp"].max()
                latest = df[df["timestamp"] == latest_ts]
                for _, row in latest.iterrows():
                    c1, c2, c3 = st.columns([3, 1, 2])
                    with c1:
                        st.write(f"**{row['route']}**")
                    with c2:
                        status_badge(row["status"])
                    with c3:
                        occ = row.get("occupancy_pct", 0)
                        delay = row.get("delay_minutes", 0)
                        delay_str = f" · +{delay} min" if delay > 0 else ""
                        st.write(f"{occ:.0f}% full{delay_str}")
        else:
            st.warning("Bus data unavailable.")

    # -----------------------------------------------------------------------
    # Tab: Parking
    # -----------------------------------------------------------------------
    with tab_parking:
        parking_result = datasets.get("parking")
        if parking_result and parking_result.success and parking_result.data is not None:
            df = parking_result.data

            if "timestamp" in df.columns and "utilization_pct" in df.columns and "available_spaces" in df.columns:
                latest_ts = df["timestamp"].max()
                latest = df[df["timestamp"] == latest_ts]
                avg_util = latest["utilization_pct"].mean()
                total_avail = int(latest["available_spaces"].sum())

                cols = st.columns(2)
                with cols[0]:
                    metric_card("Avg Utilisation", f"{avg_util:.0f}", unit="%")
                with cols[1]:
                    metric_card("Available Spaces", f"{total_avail:,}")

            chart_container(_parking_chart(df), "Parking Utilisation by Zone")
        else:
            st.warning("Parking data unavailable.")

    # -----------------------------------------------------------------------
    # Tab: Weather
    # -----------------------------------------------------------------------
    with tab_weather:
        weather_result = datasets.get("weather")
        if weather_result and weather_result.success and weather_result.data is not None:
            df = weather_result.data
            if "timestamp" in df.columns:
                latest_ts = df["timestamp"].max()
                row = df[df["timestamp"] == latest_ts].iloc[0]

                cols = st.columns(4)
                with cols[0]:
                    metric_card("Condition", row.get("condition", "—"))
                with cols[1]:
                    metric_card("Temperature", f"{row.get('temperature_c', '—')}", unit="°C")
                with cols[2]:
                    metric_card("Wind", f"{row.get('wind_kph', '—')}", unit=" kph")
                with cols[3]:
                    metric_card("Humidity", f"{row.get('humidity_pct', '—')}", unit="%")

                forecast = row.get("forecast_2h", "")
                if forecast:
                    st.markdown(
                        f'<div class="card"><div class="card-title">2-Hour Forecast</div>'
                        f'<div class="card-body">{forecast}</div></div>',
                        unsafe_allow_html=True,
                    )

                # Temperature trend chart
                try:
                    import plotly.graph_objects as go

                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(
                            x=df["timestamp"],
                            y=df["temperature_c"],
                            mode="lines+markers",
                            name="Temp (°C)",
                            line=dict(color=CHART_COLORS[0]),
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=df["timestamp"],
                            y=df["humidity_pct"],
                            mode="lines",
                            name="Humidity (%)",
                            line=dict(color=CHART_COLORS[3], dash="dot"),
                            yaxis="y2",
                        )
                    )
                    fig.update_layout(
                        yaxis=dict(title="Temperature (°C)"),
                        yaxis2=dict(title="Humidity (%)", overlaying="y", side="right"),
                        xaxis_title="Time",
                        legend=dict(orientation="h", y=1.1),
                    )
                    apply_theme(fig)
                    chart_container(fig, "Temperature & Humidity Timeline")
                except ImportError:
                    pass
        else:
            st.warning("Weather data unavailable.")

    # -----------------------------------------------------------------------
    # Tab: Security
    # -----------------------------------------------------------------------
    with tab_security:
        security_result = datasets.get("security_alerts")
        if security_result and security_result.success and security_result.data is not None:
            df = security_result.data

            # KPI counts
            severity_counts = df["severity"].value_counts() if "severity" in df.columns else {}
            cols = st.columns(4)
            for i, sev in enumerate(["Critical", "High", "Medium", "Low"]):
                with cols[i]:
                    count = int(severity_counts.get(sev, 0))
                    metric_card(sev, str(count))

            st.markdown("#### Recent Alerts")
            display_df = df.head(10) if len(df) > 10 else df
            for _, row in display_df.iterrows():
                alert_card(
                    severity=str(row.get("severity", "Low")),
                    title=str(row.get("title", "Alert")),
                    description=str(row.get("description", "")),
                    timestamp=str(row.get("timestamp", "")),
                )
        else:
            st.warning("Security data unavailable.")
