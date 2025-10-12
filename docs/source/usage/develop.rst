.. _usage_develop:

.. include:: ../_include/head.rst

=======
Develop
=======

.. warning::

    This documentation is work-in-progress.

Features
########

Module-implementations and module-specific features should be contributed to `the upstream repository <https://github.com/O-X-L/ansible-opnsense>`_!

----

Sync from Upstream
##################

The script `update.sh <https://github.com/O-X-L/opnsense-api-client/blob/latest/scripts/update.sh>`_ is used to update the modules to the latest state of the upstream repository.

We basically replaced the abstracted features of the Ansible-framework the upstream code uses. (as we do only use basic features)

----

Test & Lint
###########

.. code-block:: bash

    # ALL
    pip install -r requirements.txt


    # LINT
    pip install -r requirements_lint.txt

    make lint
    # or
    bash scripts/lint.sh


    # UNIT TESTS
    pip install -r requirements_test.txt

    make unit-test
    # or
    bash scripts/unit_test.sh


    # FUNCTIONAL TESTS
    pip install -r requirements_test.txt

    export TEST_FIREWALL=<IP>
    export TEST_API_CREDS=/tmp/opn.txt

    make func-test
    # or
    bash scripts/functional_test.sh
