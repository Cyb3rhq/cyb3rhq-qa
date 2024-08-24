'''
copyright: Copyright (C) 2015-2022, Cyb3rhq Inc.

           Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.

           This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

type: reliability

brief: All Cyb3rhq components generate log messages. These can be DEBUG, WARNING, ERROR, CRITICAL. 
       Unexpected errors/warnings/critical should not be generated.

tier: 0

modules:
    - active_response
    - agentd
    - analysisd
    - api
    - authd
    - cluster
    - fim
    - gcloud
    - github
    - logcollector
    - logtest
    - office365
    - remoted
    - rids
    - rootcheck
    - vulnerability_detector
    - cyb3rhq_db
    - wpk

components:
    - agent
    - manager

daemons:
    - cyb3rhq-agentd
    - cyb3rhq-agentlessd
    - cyb3rhq-analysisd
    - cyb3rhq-authd
    - cyb3rhq-csyslogd
    - cyb3rhq-apid
    - cyb3rhq-clusterd
    - cyb3rhq-db
    - cyb3rhq-dbd
    - cyb3rhq-execd
    - cyb3rhq-integratord
    - cyb3rhq-logcollector
    - cyb3rhq-maild
    - cyb3rhq-monitord
    - cyb3rhq-modulesd
    - cyb3rhq-remoted
    - cyb3rhq-reportd
    - cyb3rhq-syscheckd

os_platform:
    - linux
    - windows

os_version:
    - Arch Linux
    - Amazon Linux 2
    - Amazon Linux 1
    - CentOS 8
    - CentOS 7
    - CentOS 6
    - Ubuntu Focal
    - Ubuntu Bionic
    - Ubuntu Xenial
    - Ubuntu Trusty
    - Debian Buster
    - Debian Stretch
    - Debian Jessie
    - Debian Wheezy
    - Red Hat 8
    - Red Hat 7
    - Red Hat 6
    - macOS Server
    - macOS Catalina
    - macOS Sierra
    - Windows XP
    - Windows 7
    - Windows 8
    - Windows 10
    - Windows Server 2003
    - Windows Server 2012
    - Windows Server 2016
    - Windows Server 2019
'''
import json
import os
import re

import pytest

from cyb3rhq_testing import global_parameters

error_codes = ['warning', 'error', 'critical']
known_messages_filename = 'know_messages.json'
known_messages_path = os.path.join(os.path.dirname(__file__), known_messages_filename)


target = ['agents', 'managers'] if not global_parameters.target_hosts else global_parameters.target_hosts


def get_log_daemon(log_line):
    pattern = re.compile(".*\d+\/\d+\/\d+ \d+:\d+:\d+ (.*?):")
    if pattern.match(log_line):
        return pattern.match(log_line).group(1)
    else:
        return None


@pytest.mark.parametrize('code', error_codes)
@pytest.mark.parametrize('target', target)
def test_error_messages(get_report, code, target):
    '''
    description: Check if unexpected error, warning or critical occurs in the environment

    cyb3rhq_min_version: 4.4.0

    parameters:
        - get_report:
            type: fixture
            brief: Get the JSON environment report.

    assertions:
        - Verify that no unexpected warning, error or critical appears in any of the hosts.

    input_description: JSON environment reports

    expected_output:
        - None
    '''
    unexpected_errors = []
    with open(known_messages_path) as f:
        expected_error_messages = json.loads(f.read())

    for target_messages in get_report[target][code]:
        for error_messages in target_messages.values():
            for error_message in error_messages:
                target_message = True
                if global_parameters.target_daemons:
                    target_message = False
                    for daemon in global_parameters.target_daemons:
                        if get_log_daemon(error_message) == daemon:
                            target_message = True
                            break            
                if target_message:
                    known_error = False
                    if expected_error_messages[code]:
                        combined_known_regex = '(' + ')|('.join(expected_error_messages[code]) + ')'
                        known_error = re.match(combined_known_regex, error_message)

                    if not known_error:
                        unexpected_errors += [error_message]

    assert not unexpected_errors, f"Unexpected error message detected {unexpected_errors}"
