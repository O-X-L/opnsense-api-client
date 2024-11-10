from ansible.module_utils.common.arg_spec import ModuleArgumentSpecValidator


def validate_single(
        m, module_args: dict, log_mod: str,
        key: (int, str), cnf: dict) -> bool:
    result = False

    validation = ModuleArgumentSpecValidator(module_args,
                                             m.mutually_exclusive,
                                             m.required_together,
                                             m.required_one_of,
                                             m.required_if,
                                             m.required_by
                                             ).validate(parameters=cnf)

    try:
        validation_error = validation.errors[0]

    except IndexError:
        validation_error = None

    if validation_error:
        error_msg = validation.errors.msg
        if m.params['fail_verification']:
            m.fail(f"Got invalid config for {log_mod} '{key}': {error_msg}")

        else:
            m.warn(f"Got invalid config for {log_mod} '{key}': {error_msg}")

    else:
        result = True

    return result


def convert_aliases(cnf: dict, aliases: dict) -> dict:
    # would be done by ansible-module in default-modules
    converted = {}
    all_aliases = []

    # convert aliases
    for p, a in aliases.items():
        all_aliases.extend(a)

        for _a in a:
            if _a in cnf:
                converted[p] = cnf[_a]
                break

    # keep non-aliases
    for p, v in cnf.items():
        if p not in all_aliases:
            converted[p] = v

    return converted
