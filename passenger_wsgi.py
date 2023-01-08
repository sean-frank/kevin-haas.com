import os
import sys


INTERP = os.path.join(os.path.abspath('.'), 'venv/bin/python3')
if sys.executable != INTERP:
        os.execl(INTERP, INTERP, *sys.argv)

cwd = os.path.abspath('.')
# Project must be in the following directory or
# we can't import it from the last line.
sys.path.append(cwd)

# Uncomment below if your project is in a
# subdirectory named src/.
# sys.path.append(os.path.join(cwd, 'src'))

# Add the virtual environment
sys.path.insert(0, os.path.join(cwd, 'venv/bin'))
sys.path.insert(0, os.path.join(cwd, 'venv/lib/python3.9/site-packages/'))


from kevin_haas_com import app as application
