from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.webproxy_traffic import Traffic


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        download_kb_max=dict(
            type='str', required=False, default='2048',
            aliases=['download_max', 'download', 'dl_max', 'dl'],
            description='The maximum size for downloads in kilobytes (leave empty to disable)'
        ),
        upload_kb_max=dict(
            type='str', required=False, default='1024',
            aliases=['upload_max', 'upload', 'ul_max', 'ul'],
            description='The maximum size for uploads in kilobytes (leave empty to disable)'
        ),
        throttle_kb_bandwidth=dict(
            type='str', required=False, default='1024',
            aliases=['throttle_bandwidth', 'throttle_bw', 'bandwidth', 'bw'],
            description='The allowed overall bandwidth in kilobits per second (leave empty to disable)'
        ),
        throttle_kb_host_bandwidth=dict(
            type='str', required=False, default='256',
            aliases=['throttle_host_bandwidth', 'throttle_host_bw', 'host_bandwidth', 'host_bw'],
            description='The allowed per host bandwidth in kilobits per second (leave empty to disable)'
        ),
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Traffic(m=module_input, result=result))
    return result
