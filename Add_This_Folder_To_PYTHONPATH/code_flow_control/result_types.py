"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


class ResultExistence:
    def __init__(self, existence, result):
        self.existence = existence
        self.result = result

    def __bool__(self):
        return self.existence

    def __nonzero__(self):
        return self.__bool__()

    def __str__(self):
        return '{}: {}'.format(self.existence, self.result)


class ResultCache(ResultExistence):
    def __init__(self):
        super(ResultCache, self).__init__(False, None)

    def __call__(self, *args, **kwargs):
        self.existence = False

    def get(self):
        return self.result

    def set(self, new_result):
        self.existence = True
        self.result = new_result


class ResultType:
    def __init__(self, type_id, result):
        self.type_id = type_id
        self.result = result

    def __eq__(self, other):
        # "__ne__() delegates to __eq__() and inverts the result"
        # if type(other) == ResultType:
        if isinstance(other, ResultType):
            return self.type_id == other.type_id
        else:
            return self.type_id == other
