# from .dynamic_list_of_pieces__cpython import *
try:
    from .dynamic_list_of_pieces__cython import *
except ImportError:
    from .dynamic_list_of_pieces__cpython import *

"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'
