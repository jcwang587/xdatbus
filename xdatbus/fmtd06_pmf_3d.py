"""project 3d free energy surface to 2d"""

import numpy as np


def pmf_321(fes3d, axis1, axis2):
    """project 3d free energy surface to 1d

    Parameters
    ----------
    fes3d : np.ndarray
        The 3d free energy surface.
    axis1 : int
        The axis to be projected.
    axis2 : int
        The axis to be projected.

    Returns
    -------
    np.ndarray
        The 2d free energy surface.
    """

    fes2d = np.sum(fes3d, axis=axis1)
    fes2d = np.sum(fes2d, axis=axis2)

    return fes2d


