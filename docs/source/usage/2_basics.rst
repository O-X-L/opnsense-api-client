.. _usage_basics:

.. include:: ../_include/head.rst

==========
2 - Basics
==========

Client Arguments
################

* **firewall** - string - required

  IP-Address or DNS hostname of the target firewall.

  Must be included as 'common name' or 'subject alternative name' in the firewalls web-certificate to use 'ssl_verify=true'


* **port** - int - default 443

  Port the target firewall uses for its web-interface


* **credential_file** - path

  Path to the api-credential file as downloaded through the web-interface.

  Alternative to 'api_key' and 'api_secret'


* **token** - string

  API key/token used to authenticate, alternative to 'api_credential_file'


* **secret** - string

  API secret used to authenticate, alternative to 'api_credential_file'.


* **ssl_verify** - boolean - default true

  If the certificate of the target firewall should be validated. RECOMMENDED FOR PRODUCTION USAGE!


* **ssl_ca_file** - path

  If you use an internal certificate-authority to create the certificate of the target firewall, provide the path to its public key for validation


* **api_timeout** - float - default is module-specific

  Manually override the modules default API-request timeout


* **api_retries** - int - default 0

  Number of retries on API requests, in case there is an error when establishing the connection.

  This does not handle errors returned by the OPNsense system


* **debug** - boolean - default false

  Used to en-/disable the debug mode.

  All API requests and responses will be shown at runtime.

  Will be hidden if the tasks 'no_log' parameter is set to 'true'


* **profiling** - boolean - default false

  Used to en-/disable the profiling mode.

  Time consumption of the module will be logged to '/tmp/oxlorg.opnsense'

----

Module Specs
############

You can list all available modules and show their argument-specifications:

.. code-block:: python3

    c.list_modules()
    # ['acme_account', 'acme_action', 'acme_certificate', 'acme_general', 'acme_validation', 'alias', 'alias_multi', 'alias_purge', 'bind_acl', 'bind_blocklist', 'bind_domain', 'bind_general', 'bind_record', 'bind_record_multi', 'cron', 'dhcp_controlagent', 'dhcp_general', 'dhcp_reservation', 'dhcp_subnet', 'dhcrelay_destination', 'dhcrelay_relay', 'dnsmasq_boot', 'dnsmasq_domain', 'dnsmasq_general', 'dnsmasq_host', 'dnsmasq_option', 'dnsmasq_range', 'dnsmasq_tag', 'frr_bfd_general', 'frr_bfd_neighbor', 'frr_bgp_as_path', 'frr_bgp_community_list', 'frr_bgp_general', 'frr_bgp_neighbor', 'frr_bgp_peer_group', 'frr_bgp_prefix_list', 'frr_bgp_redistribution', 'frr_bgp_route_map', 'frr_diagnostic', 'frr_general', 'frr_ospf3_general', 'frr_ospf3_interface', 'frr_ospf3_network', 'frr_ospf3_prefix_list', 'frr_ospf3_redistribution', 'frr_ospf3_route_map', 'frr_ospf_general', 'frr_ospf_interface', 'frr_ospf_network', 'frr_ospf_prefix_list', 'frr_ospf_redistribution', 'frr_ospf_route_map', 'frr_rip', 'gateway', 'group', 'hasync_general', 'hasync_service', 'ids_action', 'ids_general', 'ids_policy', 'ids_policy_rule', 'ids_rule', 'ids_ruleset', 'ids_user_rule', 'interface_bridge', 'interface_gif', 'interface_gre', 'interface_lagg', 'interface_loopback', 'interface_vip', 'interface_vlan', 'interface_vxlan', 'ipsec_auth_local', 'ipsec_auth_remote', 'ipsec_cert', 'ipsec_child', 'ipsec_connection', 'ipsec_general', 'ipsec_manual_spd', 'ipsec_pool', 'ipsec_psk', 'ipsec_vti', 'list', 'monit_alert', 'monit_service', 'monit_test', 'nat_one_to_one', 'nat_source', 'neighbor', 'nginx_general', 'nginx_upstream_server', 'openvpn_client', 'openvpn_client_override', 'openvpn_server', 'openvpn_static_key', 'openvpn_status', 'package', 'postfix_address', 'postfix_domain', 'postfix_general', 'postfix_headercheck', 'postfix_recipient', 'postfix_recipientbcc', 'postfix_sender', 'postfix_senderbcc', 'postfix_sendercanonical', 'privilege', 'raw', 'reload', 'route', 'rule', 'rule_interface_group', 'rule_multi', 'rule_purge', 'savepoint', 'service', 'shaper_pipe', 'shaper_queue', 'shaper_rule', 'snapshot', 'syslog', 'system', 'unbound_acl', 'unbound_dnsbl', 'unbound_dot', 'unbound_forward', 'unbound_general', 'unbound_host', 'unbound_host_alias', 'user', 'webproxy_acl', 'webproxy_auth', 'webproxy_cache', 'webproxy_forward', 'webproxy_general', 'webproxy_icap', 'webproxy_pac_match', 'webproxy_pac_proxy', 'webproxy_pac_rule', 'webproxy_parent', 'webproxy_remote_acl', 'webproxy_traffic', 'wireguard_general', 'wireguard_peer', 'wireguard_server', 'wireguard_show']

    c.module_specs('route')
    # {'specs': {'gateway': {'type': 'str', 'required': True, 'aliases': ['gw'], 'description': 'Specify a valid existing gateway matching the networks ip protocol'}, 'network': {'type': 'str', 'required': True, 'aliases': ['nw', 'net'], 'description': 'Specify a valid network matching the gateways ip protocol'}, 'description': {'type': 'str', 'required': False, 'aliases': ['desc']}, 'match_fields': {'type': 'list', 'required': False, 'elements': 'str', 'description': "Fields that are used to match configured routes with the running config - if any of those fields are changed, the module will think it's a new route", 'choices': ['network', 'gateway', 'description'], 'default': ['network', 'gateway']}, 'reload': {'type': 'bool', 'required': False, 'default': True, 'aliases': ['apply'], 'description': 'If the running config should be reloaded/applied on change - will take some time'}, 'state': {'type': 'str', 'required': False, 'choices': ['present', 'absent'], 'default': 'present'}, 'enabled': {'type': 'bool', 'required': False, 'default': True}}}

    c.module_specs('route', stdout=True)
    # {
    #   "gateway": {
    #     "type": "str",
    #     "required": true,
    #     "aliases": [
    #       "gw"
    #     ],
    #     "description": "Specify a valid existing gateway matching the networks ip protocol"
    #   },
    #   "network": {
    #     "type": "str",
    #     "required": true,
    #     "aliases": [
    #       "nw",
    #       "net"
    #     ],
    #     "description": "Specify a valid network matching the gateways ip protocol"
    #   },
    #   "description": {
    #     "type": "str",
    #     "required": false,
    #     "aliases": [
    #       "desc"
    #     ]
    #   },
    #   "match_fields": {
    #     "type": "list",
    #     "required": false,
    #     "elements": "str",
    #     "description": "Fields that are used to match configured routes with the running config - if any of those fields are changed, the module will think it's a new route",
    #     "choices": [
    #       "network",
    #       "gateway",
    #       "description"
    #     ],
    #     "default": [
    #       "network",
    #       "gateway"
    #     ]
    #   },
    #   "reload": {
    #     "type": "bool",
    #     "required": false,
    #     "default": true,
    #     "aliases": [
    #       "apply"
    #     ],
    #     "description": "If the running config should be reloaded/applied on change - will take some time"
    #   },
    #   "state": {
    #     "type": "str",
    #     "required": false,
    #     "choices": [
    #       "present",
    #       "absent"
    #     ],
    #     "default": "present"
    #   },
    #   "enabled": {
    #     "type": "bool",
    #     "required": false,
    #     "default": true
    #   }
    # }

