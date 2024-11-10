from ..module_input import validate_input, ModuleInput, valid_results


# pylint: disable=R0912,R0915
def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    m = module_input
    result = valid_results(result)

    module_args = dict(
        target=dict(
            type='str', required=True, aliases=['tgt', 't'],
            choices=[
                'alias',
                'rule',
                'route',
                'gateway'
                'cron',
                'unbound',
                'syslog',
                'ipsec',
                'ipsec_legacy',
                'shaper',
                'monit',
                'wireguard',
                'interface_vlan',
                'interface_vxlan',
                'interface_vip',
                'interface_lagg',
                'frr',
                'webproxy',
                'bind',
                'ids',
                'openvpn',
                'dhcrelay',
                'dhcp',
            ],
            description='What part of the running config should be reloaded'
        ),
    )

    validate_input(i=module_input, definition=module_args)

    target = m.params['target']
    Target_Obj = None

    # todo: dynamic imports

    if target == 'alias':
        from ..module_utils.main.alias import Alias as Target_Obj

    elif target == 'rule':
        from ..module_utils.main.rule import Rule as Target_Obj

    elif target == 'route':
        from ..module_utils.main.route import Route as Target_Obj

    elif target == 'gateway':
        from ..module_utils.main.gateway import Gw as Target_Obj

    elif target == 'cron':
        from ..module_utils.main.cron import CronJob as Target_Obj

    elif target == 'unbound':
        from ..module_utils.main.unbound_host import Host as Target_Obj

    elif target == 'syslog':
        from ..module_utils.main.syslog import Syslog as Target_Obj

    elif target == 'ipsec':
        from ..module_utils.main.ipsec_connection import Connection as Target_Obj

    elif target == 'ipsec_legacy':
        from ..module_utils.main.ipsec_cert import KeyPair as Target_Obj

    elif target == 'shaper':
        from ..module_utils.main.shaper_pipe import Pipe as Target_Obj
        m.params['reset'] = False

    elif target == 'monit':
        from ..module_utils.main.monit_service import Service as Target_Obj

    elif target == 'wireguard':
        from ..module_utils.main.wireguard_server import Server as Target_Obj

    elif target == 'interface_vlan':
        from ..module_utils.main.interface_vlan import Vlan as Target_Obj

    elif target == 'interface_vxlan':
        from ..module_utils.main.interface_vxlan import Vxlan as Target_Obj

    elif target == 'interface_vip':
        from ..module_utils.main.interface_vip import Vip as Target_Obj

    elif target == 'interface_lagg':
        from ..module_utils.main.interface_lagg import Lagg as Target_Obj

    elif target == 'frr':
        from ..module_utils.main.frr_bgp_general import General as Target_Obj

    elif target == 'webproxy':
        from ..module_utils.main.webproxy_general import General as Target_Obj

    elif target == 'bind':
        from ..module_utils.main.bind_domain import Domain as Target_Obj

    elif target == 'ids':
        from ..module_utils.main.ids_general import General as Target_Obj

    elif target == 'openvpn':
        from ..module_utils.main.openvpn_client import Client as Target_Obj

    elif target == 'dhcrelay':
        from ..module_utils.main.dhcrelay_relay import DhcRelayRelay as Target_Obj

    elif target == 'dhcp':
        from ..module_utils.main.dhcp_reservation_v4 import ReservationV4 as Target_Obj

    if Target_Obj is not None:
        target_inst = Target_Obj(m=m, result=result)

        result['changed'] = True
        if not m.check_mode:
            target_inst.reload()

        if hasattr(target_inst, 's'):
            target_inst.s.close()

    else:
        m.fail(f"Got unsupported target: '{target}'")

    return result
