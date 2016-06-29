from distutils.core import setup
from Cython.Build import cythonize


"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


setup(
    name = 'recv_buff_size_computer module',
    ext_modules = cythonize("./Add_This_Folder_To_PYTHONPATH/simple_network/recv_buff_size_computer/recv_buff_size_computer__cython.pyx"),
)
