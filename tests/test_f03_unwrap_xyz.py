from xdatbus import xyz_unwrap
import pytest
import os
import shutil


@pytest.fixture
def setup_test_environment(tmp_path):
    # Use tmp_path for the test directory
    temp_dir = tmp_path / "test_aimd_path"
    temp_dir.mkdir()

    # Get the directory of the current test file
    test_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the test data directory
    data_dir = os.path.join(test_dir, "data/xdatcar")

    # Copy all files from the data directory to the temporary directory
    for f in os.listdir(data_dir):
        shutil.copy(os.path.join(data_dir, f), temp_dir)

    return temp_dir


def test_f03_unwrap(setup_test_environment):
    lattice = [13.859, 17.42, 15.114]

    xyz_unwrap('data/xyz/trj.xyz', lattice)
    assert os.path.exists('data/xyz/trj_unwrapped.xyz'), "XDATBUS file not created"





