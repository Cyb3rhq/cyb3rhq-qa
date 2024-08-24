Ansible Role: Filebeat for Elastic Stack
------------------------------------

An Ansible Role that installs [Filebeat-oss](https://www.elastic.co/products/beats/filebeat), this can be used in conjunction with [ansible-cyb3rhq-manager](https://github.com/cyb3rhq/cyb3rhq-ansible/ansible-cyb3rhq-server).

Requirements
------------

This role will work on:
 * Red Hat
 * CentOS
 * Fedora
 * Debian
 * Ubuntu

Role Variables
--------------

Available variables are listed below, along with default values (see `defaults/main.yml`):

```
  filebeat_output_indexer_hosts:
    - "localhost:9200"

```

License and copyright
---------------------

CYB3RHQ Copyright (C) 2016, Cyb3rhq Inc. (License GPLv3)

### Based on previous work from geerlingguy

 - https://github.com/geerlingguy/ansible-role-filebeat

### Modified by Cyb3rhq

The playbooks have been modified by Cyb3rhq, including some specific requirements, templates and configuration to improve integration with Cyb3rhq ecosystem.
