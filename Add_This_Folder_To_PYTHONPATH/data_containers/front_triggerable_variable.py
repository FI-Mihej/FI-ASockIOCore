from enum import Enum


"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


class FrontTriggerableVariableType(Enum):
    equal = 0
    lesser = 1
    lesser_or_equal = 2
    bigger = 3
    bigger_or_equal = 4
    not_equal = 5


class FrontTriggerableVariable:
    def __init__(self, triggerable_variable_type, value_limit):
        self.triggerable_variable_type = triggerable_variable_type
        self.value_limit = value_limit
        self._last_result = False
        self.test_worker = None

        if FrontTriggerableVariableType.equal == triggerable_variable_type:
            self.test_worker = FrontTriggerableVariable._equal
        elif FrontTriggerableVariableType.lesser == triggerable_variable_type:
            self.test_worker = FrontTriggerableVariable._lesser
        elif FrontTriggerableVariableType.lesser_or_equal == triggerable_variable_type:
            self.test_worker = FrontTriggerableVariable._lesser_or_equal
        elif FrontTriggerableVariableType.bigger == triggerable_variable_type:
            self.test_worker = FrontTriggerableVariable._bigger
        elif FrontTriggerableVariableType.bigger_or_equal == triggerable_variable_type:
            self.test_worker = FrontTriggerableVariable._bigger_or_equal
        elif FrontTriggerableVariableType.not_equal == triggerable_variable_type:
            self.test_worker = FrontTriggerableVariable._not_equal

    def test_trigger(self, value):
        result = None
        new_test_result = self.test_worker(value, self.value_limit)
        if new_test_result != self._last_result:
            self._last_result = new_test_result
            result = new_test_result
        return result


    @staticmethod
    def _equal(value, value_limit):
        return value == value_limit

    @staticmethod
    def _lesser(value, value_limit):
        return value < value_limit

    @staticmethod
    def _lesser_or_equal(value, value_limit):
        return value <= value_limit

    @staticmethod
    def _bigger(value, value_limit):
        return value > value_limit

    @staticmethod
    def _bigger_or_equal(value, value_limit):
        return value >= value_limit

    @staticmethod
    def _not_equal(value, value_limit):
        return value != value_limit
