import colorama
from check_is_in_pycharm import IS_RUNNING_IN_PYCHARM
from contextlib import contextmanager


"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


@contextmanager
def colorama_init():
    if not IS_RUNNING_IN_PYCHARM:
        colorama.init()

    try:
        yield
    except:
        raise
    finally:
        if not IS_RUNNING_IN_PYCHARM:
            colorama.deinit()
