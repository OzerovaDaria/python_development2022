import venv
from tempfile import TemporaryDirectory
from subprocess import run
from sys import argv

with TemporaryDirectory() as tmpDir:
    venv.create(tmpDir, with_pip=True)
    run(f'{tmpDir}/bin/pip install pyfiglet --quiet --disable-pip-version-check'.split())
    run(['python3', '-m', 'figdate', *(argv[1:])])
