__author__ = 'ButenkoMS <gtalk@butenkoms.space>'

import uuid
from enum import Enum

class TypeOfGenerator(Enum):
    INTEGER = 0
    GUID_STRING = 1

    # _VALUES_TO_NAMES = {
    #     0: "INTEGER",
    #     1: "GUID_STRING",
    # }
    #
    # _NAMES_TO_VALUES = {
    #     "INTEGER": 0,
    #     "GUID_STRING": 1,
    # }


class IDGenerator:

    def __init__(self, type=TypeOfGenerator.INTEGER):
        self.counter = 0
        self.type = type

    def get_new_ID(self):
        currentCounter = None
        if TypeOfGenerator.INTEGER == self.type:
            currentCounter = self.counter
            self.counter += 1
        elif TypeOfGenerator.GUID_STRING == self.type:
            seq = self.counter
            self.counter += 1
            currentCounter = uuid.uuid1(clock_seq=seq).hex
        return currentCounter

    def remove_ID(self, ID):
        pass

    def clear(self):
        self.counter = 0

