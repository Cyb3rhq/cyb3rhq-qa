'''
copyright: Copyright (C) 2015-2022, Cyb3rhq Inc.
           Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
           This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

type: integration

brief: The 'cyb3rhq-remoted' program is the server side daemon that communicates with the agents.
       Specifically, this test will check that the manager sends the ACK message after receiving
       the start-up message from the agent.

components:
    - remoted

suite: manager_messages

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
import pytest
import os
import cyb3rhq_testing.tools.agent_simulator as ag

from time import sleep
from cyb3rhq_testing import remote as rd
from cyb3rhq_testing import is_tcp_udp
from cyb3rhq_testing.tools import LOG_FILE_PATH
from cyb3rhq_testing.tools.configuration import load_cyb3rhq_configurations
from cyb3rhq_testing.tools.monitoring import FileMonitor


# Marks
pytestmark = pytest.mark.tier(level=1)

# Variables
current_test_path = os.path.dirname(os.path.realpath(__file__))
test_data_path = os.path.join(current_test_path, 'data')
configurations_path = os.path.join(test_data_path, 'cyb3rhq_manager_ack.yaml')

cyb3rhq_log_monitor = FileMonitor(LOG_FILE_PATH)

# Set configuration
parameters = [
    {'PROTOCOL': 'tcp'},
    {'PROTOCOL': 'udp'},
    {'PROTOCOL': 'tcp,udp'},
    {'PROTOCOL': 'udp,tcp'},
]

metadata = [
    {'protocol': 'tcp'},
    {'protocol': 'udp'},
    {'protocol': 'tcp,udp'},
    {'protocol': 'udp,tcp'},
]

agent_info = {
    'manager_address': '127.0.0.1',
    'os': 'debian7',
    'version': '4.2.0',
    'disable_all_modules': True
}

configuration_ids = [item['PROTOCOL'].upper() for item in parameters]

# Configuration data
configurations = load_cyb3rhq_configurations(configurations_path, __name__, params=parameters, metadata=metadata)


def check_manager_ack(protocol):
    """Allow to check if the manager sends the ACK message after receiving the start-up message from agent.

    Args:
        protocol (str): It can be UDP or TCP.

    Raises:
        TimeoutError: If agent does not receive the manager ACK message in the expected time.
    """

    # Create agent and sender object with default parameters
    agent = ag.Agent(**agent_info)

    # Sleep to avoid ConnectionRefusedError
    sleep(1)

    sender = ag.Sender(agent_info['manager_address'], protocol=protocol)

    # Activate receives_messages modules in simulated agent.
    agent.set_module_status('receive_messages', 'enabled')

    # Run injector with only receive messages module enabled
    injector = ag.Injector(sender, agent)
    try:
        injector.run()

        # Wait until remoted has loaded the new agent key
        rd.wait_to_remoted_key_update(cyb3rhq_log_monitor)

        # Send the start-up message
        sender.send_event(agent.startup_msg)

        # Check ACK manager message
        rd.check_agent_received_message(agent, '#!-agent ack')
    finally:
        injector.stop_receive()


@pytest.fixture(scope='module', params=configurations, ids=configuration_ids)
def get_configuration(request):
    """Get configurations from the module."""
    return request.param


def test_manager_ack(get_configuration, configure_environment, restart_remoted):
    '''
    description: Check if the manager sends the ACK message after receiving
                 the start-up message from the agent.
    
    cyb3rhq_min_version: 4.2.0

    tier: 1

    parameters:
        - get_configuration:
            type: fixture
            brief: Get configurations from the module.
        - configure_environment:
            type: fixture
            brief: Configure a custom environment for testing.
        - restart_remoted:
            type: fixture
            brief: Restart 'cyb3rhq-remoted' daemon in manager.
    
    assertions:
    
    input_description: A configuration template (test_manager_ack) is contained in an external YAML file,
                       (cyb3rhq_manager_ack.yaml). That template is combined with different test cases defined
                       in the module. Those include configuration settings for the 'cyb3rhq-remoted' daemon
                       and agents info.
    
    expected_output:
        - r'#!-agent ack'
    '''
    protocol = get_configuration['metadata']['protocol']

    if is_tcp_udp(protocol):
        check_manager_ack(rd.TCP)
        check_manager_ack(rd.UDP)
    else:
        check_manager_ack(protocol)
