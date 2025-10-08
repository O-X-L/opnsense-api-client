from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import RELOAD_MOD_ARG
from ..module_utils.main.webproxy_cache import Cache


BLANK_VALUES = {
    'memory_cache_mode': 'default',
}


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        memory_mb=dict(
            type='int', required=False, default=256, aliases=['memory', 'mem'],
            description='The cache memory size to use or zero to disable completely'
        ),
        size_mb=dict(
            type='int', required=False, default=100, aliases=['size'],
            description='The storage size for the local cache'
        ),
        directory=dict(
            type='str', required=False, default='/var/squid/cache', aliases=['dir'],
            description='The location for the local cache'
        ),
        layer_1=dict(
            type='int', required=False, default=16, aliases=['layer1', 'l1'],
            description='The number of first-level subdirectories for the local cache'
        ),
        layer_2=dict(
            type='int', required=False, default=256, aliases=['layer2', 'l2'],
            description='The number of second-level subdirectories for the local cache'
        ),
        size_mb_max=dict(
            type='int', required=False, default=4,
            aliases=['maximum_object_size', 'max_size'],
            description='The maximum object size'
        ),
        memory_kb_max=dict(
            type='int', required=False, default=512,
            aliases=['maximum_object_size_in_memory', 'max_memory', 'max_mem'],
            description='The maximum object size'
        ),
        memory_cache_mode=dict(
            type='str', required=False, default='default',
            aliases=['cache_mode', 'mode'],
            choices=['always', 'disk', 'network', 'default'],
            description='Controls which objects to keep in the memory cache (cache_mem) always: '
                        'Keep most recently fetched objects in memory (default) disk: Only disk '
                        'cache hits are kept in memory, which means an object must first be '
                        'cached on disk and then hit a second time before cached in memory. '
                        'network: Only objects fetched from network is kept in memory'
        ),
        cache_linux_packages=dict(
            type='bool', required=False, default=False,
            description='Enable or disable the caching of packages for linux distributions. '
                        'This makes sense if you have multiple servers in your network and do '
                        'not host your own package mirror. This will reduce internet traffic '
                        'usage but increase disk access'
        ),
        cache_windows_updates=dict(
            type='bool', required=False, default=False,
            description='Enable or disable the caching of Windows updates. This makes sense '
                        "if you don't have a WSUS server. If you can setup a WSUS server, "
                        'this solution should be preferred'
        ),
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Cache(m=module_input, result=result))
    return result
