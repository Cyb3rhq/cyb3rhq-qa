# Copyright (C) 2015-2022, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

import os

import pytest
from cyb3rhq_testing.tools import CYB3RHQ_PATH, CYB3RHQ_LOGS_PATH
from cyb3rhq_testing.tools.system_monitoring import HostMonitor
from cyb3rhq_testing.tools.system import HostManager


pytestmark = [pytest.mark.cluster, pytest.mark.enrollment_cluster_env]

# Hosts
testinfra_hosts = ["cyb3rhq-master", "cyb3rhq-worker1", "cyb3rhq-agent1"]

inventory_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                              'provisioning', 'enrollment_cluster', 'inventory.yml')
host_manager = HostManager(inventory_path)
local_path = os.path.dirname(os.path.abspath(__file__))
messages_path = os.path.join(local_path, 'data/messages.yml')
tmp_path = os.path.join(local_path, 'tmp')


# Remove the agent once the test has finished
@pytest.fixture(scope='module')
def clean_environment():

    yield

    host_manager.control_service(host='cyb3rhq-agent1', service='cyb3rhq', state="stopped")
    agent_id = host_manager.run_command('cyb3rhq-master', f'cut -c 1-3 {CYB3RHQ_PATH}/etc/client.keys')
    host_manager.get_host('cyb3rhq-master').ansible("command", f'{CYB3RHQ_PATH}/bin/manage_agents -r {agent_id}',
                                                  check=False)
    host_manager.clear_file(host='cyb3rhq-agent1', file_path=os.path.join(CYB3RHQ_PATH, 'etc', 'client.keys'))
    host_manager.clear_file(host='cyb3rhq-agent1', file_path=os.path.join(CYB3RHQ_LOGS_PATH, 'ossec.log'))


def test_agent_enrollment(clean_environment):
    """Check agent enrollment process works as expected. An agent pointing to a worker should be able to register itself
    into the master by starting Cyb3rhq-agent process."""
    # Clean ossec.log and cluster.log
    host_manager.clear_file(host='cyb3rhq-master', file_path=os.path.join(CYB3RHQ_LOGS_PATH, 'ossec.log'))
    host_manager.clear_file(host='cyb3rhq-worker1', file_path=os.path.join(CYB3RHQ_LOGS_PATH, 'ossec.log'))
    host_manager.clear_file(host='cyb3rhq-master', file_path=os.path.join(CYB3RHQ_LOGS_PATH, 'cluster.log'))
    host_manager.clear_file(host='cyb3rhq-worker1', file_path=os.path.join(CYB3RHQ_LOGS_PATH, 'cluster.log'))

    # Start the agent enrollment process by restarting the cyb3rhq-agent
    host_manager.control_service(host='cyb3rhq-master', service='cyb3rhq', state="restarted")
    host_manager.control_service(host='cyb3rhq-worker1', service='cyb3rhq', state="restarted")
    host_manager.control_service(host='cyb3rhq-agent1', service='cyb3rhq', state="restarted")

    # Run the callback checks for the ossec.log and the cluster.log
    HostMonitor(inventory_path=inventory_path,
                messages_path=messages_path,
                tmp_path=tmp_path).run()

    # Make sure the worker's client.keys is not empty
    assert host_manager.get_file_content('cyb3rhq-worker1', os.path.join(CYB3RHQ_PATH, 'etc', 'client.keys'))

    # Make sure the agent's client.keys is not empty
    assert host_manager.get_file_content('cyb3rhq-agent1', os.path.join(CYB3RHQ_PATH, 'etc', 'client.keys'))

    # Check if the agent is active
    agent_id = host_manager.run_command('cyb3rhq-master', f'cut -c 1-3 {CYB3RHQ_PATH}/etc/client.keys')
    assert host_manager.run_command('cyb3rhq-master', f'{CYB3RHQ_PATH}/bin/agent_control -i {agent_id} | grep Active')
