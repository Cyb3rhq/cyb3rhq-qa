'''
copyright: Copyright (C) 2015-2022, Cyb3rhq Inc.

           Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.

           This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

type: integration

brief: These tests will check if the 'cyb3rhq-authd' daemon correctly handles the enrollment requests,
       generating consistent responses to the requests received on its IP v4 network socket.
       The 'cyb3rhq-authd' daemon can automatically add a Cyb3rhq agent to a Cyb3rhq manager and provide
       the key to the agent. It is used along with the 'agent-auth' application.

components:
    - authd

targets:
    - manager

daemons:
    - cyb3rhq-authd
    - cyb3rhq-db
    - cyb3rhq-modulesd

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
    - https://documentation.cyb3rhq.com/current/user-manual/reference/daemons/cyb3rhq-authd.html
    - https://documentation.cyb3rhq.com/current/user-manual/reference/tools/agent_groups.html

tags:
    - enrollment
'''
import os
import subprocess
import time

import pytest
from cyb3rhq_testing.tools.configuration import load_cyb3rhq_configurations
from cyb3rhq_testing.tools.file import read_yaml

# Marks

pytestmark = [pytest.mark.linux, pytest.mark.tier(level=0), pytest.mark.server]


# Configurations

test_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
message_tests = read_yaml(os.path.join(test_data_path, 'enroll_messages.yaml'))
configurations_path = os.path.join(test_data_path, 'cyb3rhq_authd_configuration.yaml')
configurations = load_cyb3rhq_configurations(configurations_path, __name__, params=None, metadata=None)

# Variables
log_monitor_paths = []

receiver_sockets_params = [(("localhost", 1515), 'AF_INET', 'SSL_TLSv1_2')]

monitored_sockets_params = [('cyb3rhq-modulesd', None, True), ('cyb3rhq-db', None, True), ('cyb3rhq-authd', None, True)]

receiver_sockets, monitored_sockets, log_monitors = None, None, None  # Set in the fixtures


# Tests

@pytest.fixture(scope="function", params=message_tests)
def set_up_groups(request):
    groups = request.param.get('groups', [])
    for group in groups:
        subprocess.call(['/var/ossec/bin/agent_groups', '-a', '-g', f'{group}', '-q'])
    yield request.param
    for group in groups:
        subprocess.call(['/var/ossec/bin/agent_groups', '-r', '-g', f'{group}', '-q'])


@pytest.fixture(scope="module", params=configurations)
def get_configuration(request):
    """Get configurations from the module"""
    yield request.param


def test_ossec_auth_messages(get_configuration, set_up_groups, configure_environment, configure_sockets_environment,
                             clean_client_keys_file_module, restart_cyb3rhq_daemon, wait_for_authd_startup_module,
                             connect_to_sockets_module):
    '''
    description:
        Checks if when the `cyb3rhq-authd` daemon receives different types of enrollment requests,
        it responds appropriately to them. In this case, the enrollment requests are sent to
        an IP v4 network socket.

    cyb3rhq_min_version:
        4.2.0

    tier: 0

    parameters:
        - get_configuration:
            type: fixture
            brief: Get configurations from the module.
        - set_up_groups:
            type: fixture
            brief: Create a testing group for agents and provide the test case list.
        - configure_environment:
            type: fixture
            brief: Configure a custom environment for testing.
        - configure_sockets_environment:
            type: fixture
            brief: Configure environment for sockets and MITM.
        - clean_client_keys_file_module:
            type: fixture
            brief: Stops Cyb3rhq and cleans any previous key in client.keys file at module scope.
        - restart_authd:
            type: fixture
            brief: Restart the 'cyb3rhq-authd' daemon, clear the 'ossec.log' file and start a new file monitor.
        - wait_for_authd_startup_module:
            type: fixture
            brief: Waits until Authd is accepting connections.
        - connect_to_sockets_module:
            type: fixture
            brief: Module scope version of 'connect_to_sockets' fixture.


    assertions:
        - Verify that the response messages are consistent with the enrollment requests received.

    input_description:
        Different test cases are contained in an external `YAML` file (enroll_messages.yaml)
        that includes enrollment events and the expected output.

    expected_output:
        - Multiple values located in the `enroll_messages.yaml` file.

    tags:
        - keys
        - ssl
    '''
    test_case = set_up_groups['test_case']
    for stage in test_case:
        # Reopen socket (socket is closed by manager after sending message with client key)
        receiver_sockets[0].open()
        expected = stage['output']
        message = stage['input']
        receiver_sockets[0].send(message, size=False)
        timeout = time.time() + 10
        response = ''
        while response == '':
            response = receiver_sockets[0].receive().decode()
            if time.time() > timeout:
                assert response != '', 'The manager did not respond to the message sent.'
        assert response[:len(expected)] == expected, \
            'Failed test case {}: Response was: {} instead of: {}'.format(set_up_groups['name'], response, expected)