----

Base Modules
############

List
****

You can use the :code:`list` module to query existing entries and settings:

.. code-block:: python3

    c.run_module('list', params={'target': 'syslog'})
    # {'error': None, 'result': {'changed': False, 'data': [{'target': '192.168.0.1', 'enabled': True, 'transport': 'udp4', 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'facility': [], 'certificate': '', 'port': 5303, 'rfc5424': False, 'description': '', 'uuid': '32b1ce94-93d0-4d20-93a2-4fff12d12a54'}]}}

Reload
******

The :code:`reload` module can be used to reload services and apply config-changes.

.. code-block:: python3

    c.run_module('reload', params={'target': 'syslog'})
    # {'error': None, 'result': {'changed': True}}

Service
*******

The :code:`service` module can be used to manage services.

.. code-block:: python3

    c.run_module('service', params={'name': 'syslog', 'action': 'status'})
    # {'error': None, 'result': {'changed': False, 'executed': 'status', 'data': {'status': 'running', 'widget': {'caption_restart': 'Restart', 'caption_start': 'Start', 'caption_stop': 'Stop'}}}}

    c.run_module('service', params={'name': 'syslog', 'action': 'restart'})
    # {'error': None, 'result': {'changed': True, 'executed': 'restart'}}

----

Network Connection
##################

TLS Verification
****************

By default the TLS-connection to the firewall is verified!

If your client does not trust the target certificate you will receive a :code:`ConnectError` with the message: :code:`CERTIFICATE_VERIFY_FAILED`.

In a non-test environment you should **ALWAYS** verify that the TLS connection is valid!

For testing-purposes you are able to manually disable it by setting :code:`ssl_verify` to False.

Internal CA
===========

If you use an internal CA to sign your firewall-certificates you might have to specify the CA-file via :code:`ssl_ca_path`.

----

Bad Connections
***************

If the target firewall has a high-latency connection or the connection has some packet loss - you might want to increase the :code:`api_retries` and/or :code:`api_timeout`.

----

Forward Proxy
*************

If your target firewalls are only reachable over `a forward proxy like Squid <https://docs.o-x-l.com/proxy/forward_squid.html>`_ you can set the :code:`HTTPS_PROXY` environmental variable.
