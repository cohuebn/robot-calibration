from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class DrivetrainFeedForwardFittingResults:
    """The results of fitting the feed-forward equation to our measured results"""

    kS: float
    kV: float


def fit_feedforward(voltage_series: pd.Series, velocity_series: pd.Series):
    """
    Estimate Ks and Kv from motor measurements. Note: for this exercise,
    acceleration is currently excluded, so kA is also excluded from the fitting equation.
    If acceleration is needed later, it will need to be measured and accounted for. However,
    it is optional in the feed-forward model
    See: https://docs.wpilib.org/en/stable/docs/software/advanced-controls/controllers/feedforward.html#simplemotorfeedforward

    Arguments:
      voltage_series (pd.Series): A series of applied motor voltages (V)
      velocity_series (pd.Series): motor velocities; measured using units defined on encoder
    """

    voltages = voltage_series.to_numpy()
    velocities = velocity_series.to_numpy()

    voltages = np.asarray(voltages, dtype=float)
    velocities = np.asarray(velocities, dtype=float)

    X = np.column_stack(
        [
            np.sign(velocities),
            velocities,
        ]
    )

    constants, *_ = np.linalg.lstsq(X, voltages, rcond=None)
    kS, kV = constants
    return DrivetrainFeedForwardFittingResults(kS, kV)


def get_fitted_voltage_predictions(velocities: pd.Series, kS: float, kV: float) -> pd.Series:
    """Get a series of the predicted voltage given the provided velocities and feed-forward equation
    kS and kV values"""
    return kS * np.sign(velocities) + kV * velocities
