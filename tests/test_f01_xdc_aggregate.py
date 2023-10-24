import os
import shutil
from xdatbus import xdc_aggregate
import pytest
from ase.io import read


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

    return temp_dir


def test_f01_xdc_aggregate(setup_test_environment):
    xdc_dir = str(setup_test_environment)
    main_tmp_dir = os.path.dirname(xdc_dir)

    xdc_aggregate(xdc_dir=xdc_dir, output_path=main_tmp_dir)

    # Assertions
    xdatbus_path = os.path.join(main_tmp_dir, "XDATBUS")
    assert os.path.exists(xdatbus_path), "XDATBUS file not created"

    # Load the aggregated data
    aggregated_data = read(xdatbus_path, format='vasp-xdatcar', index=':')

    # Check the aggregation result against one of the files in the temporary directory
    assert len(aggregated_data) >= len(
        read(os.path.join(xdc_dir, "XDATCAR_01"), format='vasp-xdatcar', index=':'))
