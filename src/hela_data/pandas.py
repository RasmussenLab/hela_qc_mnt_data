import collections.abc
import typing
from typing import Iterable
from types import SimpleNamespace
import numbers

import omegaconf
import numpy as np
import pandas as pd


def combine_value_counts(X: pd.DataFrame, dropna=True) -> pd.DataFrame:
    """Pass a selection of columns to combine it's value counts.

    This performs no checks. Make sure the scale of the variables
    you pass is comparable.

    Parameters
    ----------
    X : pandas.DataFrame
        A DataFrame of several columns with values in a similar range.
    dropna : bool, optional
        Exclude NA values from counting, by default True

    Returns
    -------
    pandas.DataFrame
        DataFrame of combined value counts.
    """
    """
    """
    _df = pd.DataFrame()
    for col in X.columns:
        _df = _df.join(X[col].value_counts(dropna=dropna), how='outer')
    freq_targets = _df.sort_index()
    return freq_targets


def create_dict_of_dicts(d: dict, verbose=False,
                         # maybe this should not be here...
                         transform_values: typing.Union[typing.Callable, numbers.Number] = None):
    """Unpack a dictionary with tuple keys to a nested dictonary
    of single tuple keys.
    """
    ret = dict()
    for keys, v in d.items():
        if verbose:
            print(f"current key: {str(keys):90}: {len(v):>5}")
        current_dict = ret
        for k in keys[:-1]:
            if k not in current_dict:
                current_dict[k] = dict()
            current_dict = current_dict[k]
        last_key = keys[-1]
        if last_key not in current_dict:
            current_dict[last_key] = transform_values(
                v) if transform_values else v
        else:
            raise KeyError(f"Key already in dict: {last_key}")
    return ret


def _add_indices(array: np.array, original_df: pd.DataFrame,
                 index_only: bool = False) -> pd.DataFrame:
    index = original_df.index
    columns = None
    if not index_only:
        columns = original_df.columns
    return pd.DataFrame(array, index=index, columns=columns)


def flatten_dict_of_dicts(d: dict, parent_key: str = '') -> dict:
    """Build tuples for nested dictionaries for use as `pandas.MultiIndex`.

    Parameters
    ----------
    d : dict
        Nested dictionary for which all keys are flattened to tuples.
    parent_key : str, optional
        Outer key (used for recursion), by default ''

    Returns
    -------
    dict
        Flattend dictionary with tuple keys: {(outer_key, ..., inner_key) : value}
    """
    # simplified and adapted from: https://stackoverflow.com/a/6027615/9684872
    items = []
    for k, v in d.items():
        new_key = parent_key + (k,) if parent_key else (k,)
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten_dict_of_dicts(v, parent_key=new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)


def counts_with_proportion(s: pd.Series) -> pd.DataFrame:
    """Counts with proportion of counts(!).

    Note: In case of missing values the proportion is not based on the total number of
    rows in the DataFrame.
    """
    s = s.value_counts()
    s.index.name = 'value'
    N = s.sum()
    ret = s.to_frame('counts')
    ret['prop.'] = s / N
    return ret


def unique_cols(s: pd.Series) -> bool:
    """Check all entries are equal in pandas.Series

    Ref: https://stackoverflow.com/a/54405767/968487

    Parameters
    ----------
    s : pandas.Series
        Series to check uniqueness

    Returns
    -------
    bool
        Boolean on if all values are equal.
    """
    return (s.iloc[0] == s).all()


def show_columns_with_variation(df: pd.DataFrame) -> pd.DataFrame:
    df_describe = df.describe(include='all')
    col_mask = (df_describe.loc['unique'] > 1) | (
        df_describe.loc['std'] > 0.01)
    return df.loc[:, col_mask]


def get_unique_non_unique_columns(df: pd.DataFrame) -> SimpleNamespace:
    """Get back a namespace with an column.Index both
    of the unique and non-unique columns.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    types.SimpleNamespace
        SimpleNamespace with `unique` and `non_unique` column names indices.
    """

    mask_unique_columns = df.apply(unique_cols)

    columns = SimpleNamespace()
    columns.unique = df.columns[mask_unique_columns]
    columns.non_unique = df.columns[~mask_unique_columns]
    return columns


def prop_unique_index(df: pd.DataFrame) -> pd.DataFrame:
    counts = df.index.value_counts()
    prop = (counts > 1).sum() / len(counts)
    return 1 - prop


def replace_with(string_key: str, replace: str = "()/", replace_with: str = '') -> str:
    for symbol in replace:
        string_key = string_key.replace(symbol, replace_with)
    return string_key


def index_to_dict(index: pd.Index) -> dict:
    cols = {replace_with(col.replace(' ', '_').replace(
        '-', '_')): col for col in index}
    return cols


def get_columns_accessor(df: pd.DataFrame, all_lower_case=False) -> omegaconf.OmegaConf:
    if isinstance(df.columns, pd.MultiIndex):
        raise ValueError("MultiIndex not supported.")
    cols = index_to_dict(df.columns)
    if all_lower_case:
        cols = {k.lower(): v for k, v in cols.items()}
    return omegaconf.OmegaConf.create(cols)


def get_columns_accessor_from_iterable(cols: Iterable[str],
                                       all_lower_case=False) -> omegaconf.OmegaConf:
    cols = index_to_dict(cols)
    if all_lower_case:
        cols = {k.lower(): v for k, v in cols.items()}
    return omegaconf.OmegaConf.create(cols)


def select_max_by(df: pd.DataFrame, grouping_columns: list, selection_column: str) -> pd.DataFrame:
    df = df.sort_values(by=[*grouping_columns, selection_column], ascending=False)
    df = df.drop_duplicates(subset=grouping_columns,
                            keep='first')
    return df


def length(x):
    """Len function which return 0 if object (probably np.nan) has no length.
    Otherwise return length of list, pandas.Series, numpy.array, dict, etc."""
    try:
        return len(x)
    except BaseException:
        return 0
