from ..module_input import validate_input, ModuleInput, valid_results

TARGETS = [
    'alias', 'rule', 'rule_interface_group', 'route', 'gateway', 'syslog', 'package', 'unbound_host', 'unbound_domain',
    'frr_ospf_general', 'frr_ospf3_general', 'unbound_forward', 'shaper_pipe', 'shaper_queue', 'shaper_rule',
    'monit_service', 'monit_test', 'monit_alert', 'wireguard_server', 'bind_domain', 'wireguard_peer', 'interface_vlan',
    'unbound_host_alias', 'interface_vxlan', 'frr_bfd_neighbor', 'frr_bgp_general', 'frr_bgp_neighbor',
    'frr_ospf3_interface', 'frr_ospf_interface', 'bind_acl', 'frr_ospf_network', 'frr_rip', 'bind_general',
    'bind_blocklist', 'bind_record', 'interface_vip', 'webproxy_general', 'webproxy_cache', 'webproxy_parent',
    'webproxy_traffic', 'webproxy_remote_acl', 'webproxy_pac_proxy', 'webproxy_pac_match', 'webproxy_pac_rule',
    'cron', 'unbound_dot', 'ipsec_cert', 'ipsec_psk', 'source_nat', 'frr_bgp_prefix_list', 'frr_bgp_community_list',
    'frr_bgp_as_path', 'frr_bgp_route_map', 'frr_ospf_prefix_list', 'frr_ospf_route_map', 'webproxy_forward',
    'webproxy_acl', 'webproxy_icap', 'webproxy_auth', 'nginx_upstream_server', 'ipsec_connection', 'ipsec_pool',
    'ipsec_child', 'ipsec_vti', 'ipsec_auth_local', 'ipsec_auth_remote', 'frr_general', 'unbound_general',
    'unbound_acl', 'ids_general', 'ids_policy', 'ids_rule', 'ids_ruleset', 'ids_user_rule', 'ids_policy_rule',
    'openvpn_instance', 'openvpn_static_key', 'openvpn_client_override', 'dhcrelay_destination', 'dhcrelay_relay',
    'interface_lagg', 'interface_loopback', 'unbound_dnsbl', 'dhcp_reservation',
]


