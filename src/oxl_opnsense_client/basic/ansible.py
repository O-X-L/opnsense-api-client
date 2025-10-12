from ansible.module_utils.common.arg_spec import ModuleArgumentSpecValidator
from ansible.module_utils.common import parameters as ansible_parameters

from basic.exceptions import ModuleHelp

# abstracted replacement for the ansible-module logic


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
            mutually_exclusive: list = None,
            required_together: list = None,
            required_one_of: list = None,
            required_if: list = None,
            required_by: dict = None,
    ):
        self.supports_check_mode = supports_check_mode
        self._module_input = module_input

        self.check_mode = self._module_input.check_mode
        self.params = self._module_input.params

        if self._module_input.exit_help:
            raise ModuleHelp(argument_spec)

        # validation
        result = ModuleArgumentSpecValidator(
            argument_spec=argument_spec,
            mutually_exclusive=mutually_exclusive,
            required_together=required_together,
            required_one_of=required_one_of,
            required_if=required_if,
            required_by=required_by,
        ).validate(parameters=self.params)

        if len(result.errors.messages) > 0:
            self.fail_json(f"Failed to validate parameters: {result.errors.messages}")

        ansible_parameters._handle_aliases(argument_spec=argument_spec, parameters=self.params)
        ansible_parameters._set_defaults(argument_spec=argument_spec, parameters=self.params)
        for field, spec in argument_spec.items():
            if spec['type'] == 'dict' and 'options' in spec:
                # nested arguments
                ansible_parameters._handle_aliases(argument_spec=spec['options'], parameters=self.params[field])
                ansible_parameters._set_defaults(argument_spec=spec['options'], parameters=self.params[field])

    @staticmethod
    def exit_json(data: dict):
        del data
        # pylint: disable=E0711,E0702
        raise NotImplemented

    def warn(self, msg: str):
        self._module_input.c.debug_or_warn(msg)

    def fail_json(self, msg: str):
        self._module_input.c.fail(msg)
