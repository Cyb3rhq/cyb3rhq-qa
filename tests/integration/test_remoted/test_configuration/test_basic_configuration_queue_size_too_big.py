'''
copyright: Copyright (C) 2015-2022, Cyb3rhq Inc.
           Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
           This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

type: integration

brief: The 'cyb3rhq-remoted' program is the server side daemon that communicates with the agents.
       Specifically, this test will check that a warning message is produced when 'cyb3rhq-remoted'
       sets the queue size too big (greater than 262144)

components:
    - remoted

suite: configuration

targets:
    - manager

daemons:
    - cyb3rhq-remoted

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
    - https://documentation.cyb3rhq.com/current/user-manual/reference/daemons/cyb3rhq-remoted.html
    - https://documentation.cyb3rhq.com/current/user-manual/reference/ossec-conf/remote.html
    - https://documentation.cyb3rhq.com/current/user-manual/agents/agent-life-cycle.html
    - https://documentation.cyb3rhq.com/current/user-manual/capabilities/agent-key-polling.html

tags:
    - remoted
'''
import os
import pytest

import cyb3rhq_testing.remote as remote
from cyb3rhq_testing.api import compare_config_api_response

from cyb3rhq_testing.tools.configuration import load_cyb3rhq_configurations
from urllib3.exceptions import InsecureRequestWarning
import requests

# Marks
pytestmark = [pytest.mark.server, pytest.mark.tier(level=0)]

# Configuration
test_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
configurations_path = os.path.join(test_data_path, 'cyb3rhq_basic_configuration.yaml')

# Setting parameters for testing queue_size too big
parameters = [
    {'CONNECTION': 'secure', 'PORT': '1514', 'QUEUE_SIZE': '99999999'}
]

metadata = [
    {'connection': 'secure', 'port': '1514', 'queue_size': '99999999'}
]

configurations = load_cyb3rhq_configurations(configurations_path, "test_basic_configuration_queue_size",
                                           params=parameters,
                                           metadata=metadata)

configuration_ids = [f"{x['CONNECTION'], x['PORT'], x['QUEUE_SIZE']}" for x in parameters]


# fixtures
@pytest.fixture(scope="module", params=configurations, ids=configuration_ids)
def get_configuration(request):
    """Get configurations from the module."""
    return request.param


def test_big_queue_size(get_configuration, configure_environment, restart_remoted, wait_for_remoted_start_log):
    '''
    description: Check that when 'cyb3rhq-remoted' sets the queue size too big(greater than 262144), a warning message
                 appears. For this purpose, it uses the configuration from test cases, check if the warning has been
                 logged and the configuration is the same as the API respnse.

    cyb3rhq_min_version: 4.2.0

    tier: 0

    parameters:
        - get_configuration:
            type: fixture
            brief: Get configurations from the module.
        - configure_environment:
            type: fixture
            brief: Configure a custom environment for testing. Restart Cyb3rhq is needed for applying the configuration.
        - restart_remoted:
            type: fixture
            brief: Clear the 'ossec.log' file and start a new monitor.

    assertions:
        - Verify that remoted starts correctly.
        - Verify that the API query matches correctly with the configuration that ossec.conf contains.
        - Verify that the warning is logged when the queue size is too big.
        - Verify that the selected configuration is the same as the API response.

    input_description: A configuration template (test_basic_configuration_queue_size) is contained in an external YAML
                       file, (cyb3rhq_basic_configuration.yaml). That template is combined with different test cases
                       defined in the module. Those include configuration settings for the 'cyb3rhq-remoted' daemon and
                       agents info.

    expected_output:
        - r'Started <pid>: .* Listening on port .*'
        - r'API query '{protocol}://{host}:{port}/manager/configuration?section=remote' doesn't match the
          introduced configuration on ossec.conf.'
        - The expected error output has not been produced
        - 'WARNING: Queue size is very high. The application may run out of memory'

    tags:
        - simulator
    '''
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    cfg = get_configuration['metadata']

    log_callback = remote.callback_queue_size_too_big()
    cyb3rhq_log_monitor.start(timeout=5, callback=log_callback,
                            error_message="The expected error output has not been produced")

    compare_config_api_response([cfg], 'remote')
