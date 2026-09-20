import pandas as pd
import plotly.graph_objects as pgo


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
    chart.update_layout(
        title=chart_title,
        xaxis={"title": "Run Time (Seconds)"},
        yaxis={"title": "Inches per second"},
        yaxis2={
            "title": "Voltage",
            "overlaying": "y",
            "side": "right",
        },
    )
    return chart
