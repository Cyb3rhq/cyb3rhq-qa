'''
copyright: Copyright (C) 2015-2022, Cyb3rhq Inc.
           Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
           This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

type: integration

brief: The 'cyb3rhq-remoted' program is the server side daemon that communicates with the agents.
       Specifically, this test will check if 'cyb3rhq-remoted' can receive syslog messages through
       the socket.

components:
    - remoted

suite: socket_communication

targets:
    - manager

daemons:
    - cyb3rhq-remoted

os_platform:
    - linux
    - windows

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
    - Windows 10
    - Windows Server 2019
    - Windows Server 2016

references:
    - https://documentation.cyb3rhq.com/current/user-manual/reference/daemons/cyb3rhq-remoted.html

tags:
    - remoted
'''
import os
import re
import pytest
from time import sleep

from cyb3rhq_testing import ARCHIVES_JSON_PATH
from cyb3rhq_testing.tools import file
from cyb3rhq_testing.tools.configuration import load_configuration_template, get_test_cases_data
from cyb3rhq_testing.tools.run_simulator import syslog_simulator
from cyb3rhq_testing.tools.thread_executor import ThreadExecutor


pytestmark = [pytest.mark.tier(level=0)]

# Reference paths
TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
CONFIGURATIONS_PATH = os.path.join(TEST_DATA_PATH, 'configuration_template')
TEST_CASES_PATH = os.path.join(TEST_DATA_PATH, 'test_cases')
SYSLOG_SIMULATOR_START_TIME = 2

# Configuration and cases data
t1_configurations_path = os.path.join(CONFIGURATIONS_PATH, 'configuration_syslog_message_parser.yaml')
t1_cases_path = os.path.join(TEST_CASES_PATH, 'cases_syslog_message_parser.yaml')

# Syslog message IPV6 values test configurations (t1)
t1_configurations_parameters, t1_configurations_metadata, t1_cases_ids = get_test_cases_data(t1_cases_path)
t1_configurations = load_configuration_template(t1_configurations_path, t1_configurations_parameters,
                                                t1_configurations_metadata)


@pytest.mark.parametrize('configuration, metadata', zip(t1_configurations, t1_configurations_metadata),
                         ids=t1_cases_ids)
def test_syslog_message_parser(configuration, metadata, set_cyb3rhq_configuration, truncate_event_logs,
                               restart_cyb3rhq_daemon_function):
    '''
    description: Check if 'cyb3rhq-remoted' can receive syslog messages through the socket.

    test_phases:
        - setup:
            - Apply ossec.conf configuration changes according to the configuration template and use case.
            - Truncate cyb3rhq event logs.
            - Restart cyb3rhq-manager service to apply configuration changes.
        - test:
            - Check that the messages are parsed correctly in the archives.json file.
        - teardown:
            - Truncate cyb3rhq logs.
            - Restore initial configuration, both ossec.conf and local_internal_options.conf.

    cyb3rhq_min_version: 4.4.0

    parameters:
        - configuration:
            type: dict
            brief: Get configurations from the module.
        - metadata:
            type: dict
            brief: Get metadata from the module.
        - set_cyb3rhq_configuration:
            type: fixture
            brief: Apply changes to the ossec.conf configuration.
        - truncate_event_logs:
            type: fixture
            brief: Truncate cyb3rhq event logs.
        - restart_cyb3rhq_daemon_function:
            type: fixture
            brief: Restart the cyb3rhq service.

    assertions:
        - Verify the syslog message is received and parsed correctly.

    input_description:
        - The `configuration_syslog_message_parser` file provides the module configuration for this
          test.
        - The `cases_syslog_message_parser` file provides the test cases.

    expected_output:
        - fr'"full_log":"{message}".*"location":"{location}"'
    '''
    # Set syslog simulator parameters according to the use case data
    syslog_simulator_parameters = {'address': metadata['address'], 'port': metadata['port'],
                                   'protocol': metadata['protocol'],
                                   'messages_number': metadata['messages_number'],
                                   'message': metadata['message']}

    # Run syslog simulator thread
    syslog_simulator_thread = ThreadExecutor(syslog_simulator, {'parameters': syslog_simulator_parameters})
    syslog_simulator_thread.start()

    # Wait until syslog simulator is started
    sleep(SYSLOG_SIMULATOR_START_TIME)

    # Read the events log data
    events_data = file.read_file(ARCHIVES_JSON_PATH).split('\n')

    message = metadata['message']
    location = metadata['address']
    find_msg = (fr'"full_log":"{message}".*"location":"{location}"').replace('"', r'\"')

    event_msg = [event for event in events_data if bool(re.match(fr".*{find_msg}.*", event))]

    assert len(event_msg) == metadata['messages_number'], "The event's format is not the expected one"

    # Wait until syslog simulator ends
    syslog_simulator_thread.join()
