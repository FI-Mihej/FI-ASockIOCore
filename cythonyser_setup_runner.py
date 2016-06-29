import subprocess
import os
import shlex
from file_system import change_current_dir

"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


def main(setup_script_name):
    dir_of_current_file = os.path.dirname(os.path.abspath(__file__))
    setup_full_file_name = os.path.join(dir_of_current_file, setup_script_name + '.py')

    with change_current_dir(dir_of_current_file):
        run_parameters = 'build_ext --inplace'
        # run_parameters = 'build_ext'
        run_parameters = 'python3 {path} {params}'.format(
            path=setup_full_file_name, params=run_parameters)

        call_result = subprocess.call(shlex.split(run_parameters))
