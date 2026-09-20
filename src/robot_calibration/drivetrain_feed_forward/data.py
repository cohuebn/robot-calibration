import pandas as pd
from scipy.signal import savgol_filter


def read_logs(log_filename: str, max_time: float | None = None) -> pd.DataFrame:
    """Read WPI logs and get relevant measures for drivetrain feed-forward calibration

    Arguments
        log_filename (str): The filename to get WPI logs from
        max_time (float | None): The maximum time (in seconds from start) to get log data for. If not provided,
            all logs will be retrieved
    """
    relevant_columns = {
        "Timestamp": "timestamp",
        "NT:/SmartDashboard/Drivetrain Calibration/phase": "phase",
        "NT:/SmartDashboard/Drivetrain Calibration/voltage": "voltage",
        "NT:/SmartDashboard/Drivetrain Calibration/leftMotorRate": "left_motor_rate",
        "NT:/SmartDashboard/Drivetrain Calibration/leftMotorStaticFrictionOvercome": "left_motor_static_friction_overcome",
        "NT:/SmartDashboard/Drivetrain Calibration/rightMotorRate": "right_motor_rate",
        "NT:/SmartDashboard/Drivetrain Calibration/rightMotorStaticFrictionOvercome": "right_motor_static_friction_overcome",
        "NT:/SmartDashboard/Drivetrain Calibration/targetVoltage": "targetVoltage",
    }
    df = pd.read_csv(log_filename)
    # Rename relevant columns; drop any rows without a "phase" column
    df = df.rename(columns=relevant_columns).dropna(subset=["phase", "left_motor_rate", "right_motor_rate"])
    # Return only the relevant columns
    relevant_data = df[list(relevant_columns.values())].sort_values(by="timestamp")
    return relevant_data if max_time is None else relevant_data[relevant_data["timestamp"] <= max_time]


def _remove_noise(series: pd.Series) -> pd.Series:
    return savgol_filter(series, window_length=31, polyorder=2)


def remove_noise_from_motor_rates(log_data: pd.DataFrame) -> pd.DataFrame:
    """The motor encoders have some noise in them evident from spikes that don't follow the general encoder
    rate trajectories. This method updates the encoder rate columns to smooth out the noise while
    retaining the original motor rates in 'raw' columns (e.g. 'raw_left_motor_rate')"""
    smoothed_log_data = log_data.copy()
    smoothed_log_data["raw_left_motor_rate"] = smoothed_log_data["left_motor_rate"]
    smoothed_log_data["raw_right_motor_rate"] = smoothed_log_data["right_motor_rate"]
    smoothed_log_data["left_motor_rate"] = _remove_noise(smoothed_log_data["raw_left_motor_rate"])
    smoothed_log_data["right_motor_rate"] = _remove_noise(smoothed_log_data["raw_right_motor_rate"])
    return smoothed_log_data
