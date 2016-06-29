from contextlib import contextmanager
from code_flow_control import ResultExistence
from help_tools import PYTHON_VERSION_INT

"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


class DumbProfiler:
    def __call__(self, function):
        return function

    def print_stats(self):
        return

    def dump_stats(self):
        return


try:
    from line_profiler import LineProfiler
except ImportError:
    LineProfiler = DumbProfiler


def set_profiler(allow_profiling=True):
    prof = None
    if allow_profiling:
        prof = LineProfiler()
    else:
        prof = DumbProfiler()
    if PYTHON_VERSION_INT[0] >= 3:
        import builtins
    else:
        import __builtin__ as builtins
    if 'profile' not in builtins.__dict__:
        builtins.__dict__['profile'] = prof
    else:
        if type(builtins.__dict__['profile']) != type(prof):
            raise Exception('Profiler settings are desynced between modules!')


@contextmanager
def profiler_result(profiler, print_result=False, output_file: ResultExistence=None):
    output_file = output_file or ResultExistence(None, None)

    try:
        yield profiler
    except:
        raise
    finally:
        if print_result:
            profiler.print_stats()
        if output_file.existence:
            if output_file.result:
                profiler.dump_stats(output_file.result)
            else:
                # TODO: сделать автоматическое имя из имени прогоняемого файла и случайного GUID
                raise NotImplemented()


