from pathlib import Path

from basic.exceptions import ModuleFailure, ModuleSuccess
# from basic.module_input import ModuleInput

# abstracted replacement for the ansible-module logic


TYPE_MAPPING = {
    'str': str,
    'bool': bool,
    'list': list,
    'int': int,
    'float': float,
    'dict': dict,
    'path': Path,
}


class ValidationError:
    def __init__(self, msg: str):
        self.msg = msg


class ValidationResult:
    def __init__(self, errors: list[ValidationError]):
        self.errors = errors


# pylint: disable=R0915
def validate_and_normalize_params(parameters: dict, argument_spec: dict) -> tuple[ValidationResult, dict]:
    p = parameters
    errors = []
    if len(p) == 0:
        errors.append(ValidationError('No parameters/arguments provided'))

    normalized_params = {}
    for k, d in argument_spec.items():
        kn = k
        if k not in p and 'aliases' in d:
            for ka in d['aliases']:
                if ka in p:
                    kn = ka
                    break

        if kn not in p:
            if 'required' in d and d['required']:
                errors.append(ValidationError(f"The required parameter '{k}' was not provided!"))

            if 'default' in d:
                normalized_params[k] = d['default']

            else:
                normalized_params[k] = ''

        else:
            normalized_params[k] = parameters[k]

        if 'type' in d:
            t = TYPE_MAPPING[d['type']]
            if not isinstance(normalized_params[k], t):
                try:
                    normalized_params[k] = t(normalized_params[k])

                except (TypeError, ValueError) as e:
                    errors.append(ValidationError(
                        f"The parameter '{k}' has an invalid type - must be {d['type']} ({e})"
                    ))

        if 'choices' in d:
            if isinstance(normalized_params[k], str) and normalized_params[k] not in d['choices']:
                errors.append(ValidationError(
                    f"The parameter '{k}' has an invalid value - must be one of: {d['choices']}"
                ))

            elif isinstance(normalized_params[k], list):
                for e in normalized_params[k]:
                    if e not in d['choices']:
                        errors.append(ValidationError(
                            f"The parameter '{k}' has an invalid value - have to be one or multiple of: {d['choices']}"
                        ))

    return ValidationResult(errors), normalized_params


class ModuleArgumentSpecValidator:
    def __init__(self, argument_spec: dict, result: ValidationResult = None):
        self.argument_spec = argument_spec
        self.result = result

    # pylint: disable=R0915
    def validate(self, parameters: dict) -> ValidationResult:
        if self.result is not None:
            return self.result

        result, _ = validate_and_normalize_params(parameters, self.argument_spec)
        return result


class AnsibleModule:
    def __init__(self, argument_spec: dict, supports_check_mode: bool):
        self.argument_spec = argument_spec
        self.supports_check_mode = supports_check_mode

        # todo: module_input
        self.check_mode = False
        self.diff_mode = False
        self.params = {}

    def _validate_and_normalize(self):
        result, normalized_params = validate_and_normalize_params(self.params, self.argument_spec)
        if len(result.errors) > 0:
            self.fail_json(f"Failed to validate parameters: {result.errors}")

        self.params = normalized_params

    @staticmethod
    def exit_json(result: dict):
        raise ModuleSuccess(result)

    @staticmethod
    def warn(msg: str):
        print(f"WARNING: {msg}")

    @staticmethod
    def fail_json(msg: str):
        raise ModuleFailure(msg)
