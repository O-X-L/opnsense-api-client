from ....exceptions import ModuleFailure

MODULE_EXCEPTIONS = (ModuleNotFoundError, ImportError)


class ModuleSoftError(Exception):
    pass


def exit_bug(msg: str):
    raise ModuleFailure(f"THIS MIGHT BE A MODULE-BUG: {msg}")


def exit_debug(msg: str):
    raise ModuleFailure(f"DEBUG INFO: {msg}")


def exit_env(msg: str):
    raise ModuleFailure(f"ENVIRONMENTAL ERROR: {msg}")


def exit_cnf(msg: str):
    raise ModuleFailure(f"CONFIG ERROR: {msg}")


def module_dependency_error() -> None:
    exit_env(
        'For this Ansible-module to work you must install its dependencies first: '
        "'python3 -m pip install --upgrade httpx'"
    )
