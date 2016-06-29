from code_flow_control.result_types import ResultExistence


"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


class AddToCompoundDict:
    def __init__(self, original_dict, default_value, mediator):
        '''

        :param original_dict:
        :param default_value: functor. list(); {1:set(), 2:[set(), set(), list()]}; etc.
        :param mediator: functor. original_dict[index].add(y), original_dict[index] += y, etc. Should return
            ResultExistence(True, ...) or None/nothing
        :return:
        '''
        self.original_dict = original_dict
        self._mediator = mediator
        self._default_value = default_value

    def add(self, key, value=None):
        # if key not in self.original_dict:
        #     self.original_dict[key] = self._default_value()
        self.original_dict.setdefault(key, self._default_value())
        result = self._mediator(self.original_dict, key, value)
        # if result is not None:
        if isinstance(result, ResultExistence):
            self.original_dict[key] = result.result
