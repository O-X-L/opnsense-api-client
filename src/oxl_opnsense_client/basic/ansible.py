from pathlib import Path

from basic.exceptions import ModuleHelp

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

    def __repr__(self) -> str:
        return self.msg

class ValidationResult:
    def __init__(self, errors: list[ValidationError]):
        self.errors = errors

    def __repr__(self) -> str:
        return str(self.errors)


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

        empty = False
        if kn not in p or p[kn] in [None, '']:
            if 'required' in d and d['required']:
                errors.append(ValidationError(f"The required parameter '{k}' was not provided!"))

            if 'default' in d:
                normalized_params[k] = d['default']

            else:
                normalized_params[k] = ''

        else:
            normalized_params[k] = parameters[k]

        if empty:
            continue

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

        try:
            result, _ = validate_and_normalize_params(parameters, self.argument_spec)

        except KeyError as e:
            return ValidationResult([
                ValidationError(f"Failed to validate parameters: {e}")
            ])

        return result


class ModuleInput:
    def __init__(self, client, params: dict, check_mode: bool = False, exit_help: bool = False):
        self.c = client
        self.user_params = params
        self.check_mode = check_mode
        self.exit_help = exit_help

    @property
    def params(self):
        return {**self.c.params, **self.user_params}


class AnsibleModule:
    def __init__(
            self,
            argument_spec: dict,
            module_input: ModuleInput,
            supports_check_mode: bool = False,
            required_if: list = None,
            required_one_of: list = None,
            mutually_exclusive: list = None,
    ):
        self.argument_spec = argument_spec
        self.supports_check_mode = supports_check_mode
        del required_if, required_one_of, mutually_exclusive

        self._module_input = module_input

        self.check_mode = self._module_input.check_mode
        self.params = self._module_input.params
        self._validate_and_normalize()

    def _validate_and_normalize(self):
        if self._module_input.exit_help:
            raise ModuleHelp(self.argument_spec)

        try:
            result, normalized_params = validate_and_normalize_params(self.params, self.argument_spec)

        except KeyError as e:
            self.fail_json(f"Failed to validate parameters: {e}")
            return

        if len(result.errors) > 0:
            self.fail_json(f"Failed to validate parameters: {result.errors}")

        self.params = normalized_params



    @staticmethod
    def exit_json(data: dict):
        del data
        # pylint: disable=E0711,E0702
        raise NotImplemented

    def warn(self, msg: str):
        self._module_input.c.warn(msg)

    def fail_json(self, msg: str):
        self._module_input.c.fail(msg)
