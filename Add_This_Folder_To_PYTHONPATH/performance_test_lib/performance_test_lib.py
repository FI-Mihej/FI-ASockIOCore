from contextlib import contextmanager
import copy
import time
from code_flow_control import ResultExistence

"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


class PerformanceTestResult(Exception):
    def __init__(self, result):
        super(PerformanceTestResult, self).__init__()
        self.result = result


@contextmanager
def test_run_time(test_name: str, number_of_iterations: int, throw_result: bool=False):
    index = ResultExistence(True, copy.copy(number_of_iterations))
    start_time = time.time()
    try:
        yield index
    except:
        raise
    finally:
        number_of_iterations -= index.result
        end_time = time.time()
        result_time = end_time - start_time
        print('>>> "{}"'.format(test_name))
        print('\t' + 'It was used', result_time, 'seconds to process', number_of_iterations, 'iterations.')
        if result_time > 0:
            print('\t' + 'There is', number_of_iterations / result_time, 'iterations per second')
        print()

        if throw_result:
            result_data = list()
            result_data.append(result_time)
            if result_time > 0:
                result_data.append(number_of_iterations / result_time)
            else:
                result_data.append(None)
            result_data = tuple(result_data)
            raise PerformanceTestResult(result_data)


def test_function_run_time(testable_function):
    '''
    Use 'iterations_qnt=1000000' parameter to pass number of iterations
    :param testable_function: function
    :return:
    '''
    def run_time_test_func(*args, **kwargs):

        test_name = ''
        if 'performance_test_lib__test_name' in kwargs:
            test_name = str(kwargs['performance_test_lib__test_name'])
            del kwargs['performance_test_lib__test_name']
        test_name = '{}: {}'.format(str(testable_function), test_name)

        number_of_iterations = 0
        if 'performance_test_lib__iterations_qnt' in kwargs:
            number_of_iterations = int(kwargs['performance_test_lib__iterations_qnt'])
            del kwargs['performance_test_lib__iterations_qnt']

        throw_result = False
        if 'performance_test_lib__throw_result' in kwargs:
            throw_result = kwargs['performance_test_lib__throw_result']
            del kwargs['performance_test_lib__throw_result']

        with test_run_time(test_name, number_of_iterations, throw_result) as index:
            while index.result > 0:
                testable_function(*args, **kwargs)
                index.result -= 1
    return run_time_test_func
