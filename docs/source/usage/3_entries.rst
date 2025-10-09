.. _usage_entries:

.. include:: ../_include/head.rst

===========
3 - Entries
===========

General vs Entry Modules
########################

From a logic-standpoint we need to differentiate between modules that:

* configure general service-settings and

* the ones that manage multiple entries of a service

'General' modules can only update the settings.

'Entry' modules can create, update and delete entries.

Create - Update - Delete
########################

**Existing entries need to be matched!** Matching is performed by either a single **'ID-Field'** (commonly 'name') or by multiple **'Match-Fields'** (seen as :code:`match_fields` argument in the module-specs)

.. code-block:: python3

    # LIST
    c.run_module('list', params={'target': 'syslog'})
    # {'error': None, 'result': {'changed': False, 'data': []}}

    # CREATE
    c.run_module('syslog', params={'target': '192.168.0.1', 'port': 5303})
    # {'error': None, 'result': {'changed': True, 'diff': {'before': None, 'after': {'uuid': None, 'rfc5424': False, 'enabled': True, 'target': '192.168.0.1', 'transport': 'udp4', 'facility': [], 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'certificate': '', 'port': 5303, 'description': ''}}}}

    # UPDATE
    c.run_module('syslog', params={'target': '192.168.0.1', 'port': 11303, 'match_field': ['target']})
    # {'error': None, 'result': {'changed': True, 'diff': {'before': {'uuid': 'ead66777-ae96-42b5-a271-8ffa14a7f814', 'rfc5424': False, 'enabled': True, 'target': '192.168.0.1', 'transport': 'udp4', 'facility': [], 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'certificate': '', 'port': 5303, 'description': ''}, 'after': {'uuid': 'ead66777-ae96-42b5-a271-8ffa14a7f814', 'rfc5424': False, 'enabled': True, 'target': '192.168.0.1', 'transport': 'udp4', 'facility': [], 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'certificate': '', 'port': 11303, 'description': ''}}}}

    # LIST
    c.run_module('list', params={'target': 'syslog'})
    # {'error': None, 'result': {'changed': False, 'data': [{'target': '192.168.0.1', 'enabled': True, 'transport': 'udp4', 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'facility': [], 'certificate': '', 'port': 11303, 'rfc5424': False, 'description': '', 'uuid': 'ead66777-ae96-42b5-a271-8ffa14a7f814'}]}}

    # CHECK-MODE (DRY-RUN)
    c.run_module('syslog', params={'target': '192.168.0.1', 'state': 'absent', 'match_fields': ['target']}, check_mode=True)
    # {'error': None, 'result': {'changed': True, 'diff': {'before': {'uuid': 'ead66777-ae96-42b5-a271-8ffa14a7f814', 'rfc5424': False, 'enabled': True, 'target': '192.168.0.1', 'transport': 'udp4', 'facility': [], 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'certificate': '', 'port': 11303, 'description': ''}}}}

    # LIST
    c.run_module('list', params={'target': 'syslog'})
    # {'error': None, 'result': {'changed': False, 'data': [{'target': '192.168.0.1', 'enabled': True, 'transport': 'udp4', 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'facility': [], 'certificate': '', 'port': 11303, 'rfc5424': False, 'description': '', 'uuid': 'ead66777-ae96-42b5-a271-8ffa14a7f814'}]}}

    # DELETE
    c.run_module('syslog', params={'target': '192.168.0.1', 'state': 'absent', 'match_fields': ['target']})
    # {'error': None, 'result': {'changed': True, 'diff': {'before': {'uuid': 'ead66777-ae96-42b5-a271-8ffa14a7f814', 'rfc5424': False, 'enabled': True, 'target': '192.168.0.1', 'transport': 'udp4', 'facility': [], 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'certificate': '', 'port': 11303, 'description': ''}, 'after': None}}}

    # LIST
    c.run_module('list', params={'target': 'syslog'})
    # {'error': None, 'result': {'changed': False, 'data': []}}
