import subprocess
import os


def sum_hill():
    current_dir = os.path.dirname(__file__)
    script_path = os.path.join(current_dir, './resources', 'your_script.sh')
    subprocess.run(['bash', script_path])
