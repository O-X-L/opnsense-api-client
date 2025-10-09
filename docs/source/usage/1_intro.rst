.. _usage_intro:

.. include:: ../_include/head.rst

=========
1 - Intro
=========

This is a Python3 client for interacting with the official OPNsense API.

It enables easy management and automation of OPNsense firewalls.

The base-code is a Fork of `this OPNsense Ansible-Collection <https://github.com/O-X-L/ansible-opnsense>`_ that was refactored for use within raw Python.

This can be useful if you want to automate your Infrastructure and do not use `Ansible <https://www.ansible.com/how-ansible-works/>`_.

----

Install
#######

.. code-block:: bash

    pip install oxl-opnsense-client

Check
#####

.. code-block:: python3

    from oxl_opnsense_client import Client

    with Client(
        firewall='192.168.10.20',
        port=443,  # default
        credential_file='/tmp/.opnsense.txt',
        # token='0pWN/C3tnXem6OoOp0zc9K5GUBoqBKCZ8jj8nc4LEjbFixjM0ELgEyXnb4BIqVgGNunuX0uLThblgp9Z',
        # secret='Vod5ug1kdSu3KlrYSzIZV9Ae9YFMgugCIZdIIYpefPQVhvp6KKuT7ugUIxCeKGvN6tj9uqduOzOzUlv',
    ) as c:
        c.test()
