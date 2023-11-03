import numpy as np

try:
    import biotite
    BIOTITE_AVAILABLE = True
except ImportError:
    load_structure = None
    BIOTITE_AVAILABLE = False

