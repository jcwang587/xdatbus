from xdatbus import neb_2d, local_minima
import pytest
import numpy as np
import os
import shutil


@pytest.fixture
def setup_test_environment(tmp_path, request):
    # Get the name of the test function
    test_name = request.node.name

    # Use tmp_path for the test directory
    temp_dir = tmp_path / test_name
    temp_dir.mkdir()

    # Get the directory of the current test file
    test_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the test data directory
    data_dir = os.path.join(test_dir, "data/npy")

    # Copy all files from the data directory to the temporary directory
    for f in os.listdir(data_dir):
        shutil.copy(os.path.join(data_dir, f), temp_dir)

    fes_file = [f for f in os.listdir(temp_dir) if f.endswith("_2d.npy")][0]

    return os.path.join(temp_dir, fes_file)


def test_fmtd07_neb(setup_test_environment):
    fes_path = str(setup_test_environment)

    fes = np.load(fes_path)

    local_minima_coords = local_minima(fes)
    n_images = 10
    n_steps = 1000
    spring_constant = 0.2

    mep_13, mep_fes_13 = neb_2d(
        fes,
        local_minima_coords[1],
        local_minima_coords[3],
        n_images,
        n_steps,
        spring_constant,
    )

    assert len(mep_13) == n_images, "Number of images in the path is not correct"
    assert max(mep_fes_13) - min(mep_fes_13) > 0, "Path FES is not correct"
