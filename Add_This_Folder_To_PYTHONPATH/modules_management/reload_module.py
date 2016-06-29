import platform
from importlib import import_module
PYTHON_VERSION = platform.python_version_tuple()  # tuple() of str(); for example: ('3', '5', '1')
if PYTHON_VERSION[0] == '2':
    pass
elif PYTHON_VERSION[0] == '3':
    try:
        from imp import reload
    except ImportError:
        from importlib import reload
else:
    raise ImportError()


"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


def reload_module(module):
    '''
    You SHOULD use construction "import SOME_MODULE" before reload_module() call if construction
        "from SOME_MODULE import SOME_ITEM" was used originally.
    :param module:
    :return:
    '''
    reload(module)


def reload_module_by_text_name(module_name, package=None):
    '''
    :param module_name: Text representation of module name. "os.path" for example.
        See importlib.import_module() in the Python docs
    :param package: see importlib.import_module() in the Python docs
    :return:
    '''
    module = import_module(module_name, package)
    reload(module)
