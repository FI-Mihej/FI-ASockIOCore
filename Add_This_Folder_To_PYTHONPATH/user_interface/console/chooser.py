import colorama
from .colorama_helpers import colorama_init

"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ButenkoMS <gtalk@butenkoms.space>'


_LINE_TEMPLATE = '   {}: {}{}{}'


class Chooser:
    def __init__(self, list_of_options: list, variant_type_name: str=None, line_template: str=None):
        self.list_of_options = list_of_options
        self.variant_type_name = variant_type_name or 'variant'
        self.line_template = line_template or _LINE_TEMPLATE

    def choose(self, last_tool_id_str: str=None):
        last_tool_id_str = last_tool_id_str or ''
        input_raw_last_tool_id = str()
        tool_number = None
        tool_is_chosen = False

        with colorama_init():
            print('{}Chose {} By Entering Number:{}'.format(colorama.Fore.YELLOW, self.variant_type_name.title(),
                                                            colorama.Style.RESET_ALL))
            index = 1
            for tool_name in self.list_of_options:
                print(self.line_template.format(
                    tool_name,
                    colorama.Fore.GREEN,
                    index,
                    colorama.Style.RESET_ALL
                ))
                index += 1

            while not tool_is_chosen:
                try:
                    tool_number = input('Chose {0} ID number or leave empty to use last used {0} ID ({1}): '.format(
                        self.variant_type_name, last_tool_id_str))
                    if len(tool_number) == 0:
                        tool_number = last_tool_id_str
                    tool_number = int(tool_number)
                    if (tool_number < 1) or (tool_number > len(self.list_of_options)):
                        raise ValueError
                    input_raw_last_tool_id = str(tool_number)
                    tool_number -= 1
                    tool_is_chosen = True
                except ValueError:
                    pass
            print()

        result = (tool_is_chosen, tool_number, input_raw_last_tool_id)
        return result
