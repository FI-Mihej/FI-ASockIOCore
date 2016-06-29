from importlib import import_module
from contextlib import contextmanager


"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


@contextmanager
def alt_import(module_name, package=None):
    module = None
    try:
        module = import_module(module_name, package)
    except ImportError:
        pass

    try:
        yield module
    except ImportError as ex:
        print('IMPORT ERROR: {}'.format(str(ex)))
