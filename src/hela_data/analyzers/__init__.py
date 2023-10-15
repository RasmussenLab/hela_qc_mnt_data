from types import SimpleNamespace


import pandas as pd

__all__ = ['Analysis']


class Analysis(SimpleNamespace):
    pass


def long_format(df: pd.DataFrame,
                colname_values: str = 'intensity',
                ) -> pd.DataFrame:
    names = df.columns.names
    if None in names:
        raise ValueError(f"Column names must not be None: {names}")
    df_long = df.stack(names).to_frame(colname_values)
    return df_long


def wide_format(df: pd.DataFrame,
                columns: str = 'Sample ID',
                name_values: str = 'intensity') -> pd.DataFrame:
    df_wide = df.pivot(columns=columns, values=name_values)
    df_wide = df_wide.T
    return df_wide
