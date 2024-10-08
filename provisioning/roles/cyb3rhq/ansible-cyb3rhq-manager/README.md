Ansible Playbook - Cyb3rhq manager
================================

This role will install the Cyb3rhq manager on a host.

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

This role has some variables which you can or need to override.
```
cyb3rhq_manager_fqdn: ~
cyb3rhq_manager_config: []
shared_agent_config: []
```

Vault variables
----------------

### vars/agentless_creds.yml
This file has the agenless credentials.
```
---
 agentless_creds:
 - type: ssh_integrity_check_linux
   frequency: 3600
   host: root@example.net
   state: periodic
   arguments: '/bin /etc/ /sbin'
   passwd: qwerty
```

### vars/cyb3rhq_api_creds.yml
This file has user and password created in httpasswd format.
```
---
cyb3rhq_api_user:
  - "foo:$apr1$/axqZYWQ$Xo/nz/IG3PdwV82EnfYKh/"
```

### vars/authd_pass.yml
This file has the password to be used for the authd daemon.
```
---
authd_pass: foobar
```

Default config
--------------

### defaults/main.yml
```
---
cyb3rhq_manager_fqdn: "cyb3rhq-server"

cyb3rhq_manager_config:
  json_output: 'yes'
  alerts_log: 'yes'
  logall: 'no'
  authd:
    enable: false
  email_notification: no
  mail_to:
    - admin@example.net
  mail_smtp_server: localhost
  mail_from: cyb3rhq-server@example.com
  syscheck:
    frequency: 43200
    scan_on_start: 'yes'
    ignore:
      - /etc/mtab
      - /etc/mnttab
      - /etc/hosts.deny
      - /etc/mail/statistics
      - /etc/random-seed
      - /etc/random.seed
      - /etc/adjtime
      - /etc/httpd/logs
      - /etc/utmpx
      - /etc/wtmpx
      - /etc/cups/certs
      - /etc/dumpdates
      - /etc/svc/volatile
    no_diff:
      - /etc/ssl/private.key
    directories:
      - dirs: /etc,/usr/bin,/usr/sbin
        checks: 'check_all="yes"'
      - dirs: /bin,/sbin
        checks: 'check_all="yes"'
  rootcheck:
    frequency: 43200
  openscap:
    timeout: 1800
    interval: '1d'
    scan_on_start: 'yes'
  log_level: 1
  email_level: 12
  localfiles:
    - format: 'syslog'
      location: '/var/log/messages'
    - format: 'syslog'
      location: '/var/log/secure'
    - format: 'command'
      command: 'df -P'
      frequency: '360'
    - format: 'full_command'
      command: 'netstat -tln | grep -v 127.0.0.1 | sort'
      frequency: '360'
    - format: 'full_command'
      command: 'last -n 20'
      frequency: '360'
  globals:
    - '127.0.0.1'
    - '192.168.2.1'
  connection:
    - type: 'secure'
      port: '1514'
      protocol: 'tcp'
  commands:
    - name: 'disable-account'
      executable: 'disable-account.sh'
      expect: 'user'
      timeout_allowed: 'yes'
    - name: 'restart-ossec'
      executable: 'restart-ossec.sh'
      expect: ''
      timeout_allowed: 'no'
    - name: 'firewall-drop'
      executable: 'firewall-drop.sh'
      expect: 'srcip'
      timeout_allowed: 'yes'
    - name: 'host-deny'
      executable: 'host-deny.sh'
      expect: 'srcip'
      timeout_allowed: 'yes'
    - name: 'route-null'
      executable: 'route-null.sh'
      expect: 'srcip'
      timeout_allowed: 'yes'
    - name: 'win_route-null'
      executable: 'route-null.cmd'
      expect: 'srcip'
      timeout_allowed: 'yes'
  active_responses:
    - command: 'host-deny'
      location: 'local'
      level: 6
      timeout: 600

shared_agent_config:
  - type: os
    type_value: linux
    frequency_check: 79200
    ignore_files:
      - /etc/mtab
      - /etc/mnttab
      - /etc/hosts.deny
      - /etc/mail/statistics
      - /etc/svc/volatile
    directories:
      - check_all: yes
        dirs: /etc,/usr/bin,/usr/sbin
      - check_all: yes
        dirs: /bin,/sbin
    localfiles:
      - format: 'syslog'
        location: '/var/log/messages'
      - format: 'syslog'
        location: '/var/log/secure'
      - format: 'syslog'
        location: '/var/log/maillog'
      - format: 'apache'
        location: '/var/log/httpd/error_log'
      - format: 'apache'
        location: '/var/log/httpd/access_log'
      - format: 'apache'
        location: '/var/ossec/logs/active-responses.log'
```

#### Custom variables:
You can create a YAML file and change the default variables for this role, to later using it with `-e` option in `ansible-playbooks`, for example:

```
---
cyb3rhq_manager_fqdn: "cyb3rhq-server"

cyb3rhq_manager_config:
  email_notification: yes
  mail_to:
    - myadmin@mydomain.com
  mail_smtp_server: mysmtp.mydomain.com
```

Dependencies
------------

No dependencies.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: cyb3rhq-server.example.com
      roles:
         - { role: ansible-cyb3rhq-server }

License and copyright
---------------------

CYB3RHQ Copyright (C) 2016, Cyb3rhq Inc. (License GPLv3)

### Based on previous work from dj-wasabi

 - https://github.com/dj-wasabi/ansible-ossec-server

### Modified by Cyb3rhq

The playbooks have been modified by Cyb3rhq, including some specific requirements, templates and configuration to improve integration with Cyb3rhq ecosystem.
