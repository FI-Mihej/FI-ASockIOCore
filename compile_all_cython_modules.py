import cythonyser_setup_runner

"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


CYTHON_MODULES_SETUP_SCRIPTS_LIST = [
    'setup__dynamic_list_of_pieces',
    'setup__recv_buff_size_computer'
]


def main():
    for module in CYTHON_MODULES_SETUP_SCRIPTS_LIST:
        cythonyser_setup_runner.main(module)


if __name__ == '__main__':
    main()
