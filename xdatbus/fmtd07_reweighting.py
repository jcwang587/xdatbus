"""In many cases you might decide which variable should be analyzed after having performed a metadynamics simulation.
For example, you might want to calculate the free energy as a function of CVs other than those biased during the
metadynamics simulation. At variance with standard MD simulations, you cannot simply calculate histograms of other
variables directly from your metadynamics trajectory, because the presence of the metadynamics bias potential has
altered the statistical weight of each frame. To remove the effect of this bias and thus be able to calculate properties
of the system in the unbiased ensemble, you must reweight (unbias) your simulation."""

import numpy as np
