import os
import shutil
from xdatbus import f01_aggregate
import pytest
from ase.io import read


@pytest.fixture
def setup_test_environment(tmp_path):
    # Use tmp_path for the test directory
    temp_dir = tmp_path / "test_aimd_path"
    temp_dir.mkdir()

    # Get the directory of the current test file
    test_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the test data directory
    data_dir = os.path.join(test_dir, "data")

    # Copy all files from the data directory to the temporary directory
    for f in os.listdir(data_dir):
        shutil.copy(os.path.join(data_dir, f), temp_dir)

    return temp_dir


def test_f01_aggregate(setup_test_environment):
    aimd_path = str(setup_test_environment)
    main_tmp_dir = os.path.dirname(aimd_path)

    f01_aggregate(aimd_path=aimd_path, output_path=main_tmp_dir)

    # Assertions
    xdatbus_path = os.path.join(main_tmp_dir, "XDATBUS")
    assert os.path.exists(xdatbus_path), "XDATBUS file not created"

    # Load the aggregated data
    aggregated_data = read(xdatbus_path, format='vasp-xdatcar', index=':')

    # Check the aggregation result against one of the files in the temporary directory
    assert len(aggregated_data) >= len(
        read(os.path.join(aimd_path, "XDATCAR_01"), format='vasp-xdatcar', index=':'))
