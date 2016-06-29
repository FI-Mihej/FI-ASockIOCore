import platform
import requests
import binascii
import os, os.path
import pickle
import datetime
import base64
import json
from inspect import currentframe, getframeinfo, getouterframes
import traceback
import sys
import struct

from modules_management import alt_import

with alt_import('lzma') as module:
    if module is None:
        import lzmaffi.compat
        lzmaffi.compat.register()
        import lzma


__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


PLATFORM_NAME = platform.python_implementation()  # can be 'PyPy', 'CPython', etc.
PYTHON_VERSION = platform.python_version_tuple()  # tuple() of str(); for example: ('3', '5', '1')
PYTHON_VERSION_INT = sys.version_info  # sys.version_info == (major=3, minor=2, micro=5, releaselevel='final', serial=0)
#   Usage: sys.version_info[0] == 3


class BaseClassSettings:
    def check(self):
        pass


def none_or(input_value, default_value):
    '''
    {value = input_value or default_value} will not work when for example {value = '' or b''}
    :param input_value:
    :param default_value:
    :return:
    '''
    if input_value is None:
        return default_value
    else:
        return input_value
