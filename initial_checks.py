import json
import os
import shutil
import sys

from settings import PROJECT_PATH

# settings
SKIP_PATHS = {'.tox', '.ipynb_checkpoints'}
INIT_FORBIDDEN_IN = {'scripts', 'notebooks'}
NOTEBOOKS_ALLOWED_IN = {'notebooks'}

# constants
INIT_FILENAME = '__init__.py'
JUPYTER_NOTEBOOK = '.ipynb'
TERMINAL_WIDTH = shutil.get_terminal_size().columns


def print_header(header):
    print(str.center(header, TERMINAL_WIDTH, '='))


errors = False
inits_in_wrong_places = []
ipynbs_not_in_notebooks = []
ipynbs_with_outputs = []

for path, subdirs, files in os.walk(PROJECT_PATH):
    if any(name in path for name in SKIP_PATHS):
        continue

    for filename in files:
        file_path = os.path.join(path, filename)

        if filename == INIT_FILENAME and any(name in path for name in INIT_FORBIDDEN_IN):
            inits_in_wrong_places.append(file_path)

        if (filename.endswith(JUPYTER_NOTEBOOK) and
                not any(name in path for name in NOTEBOOKS_ALLOWED_IN)):
            ipynbs_not_in_notebooks.append(file_path)

        if filename.endswith(JUPYTER_NOTEBOOK):
            with open(file_path, 'r') as notebook_file:
                notebook = json.load(notebook_file)
            for cell in notebook['cells']:
                if (cell.get('ExecuteTime') is not None or
                        cell.get('execution_count') is not None or
                        cell.get('outputs')):
                    ipynbs_with_outputs.append(file_path)
                    break

if inits_in_wrong_places:
    errors = True
    print_header(' __init__.py in {} '.format(' & '.join(INIT_FORBIDDEN_IN)))
    print('\n'.join(inits_in_wrong_places))

if ipynbs_not_in_notebooks:
    errors = True
    print_header(' Jupyter notebooks not in */{}/ '.format(' & '.join(NOTEBOOKS_ALLOWED_IN)))
    print('\n'.join(ipynbs_not_in_notebooks))

if ipynbs_with_outputs:
    errors = True
    print_header(' Jupyter notebooks with output (use "clear output") '.format(
        ' & '.join(INIT_FORBIDDEN_IN)))
    print('\n'.join(ipynbs_with_outputs))

if errors:
    print('=' * TERMINAL_WIDTH)
    sys.exit(1)
