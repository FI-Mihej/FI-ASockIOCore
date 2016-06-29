from inspect import getouterframes, currentframe
from RequestCache import RequestCache
import os

"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


class LineTracer:
    def __init__(self, print_full_file_name=False, trace_allowed=True):
        self.print_full_file_name = print_full_file_name
        self.trace_allowed = trace_allowed
        self._file_cache = RequestCache(999999)
        pass

    def _get_file_data(self, path):
        file_data = self._file_cache.try_to_get_data_for_request(path)
        if not file_data:
            with open(path) as file:
                file_data = file.readlines()
                file_data = [line.rstrip('\n') for line in file_data]
                self._file_cache.put_new_request(path, file_data)
        return file_data

    def _get_file_line(self, path, line_num):
        line_num -= 1  # make line numbers start from 0 - not from 1
        default_answer = None
        if line_num < 0:
            return default_answer
        file_data = self._get_file_data(path)
        max_line = len(file_data) - 1
        if line_num > max_line:
            return default_answer

        return file_data[line_num]

    def trace(self, depth=0):
        if not self.trace_allowed:
            result = (None, None, None, None, None)
            return result
        frame, filename, line_number, function_name, lines, index = getouterframes(currentframe())[1 + depth]
        previous_line_num = line_number - 1
        lines = self._get_file_line(filename, previous_line_num)
        if not self.print_full_file_name:
            filename = os.path.basename(filename)
        result = (filename, function_name, previous_line_num, lines, index)
        return result

    def __call__(self):
        if not self.trace_allowed:
            return
        print(self.trace(depth=1))
