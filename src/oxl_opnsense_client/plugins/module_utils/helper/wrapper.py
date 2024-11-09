
from inspect import stack as inspect_stack
from inspect import getfile as inspect_getfile

from ..base.cls import BaseModule, GeneralModule
from .utils import profiler
from .main import diff_remove_empty


def module_process(instance: (BaseModule, GeneralModule)):
    instance.check()
    instance.process()
    if 'reload' in instance.m.params and instance.r['changed'] and instance.m.params['reload']:
        instance.reload()

    if hasattr(instance, 's'):
        instance.s.close()

    instance.r['diff'] = diff_remove_empty(instance.r['diff'])


def module_wrapper(instance: (BaseModule, GeneralModule)):
    if instance.m.params['profiling'] or instance.m.params['debug']:
        module_name = inspect_getfile(inspect_stack()[1][0]).rsplit('/', 1)[1].rsplit('.', 1)[0]
        return profiler(check=module_process, module_name=module_name, kwargs={'instance': instance})

    return module_process(instance)
