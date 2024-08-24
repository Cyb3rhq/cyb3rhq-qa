Ansible Playbook - Cyb3rhq agent
==============================

This role will install and configure a Cyb3rhq Agent.

OS Requirements
----------------

This role is compatible with:
 * Red Hat
 * CentOS
 * Fedora
 * Debian
 * Ubuntu


Role Variables
--------------

* `cyb3rhq_managers`: Collection of Cyb3rhq Managers' IP address, port, and protocol used by the agent
* `cyb3rhq_agent_authd`: Collection with the settings to register an agent using authd.

Playbook example
----------------

The following is an example of how this role can be used:

     - hosts: all:!cyb3rhq-manager
       roles:
         - ansible-cyb3rhq-agent
       vars:
         cyb3rhq_managers:
           - address: 127.0.0.1
             port: 1514
             protocol: tcp
             api_port: 55000
             api_proto: 'http'
             api_user: 'ansible'
         cyb3rhq_agent_authd:
           registration_address: 127.0.0.1
           enable: true
           port: 1515
           ssl_agent_ca: null
           ssl_auto_negotiate: 'no'


License and copyright
---------------------

CYB3RHQ Copyright (C) 2016, Cyb3rhq Inc. (License GPLv3)

### Based on previous work from dj-wasabi

  - https://github.com/dj-wasabi/ansible-ossec-server

### Modified by Cyb3rhq

The playbooks have been modified by Cyb3rhq, including some specific requirements, templates and configuration to improve integration with Cyb3rhq ecosystem.
