from xdatbus import xdc_unwrap
import pytest
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
    data_dir = os.path.join(test_dir, "data/xdatcar")

    # Copy all files from the data directory to the temporary directory
    for f in os.listdir(data_dir):
        shutil.copy(os.path.join(data_dir, f), temp_dir)

    # Assuming you have only one .xyz file (or you want to test with the first one you find)
    xdatcar_file = [f for f in os.listdir(temp_dir) if f.endswith('01')][0]

    return os.path.join(temp_dir, xdatcar_file)


def test_f02_xdc_unwrap(setup_test_environment):
    xdc_path = str(setup_test_environment)
    main_tmp_dir = os.path.dirname(xdc_path)

    xdc_unwrap(xdc_path=xdc_path)

    # Assertions
    xyz_unwrap_path = os.path.join(main_tmp_dir, "XDATCAR_01_unwrapped.xyz")

    assert os.path.exists(xyz_unwrap_path), "unwrapped trj file not created"
