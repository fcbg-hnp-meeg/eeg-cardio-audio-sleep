import numpy as np
from numpy.typing import ArrayLike

from ._checks import _check_type


def match_positions(x: ArrayLike, y: ArrayLike, threshold: int):
    """Match the peaks from x and y, 2 by 2.

    Return indices from X and Y that are closer than a threshold distance.
    Assumes one element from X matches one and only one element from Y.

    Parameters
    ----------
    x : array
        Array of positions (in samples, ints).
    y : array
        Array of positions (in samples, ints).
    threshold : int
        Distance threshold in samples.

    Returns
    -------
    idx : array
        Indices from positions in X close to a position in Y.
    idy : array
        Indices from positions in Y close to a position in X.
    """
    _check_type(x, (list, tuple, np.ndarray), "x")
    _check_type(y, (list, tuple, np.ndarray), "y")
    _check_type(threshold, ("int",), "threshold")
    x = np.array(x)
    y = np.array(y)
    if threshold <= 0:
        raise ValueError(
            "Argument 'threshold' must be a strictly positive integer. "
            f"Provided: '{threshold}'."
        )

    d = np.repeat(x, y.shape[0]).reshape(x.shape[0], y.shape[0])
    d -= y
    idx, idy = np.where((-threshold < d) & (d < threshold))
    assert idx.shape == idy.shape  # sanity-check

    return idx, idy
