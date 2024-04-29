"""In many cases you might decide which variable should be analyzed after having performed a metadynamics simulation.
For example, you might want to calculate the free energy as a function of CVs other than those biased during the
metadynamics simulation. At variance with standard MD simulations, you cannot simply calculate histograms of other
variables directly from your metadynamics trajectory, because the presence of the metadynamics bias potential has
altered the statistical weight of each frame. To remove the effect of this bias and thus be able to calculate properties
of the system in the unbiased ensemble, you must reweight (unbias) your simulation."""

import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess


def reweight(fes, cv, nv, kb, t, grid_min, grid_max, grid_num):
    """Reweight a metadynamics simulation to the unbiased ensemble using histogram reweighting.

        Parameters
        ----------
        fes : np.ndarray
            The free energy surface calculated from the metadynamics simulation.
        cv : np.ndarray
            The collective variable used in the metadynamics simulation.
        nv : np.ndarray
            The new collective variable for which the potential of mean force will be calculated.
        kb : float
            The Boltzmann constant.
        t : float
            The temperature of the simulation.
        grid_min : float
            The minimum value of the collective variable.
        grid_max : float
            The maximum value of the collective variable.
        grid_num : int
            The number of bins in the histogram.

    Returns
    -------
    np.ndarray
        The unbiased free energy surface.
    """
    fes_flat = fes.flatten()
    cv_hist = np.exp(-fes_flat / (kb * t))

    nv_bins = np.linspace(grid_min, grid_max, grid_num)
    nv_hist = np.zeros(len(nv_bins) - 1)

    for i in range(len(nv)):
        for j in range(len(cv_hist)):
            if nv_bins[i] <= nv[j] < nv_bins[i + 1]:
                nv_hist[i] += cv_hist[j]

    nv_hist = nv_hist / np.sum(nv_hist)

    pmf = -kb * t * np.log(nv_hist)
    pmf -= np.min(pmf)

    pmf_smooth = lowess(pmf, nv_bins, frac=0.1, return_sorted=False)

    return pmf_smooth

