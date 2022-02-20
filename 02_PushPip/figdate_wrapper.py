import venv
import shutil
import tempfile
import subprocess

form = '%Y %d %b, %A'
shr = 'graceful'
tmpd = tempfile.mkdtemp()
venv.create(tmpd , with_pip=True)
subprocess.run([tmpd + '/bin/pip', 'install', 'pyfiglet'], capture_output=True)
subprocess.run([tmpd + '/bin/python3', '-m', 'figdate', form, shr])
shutil.rmtree(tmpd)

