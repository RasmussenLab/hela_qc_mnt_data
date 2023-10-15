from random import sample


def sample_iterable(iterable: dict, n=10) -> list:
    """Sample some keys from a given dictionary."""
    n_examples_ = n if len(iterable) > n else len(iterable)
    keys = list(iterable)
    sample_ = sample(keys, n_examples_)
    return sample_
