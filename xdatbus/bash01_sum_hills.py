import subprocess
import os


def sum_hill():
    current_dir = os.path.dirname(__file__)
    script_path = os.path.join(current_dir, './resources', 'sum_hills.sh')
    subprocess.run(['bash', script_path])
