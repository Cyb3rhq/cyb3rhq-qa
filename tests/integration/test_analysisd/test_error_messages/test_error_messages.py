'''
copyright: Copyright (C) 2015-2022, Cyb3rhq Inc.

           Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.

           This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

type: integration

brief: The 'cyb3rhq-analysisd' daemon receives the log messages and compares them to the rules.
       It then creates an alert when a log message matches an applicable rule.
       Specifically, these tests will check if the 'cyb3rhq-analysisd' daemon handles correctly
       the invalid events it receives.

components:
    - analysisd

suite: error_messages

targets:
    - manager

daemons:
    - cyb3rhq-analysisd
    - cyb3rhq-db

os_platform:
    - linux

os_version:
    - Arch Linux
    - Amazon Linux 2
    - Amazon Linux 1
    - CentOS 8
    - CentOS 7
    - Debian Buster
    - Red Hat 8
    - Ubuntu Focal
    - Ubuntu Bionic

references:
    - https://documentation.cyb3rhq.com/current/user-manual/reference/daemons/cyb3rhq-analysisd.html

tags:
    - events
'''
import os

import pytest
import yaml
from cyb3rhq_testing import global_parameters
from cyb3rhq_testing.analysis import callback_fim_error
from cyb3rhq_testing.tools import LOG_FILE_PATH, CYB3RHQ_PATH
from cyb3rhq_testing.tools.monitoring import ManInTheMiddle

# Marks

pytestmark = [pytest.mark.linux, pytest.mark.tier(level=0), pytest.mark.server]

# Configurations

test_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
messages_path = os.path.join(test_data_path, 'error_messages.yaml')
with open(messages_path) as f:
    test_cases = yaml.safe_load(f)

# Variables

log_monitor_paths = [LOG_FILE_PATH]
analysis_path = os.path.join(os.path.join(CYB3RHQ_PATH, 'queue', 'sockets', 'queue'))

receiver_sockets_params = [(analysis_path, 'AF_UNIX', 'UDP')]

mitm_analysisd = ManInTheMiddle(address=analysis_path, family='AF_UNIX', connection_protocol='UDP')
# monitored_sockets_params is a List of daemons to start with optional ManInTheMiddle to monitor
# List items -> (cyb3rhq_daemon: str,(
#                mitm: ManInTheMiddle
#                daemon_first: bool))
# Example1 -> ('cyb3rhq-clusterd', None)              Only start cyb3rhq-clusterd with no MITM
# Example2 -> ('cyb3rhq-clusterd', (my_mitm, True))   Start MITM and then cyb3rhq-clusterd
monitored_sockets_params = [('cyb3rhq-analysisd', mitm_analysisd, True)]

receiver_sockets, monitored_sockets, log_monitors = None, None, None  # Set in the fixtures


# Tests

@pytest.mark.parametrize('test_case',
                         [test_case['test_case'] for test_case in test_cases],
                         ids=[test_case['name'] for test_case in test_cases])
def test_error_messages(configure_sockets_environment, connect_to_sockets_module, wait_for_analysisd_startup,
                        test_case: list):
    '''
    description: Check if when the 'cyb3rhq-analysisd' daemon socket receives a message with an invalid event,
                 it generates the corresponding error that sends to the 'cyb3rhq-db' daemon socket.

    cyb3rhq_min_version: 4.2.0

    tier: 2

    parameters:
        - configure_sockets_environment:
            type: fixture
            brief: Configure environment for sockets and MITM.
        - connect_to_sockets_module:
            type: fixture
            brief: Module scope version of 'connect_to_sockets' fixture.
        - wait_for_analysisd_startup:
            type: fixture
            brief: Wait until the 'cyb3rhq-analysisd' has begun and the 'alerts.json' file is created.
        - test_case:
            type: list
            brief: List of tests to be performed.

    assertions:
        - Verify that the errors messages generated are consistent with the events received.

    input_description: Different test cases that are contained in an external YAML file (error_messages.yaml)
                       that includes 'syscheck' events data and the expected output.

    expected_output:
        - Multiple messages (error logs) corresponding to each test case,
          located in the external input data file.

    tags:
        - errors
        - man_in_the_middle
        - wdb_socket
    '''
    for stage in test_case:
        receiver_sockets[0].send(stage['input'])
        result = log_monitors[0].start(timeout=4 * global_parameters.default_timeout,
                                       callback=callback_fim_error).result()
        assert result == stage['output'], 'Failed test case stage {}: {}'.format(test_case.index(stage) + 1,
                                                                                 stage['stage'])
