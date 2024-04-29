"""In many cases you might decide which variable should be analyzed after having performed a metadynamics simulation.
For example, you might want to calculate the free energy as a function of CVs other than those biased during the
metadynamics simulation. At variance with standard MD simulations, you cannot simply calculate histograms of other
variables directly from your metadynamics trajectory, because the presence of the metadynamics bias potential has
altered the statistical weight of each frame. To remove the effect of this bias and thus be able to calculate properties
of the system in the unbiased ensemble, you must reweight (unbias) your simulation."""

import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess


def reweighting(fes, cv, kb, t):
    """Reweight a metadynamics simulation to the unbiased ensemble using histogram reweighting.

        Parameters
        ----------
        fes : np.ndarray
            The free energy surface calculated from the metadynamics simulation.
        cv : np.ndarray
            The collective variable used in the metadynamics simulation.
        kb : float
            The Boltzmann constant.
        t : float
            The temperature of the simulation.

    Returns
    -------
    np.ndarray
        The unbiased free energy surface.
    """
    # Calculate the bias potential
    bias = -kb * t * np.log(np.exp(-fes / (kb * t)).sum())

    # Calculate the unbiased free energy surface
    fes_unbiased = fes + bias

    # Calculate the unbiased probability distribution
    prob = np.exp(-fes_unbiased / (kb * t))
    prob /= prob.sum()

    # Calculate the unbiased free energy surface
    fes_unbiased = -kb * t * np.log(prob)

    return fes_unbiased
