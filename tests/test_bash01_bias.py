import os
import shutil
from xdatbus import sum_hills
import pytest


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
    data_dir = os.path.join(test_dir, "data/hills")

    # Copy all files from the data directory to the temporary directory
    for f in os.listdir(data_dir):
        shutil.copy(os.path.join(data_dir, f), temp_dir)

    # Assuming you have only one .xyz file (or you want to test with the first one you find)
    hills_file = [f for f in os.listdir(temp_dir) if f.endswith('HILLS')][0]

    return os.path.join(temp_dir, hills_file)


def test_bash01_bias(setup_test_environment):
    hills_dir = str(setup_test_environment)
    main_tmp_dir = os.path.dirname(hills_dir)

    sum_hills(plumed_hills=hills_dir, plumed_outfile="fes_bias.dat", plumed_min=0.0, plumed_max=11.636, plumed_bin=100)