# pylint: disable=R0912,R0915
def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    m = module_input
    result = valid_results(result)

    module_args = dict(
        target=dict(
            type='str', required=True, aliases=['tgt', 't'],
            choices=TARGETS,
            description='What part of the running config should be listed'
        ),
    )

    validate_input(i=module_input, definition=module_args)

    target = m.params['target']
    Target_Obj, target_inst = None, None

    # todo: dynamic imports
    if target == 'alias':
        from ..module_utils.main.alias import Alias as Target_Obj

    elif target == 'rule':
        from ..module_utils.main.rule import Rule as Target_Obj

    elif target == 'rule_interface_group':
        from ..module_utils.main.rule_interface_group import Group as Target_Obj

    elif target == 'route':
        from ..module_utils.main.route import Route as Target_Obj

    elif target == 'gateway':
        from ..module_utils.main.gateway import Gw as Target_Obj

    elif target == 'cron':
        from ..module_utils.main.cron import CronJob as Target_Obj

    elif target == 'unbound_general':
        from ..module_utils.main.unbound_general import General as Target_Obj

    elif target == 'unbound_acl':
        from ..module_utils.main.unbound_acl import Acl as Target_Obj

    elif target == 'unbound_host':
        from ..module_utils.main.unbound_host import Host as Target_Obj

    elif target == 'unbound_host_alias':
        from ..module_utils.main.unbound_host_alias import Alias as Target_Obj

    elif target == 'unbound_domain':
        from ..module_utils.main.unbound_domain import  \
            Domain as Target_Obj

    elif target == 'unbound_dot':
        from ..module_utils.main.unbound_dot import DnsOverTls as Target_Obj

    elif target == 'unbound_forward':
        from ..module_utils.main.unbound_forward import Forward as Target_Obj

    elif target == 'unbound_dnsbl':
        from ..module_utils.main.unbound_dnsbl import DnsBL as Target_Obj

    elif target == 'syslog':
        from ..module_utils.main.syslog import Syslog as Target_Obj

    elif target == 'package':
        from ..module_utils.main.package import Package
        target_inst = Package(m=m, name='dummy')

    elif target == 'ipsec_cert':
        from ..module_utils.main.ipsec_cert import KeyPair as Target_Obj

    elif target == 'ipsec_psk':
        from ..module_utils.main.ipsec_psk import PreSharedKey as Target_Obj

    elif target == 'shaper_pipe':
        from ..module_utils.main.shaper_pipe import Pipe as Target_Obj

    elif target == 'shaper_queue':
        from ..module_utils.main.shaper_queue import Queue as Target_Obj

    elif target == 'shaper_rule':
        from ..module_utils.main.shaper_rule import Rule as Target_Obj

    elif target == 'monit_service':
        from ..module_utils.main.monit_service import Service as Target_Obj

    elif target == 'monit_test':
        from ..module_utils.main.monit_test import Test as Target_Obj

    elif target == 'monit_alert':
        from ..module_utils.main.monit_alert import Alert as Target_Obj

    elif target == 'wireguard_server':
        from ..module_utils.main.wireguard_server import Server as Target_Obj

    elif target == 'wireguard_peer':
        from ..module_utils.main.wireguard_peer import Peer as Target_Obj

    elif target == 'interface_vlan':
        from ..module_utils.main.interface_vlan import Vlan as Target_Obj

    elif target == 'interface_vxlan':
        from ..module_utils.main.interface_vxlan import Vxlan as Target_Obj

    elif target == 'interface_lagg':
        from ..module_utils.main.interface_lagg import Lagg as Target_Obj

    elif target == 'interface_loopback':
        from ..module_utils.main.interface_loopback import Loopback as Target_Obj

    elif target == 'source_nat':
        from ..module_utils.main.source_nat import SNat as Target_Obj

    elif target == 'frr_general':
        from ..module_utils.main.frr_general import General as Target_Obj

    elif target == 'frr_bfd_neighbor':
        from ..module_utils.main.frr_bfd_neighbor import Neighbor as Target_Obj

    elif target == 'frr_bgp_general':
        from ..module_utils.main.frr_bgp_general import General as Target_Obj

    elif target == 'frr_bgp_neighbor':
        from ..module_utils.main.frr_bgp_neighbor import Neighbor as Target_Obj

    elif target == 'frr_bgp_prefix_list':
        from ..module_utils.main.frr_bgp_prefix_list import Prefix as Target_Obj

    elif target == 'frr_bgp_route_map':
        from ..module_utils.main.frr_bgp_route_map import RouteMap as Target_Obj

    elif target == 'frr_bgp_community_list':
        from ..module_utils.main.frr_bgp_community_list import Community as Target_Obj

    elif target == 'frr_bgp_as_path':
        from ..module_utils.main.frr_bgp_as_path import AsPath as Target_Obj

    elif target == 'frr_ospf_general':
        from ..module_utils.main.frr_ospf_general import General as Target_Obj

    elif target == 'frr_ospf3_general':
        from ..module_utils.main.frr_ospf3_general import General as Target_Obj

    elif target == 'frr_ospf3_interface':
        from ..module_utils.main.frr_ospf3_interface import Interface as Target_Obj

    elif target == 'frr_ospf_prefix_list':
        from ..module_utils.main.frr_ospf_prefix_list import Prefix as Target_Obj

    elif target == 'frr_ospf_interface':
        from ..module_utils.main.frr_ospf_interface import Interface as Target_Obj

    elif target == 'frr_ospf_route_map':
        from ..module_utils.main.frr_ospf_route_map import RouteMap as Target_Obj

    elif target == 'frr_ospf_network':
        from ..module_utils.main.frr_ospf_network import Network as Target_Obj

    elif target == 'frr_rip':
        from ..module_utils.main.frr_rip import Rip as Target_Obj

    elif target == 'bind_general':
        from ..module_utils.main.bind_general import General as Target_Obj

    elif target == 'bind_blocklist':
        from ..module_utils.main.bind_blocklist import Blocklist as Target_Obj

    elif target == 'bind_acl':
        from ..module_utils.main.bind_acl import Acl as Target_Obj

    elif target == 'bind_domain':
        from ..module_utils.main.bind_domain import Domain as Target_Obj

    elif target == 'bind_record':
        from ..module_utils.main.bind_record import Record as Target_Obj

    elif target == 'interface_vip':
        from ..module_utils.main.interface_vip import Vip as Target_Obj

    elif target == 'webproxy_general':
        from ..module_utils.main.webproxy_general import General as Target_Obj

    elif target == 'webproxy_cache':
        from ..module_utils.main.webproxy_cache import Cache as Target_Obj

    elif target == 'webproxy_traffic':
        from ..module_utils.main.webproxy_traffic import Traffic as Target_Obj

    elif target == 'webproxy_parent':
        from ..module_utils.main.webproxy_parent import Parent as Target_Obj

    elif target == 'webproxy_forward':
        from ..module_utils.main.webproxy_forward import General as Target_Obj

    elif target == 'webproxy_acl':
        from ..module_utils.main.webproxy_acl import General as Target_Obj

    elif target == 'webproxy_icap':
        from ..module_utils.main.webproxy_icap import General as Target_Obj

    elif target == 'webproxy_auth':
        from ..module_utils.main.webproxy_auth import General as Target_Obj

    elif target == 'webproxy_remote_acl':
        from ..module_utils.main.webproxy_remote_acl import Acl as Target_Obj

    elif target == 'webproxy_pac_proxy':
        from ..module_utils.main.webproxy_pac_proxy import Proxy as Target_Obj

    elif target == 'webproxy_pac_match':
        from ..module_utils.main.webproxy_pac_match import Match as Target_Obj

    elif target == 'webproxy_pac_rule':
        from ..module_utils.main.webproxy_pac_rule import Rule as Target_Obj

    elif target == 'nginx_upstream_server':
        from ..module_utils.main.nginx_upstream_server import UpstreamServer as Target_Obj

    elif target == 'ipsec_connection':
        from ..module_utils.main.ipsec_connection import Connection as Target_Obj

    elif target == 'ipsec_pool':
        from ..module_utils.main.ipsec_pool import Pool as Target_Obj

    elif target == 'ipsec_child':
        from ..module_utils.main.ipsec_child import Child as Target_Obj

    elif target == 'ipsec_vti':
        from ..module_utils.main.ipsec_vti import Vti as Target_Obj

    elif target == 'ipsec_auth_local':
        from ..module_utils.main.ipsec_auth_local import Auth as Target_Obj

    elif target == 'ipsec_auth_remote':
        from ..module_utils.main.ipsec_auth_remote import Auth as Target_Obj

    elif target == 'ids_general':
        from ..module_utils.main.ids_general import General as Target_Obj

    elif target == 'ids_policy':
        from ..module_utils.main.ids_policy import Policy as Target_Obj

    elif target == 'ids_rule':
        from ..module_utils.main.ids_rule import Rule as Target_Obj

    elif target == 'ids_ruleset':
        from ..module_utils.main.ids_ruleset import Ruleset as Target_Obj

    elif target == 'ids_user_rule':
        from ..module_utils.main.ids_user_rule import Rule as Target_Obj

    elif target == 'ids_policy_rule':
        from ..module_utils.main.ids_policy_rule import Rule as Target_Obj

    elif target == 'openvpn_instance':
        from ..module_utils.main.openvpn_client import Client as Target_Obj

    elif target == 'openvpn_static_key':
        from ..module_utils.main.openvpn_static_key import Key as Target_Obj

    elif target == 'openvpn_client_override':
        from ..module_utils.main.openvpn_client_override import Override as Target_Obj

    elif target == 'dhcrelay_destination':
        from ..module_utils.main.dhcrelay_destination import DhcRelayDestination as Target_Obj

    elif target == 'dhcrelay_relay':
        from ..module_utils.main.dhcrelay_relay import DhcRelayRelay as Target_Obj

    elif target == 'dhcp_reservation':
        from ..module_utils.main.dhcp_reservation_v4 import ReservationV4 as Target_Obj

    result['data'] = None

    if Target_Obj is not None or target_inst is not None:
        if target_inst is None:
            target_inst = Target_Obj(m=m, result=result)

        if hasattr(target_inst, 'get_existing'):
            # has additional filtering
            target_func = getattr(target_inst, 'get_existing')

        elif hasattr(target_inst, 'search_call'):
            target_func = getattr(target_inst, 'search_call')

        elif hasattr(target_inst, '_search_call'):
            target_func = getattr(target_inst, '_search_call')

        else:
            target_func = getattr(target_inst.b, 'get_existing')

        result['data'] = target_func()

        if hasattr(target_inst, 's'):
            target_inst.s.close()

    else:
        m.fail(f"Got unsupported target: '{target}'")

    return result
