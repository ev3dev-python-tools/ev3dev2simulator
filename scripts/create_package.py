import subprocess
import os
from pathlib import Path


def main():
    ev3_dir = Path(__file__).resolve().parent.parent
    os.chdir(ev3_dir)
    subprocess.call(['python', 'setup.py', 'bdist_wheel', '-d', 'pypi'])


if __name__ == '__main__':
    main()
