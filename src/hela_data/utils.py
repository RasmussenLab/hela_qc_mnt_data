import pathlib
from random import sample
from typing import Union


def sample_iterable(iterable: dict, n=10) -> list:
    """Sample some keys from a given dictionary."""
    n_examples_ = n if len(iterable) > n else len(iterable)
    keys = list(iterable)
    sample_ = sample(keys, n_examples_)
    return sample_


def append_to_filepath(filepath: Union[pathlib.Path, str],
                       to_append: str,
                       sep: str = '_',
                       new_suffix: str = None) -> pathlib.Path:
    """Append filepath with specified to_append using a seperator.

    Example: `data.csv` to data_processed.csv
    """
    filepath = pathlib.Path(filepath)
    suffix = filepath.suffix
    if new_suffix:
        suffix = f".{new_suffix}"
    new_fp = filepath.parent / f'{filepath.stem}{sep}{to_append}{suffix}'
    return new_fp
