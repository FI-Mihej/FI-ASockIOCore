from distutils.core import setup
from Cython.Build import cythonize


"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


setup(
    name = 'dynamic_list_of_pieces module',
    ext_modules = cythonize("./Add_This_Folder_To_PYTHONPATH/data_containers/dynamic_list_of_pieces/dynamic_list_of_pieces__cython.pyx"),
)
