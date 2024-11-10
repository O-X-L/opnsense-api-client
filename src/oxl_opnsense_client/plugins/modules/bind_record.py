from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.bind_record import RECORD_MOD_ARGS
from ..module_utils.main.bind_record import Record


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)
    validate_input(i=module_input, definition=RECORD_MOD_ARGS)
    module_wrapper(Record(m=module_input, result=result))
    return result
