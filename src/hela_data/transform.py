import pandas as pd
import numpy as np


def log(row: pd.Series):
    """Apply log Transformation to values setting zeros to NaN."""
    return np.log(row.where(row != 0.0))
