from typing import Literal

import pandas as pd
import plotly.graph_objects as pgo


_time_units = "Run Time (Seconds)"
_motor_velocity_units = "Inches per Second"


Phase = Literal["RampUp", "RampDown", "ReturnToZero"]


# Plot settings for different phases of calibration
_phase_map: dict[Phase, dict] = {
    "RampUp": {"color": "rgba(255, 0, 0, 0.1)", "title": "Ramp Up"},
    "RampDown": {"color": "rgba(0, 255, 0, 0.1)", "title": "Ramp Down"},
    "ReturnToZero": {"color": "rgba(0, 0, 255, 0.1)", "title": "Return to Zero"},
}


def _get_phase_color(phase: Phase) -> str:
    phase_settings = _phase_map.get(phase)
    return phase_settings["color"] if phase_settings else "rgba(150,150,150,0.1)"


def _get_phase_title(phase: Phase) -> str:
    phase_settings = _phase_map.get(phase)
    return phase_settings["title"] if phase_settings else phase


def _add_phase_shading(figure: pgo.Figure, fitting_data: pd.DataFrame):
    """Add shading for the phases (ramp up, ramp down, return to zero) to the given figure"""
    # Assign distinct colors for phases
    for phase, group in fitting_data.groupby("phase"):
        x_start = group["timestamp"].min()
        x_end = group["timestamp"].max()

        figure.add_vrect(
            x0=x_start,
            x1=x_end,
            fillcolor=_get_phase_color(phase),
            layer="below",
            line_width=0,
            annotation_text=_get_phase_title(phase),
            annotation_position="top",
        )


def get_chart_of_voltage_impact_on_motors(log_data: pd.DataFrame, chart_title: str) -> pgo.Figure:
    # Visualize the voltage impact on motors
    chart = pgo.Figure()
    # Add left motor rate
    chart.add_trace(
        pgo.Scatter(
            name="Left Motor Rate",
            x=log_data["timestamp"],
            y=log_data["left_motor_rate"],
            mode="lines",
        )
    )
    chart.add_trace(
        pgo.Scatter(
            name="Right Motor Rate",
            x=log_data["timestamp"],
            y=log_data["right_motor_rate"],
            mode="lines",
        )
    )
    chart.add_trace(
        pgo.Scatter(
            name="Voltage",
            x=log_data["timestamp"],
            y=log_data["voltage"],
            mode="lines",
            yaxis="y2",
        )
    )
    _add_phase_shading(chart, log_data)
    chart.update_layout(
        title=chart_title,
        xaxis={"title": _time_units},
        yaxis={"title": _motor_velocity_units},
        yaxis2={
            "title": "Voltage",
            "overlaying": "y",
            "side": "right",
        },
    )
    return chart


def get_chart_of_actual_vs_predicted_voltage(
    fitting_data: pd.DataFrame, velocity_column_name: str, chart_title: str
) -> pgo.Figure:
    # Visualize the voltage impact on motors
    chart = pgo.Figure()
    chart.add_trace(
        pgo.Scatter(
            name="Motor Rate",
            x=fitting_data["timestamp"],
            y=fitting_data[velocity_column_name],
            mode="lines",
        )
    )
    chart.add_trace(
        pgo.Scatter(
            name="Actual Voltage",
            x=fitting_data["timestamp"],
            y=fitting_data["voltage"],
            mode="lines",
            yaxis="y2",
        )
    )
    chart.add_trace(
        pgo.Scatter(
            name="Predicted Voltage",
            x=fitting_data["timestamp"],
            y=fitting_data["left_motor_predicted_voltage"],
            mode="lines",
            yaxis="y2",
        )
    )
    _add_phase_shading(chart, fitting_data)
    chart.update_layout(
        title=chart_title,
        xaxis={"title": _time_units},
        yaxis={"title": _motor_velocity_units},
        yaxis2={
            "title": "Voltage",
            "overlaying": "y",
            "side": "right",
        },
    )
    return chart
