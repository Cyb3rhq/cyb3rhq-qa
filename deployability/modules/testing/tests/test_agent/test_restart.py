# Copyright (C) 2015, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import re
import pytest

from modules.testing.utils import logger
from ..helpers.agent import Cyb3rhqAgent
from ..helpers.generic import GeneralComponentActions, HostInformation
from ..helpers.manager import Cyb3rhqManager
from ..helpers.utils import Utils

@pytest.fixture(scope="module", autouse=True)
def cyb3rhq_params(request):
    cyb3rhq_version = request.config.getoption('--cyb3rhq_version')
    cyb3rhq_revision = request.config.getoption('--cyb3rhq_revision')
    dependencies = request.config.getoption('--dependencies')
    targets = request.config.getoption('--targets')
    live = request.config.getoption('--live')

    return {
        'cyb3rhq_version': cyb3rhq_version,
        'cyb3rhq_revision': cyb3rhq_revision,
        'dependencies': dependencies,
        'targets': targets,
        'live': live
    }


@pytest.fixture(scope="module", autouse=True)
def setup_test_environment(cyb3rhq_params):
    targets = cyb3rhq_params['targets']
    # Clean the string and split it into key-value pairs
    targets = targets.replace(' ', '')
    targets = targets.replace('  ', '')
    pairs = [pair.strip() for pair in targets.strip('{}').split(',')]
    targets_dict = dict(pair.split(':') for pair in pairs)

    cyb3rhq_params['master'] = targets_dict.get('cyb3rhq-1')
    cyb3rhq_params['workers'] = [value for key, value in targets_dict.items() if key.startswith('cyb3rhq-') and key != 'cyb3rhq-1']
    cyb3rhq_params['agents'] = [value for key, value in targets_dict.items() if key.startswith('agent')]
    cyb3rhq_params['indexers'] = [value for key, value in targets_dict.items() if key.startswith('node-')]
    cyb3rhq_params['dashboard'] = targets_dict.get('dashboard', cyb3rhq_params['master'])

    # If there are no indexers, we choose cyb3rhq-1 by default
    if not cyb3rhq_params['indexers']:
        cyb3rhq_params['indexers'].append(cyb3rhq_params['master'])

    cyb3rhq_params['managers'] = {key: value for key, value in targets_dict.items() if key.startswith('cyb3rhq-')}
    cyb3rhq_params['agents'] = {key + '-' + re.findall(r'agent-(.*?)/', value)[0].replace('.',''): value for key, value in targets_dict.items() if key.startswith('agent')}

    updated_agents = {}
    for agent_name, agent_params in cyb3rhq_params['agents'].items():
        Utils.check_inventory_connection(agent_params)
        if GeneralComponentActions.is_component_active(agent_params, 'cyb3rhq-agent') and GeneralComponentActions.has_agent_client_keys(agent_params):
            if HostInformation.get_client_keys(agent_params) != []:
                client_name = HostInformation.get_client_keys(agent_params)[0]['name']
                updated_agents[client_name] = agent_params
            else:
                updated_agents[agent_name] = agent_params
        if updated_agents != {}:
            cyb3rhq_params['agents'] = updated_agents

def test_restart(cyb3rhq_params):
    for _, agent_params in cyb3rhq_params['agents'].items():
        GeneralComponentActions.component_restart(agent_params, 'cyb3rhq-agent')


def test_status(cyb3rhq_params):
    for agent_names, agent_params in cyb3rhq_params['agents'].items():
        status = GeneralComponentActions.get_component_status(agent_params, 'cyb3rhq-agent')
        valid_statuses = ['active', 'Running', 'is running']
        assert any(valid_status in status for valid_status in valid_statuses), logger.error(f'{agent_names} is not active by command')


def test_connection(cyb3rhq_params):
    for agent_names, _ in cyb3rhq_params['agents'].items():
        assert agent_names in Cyb3rhqManager.get_agent_control_info(cyb3rhq_params['master']), logger.error(f'{agent_names} is not present in agent_control information')


def test_isActive(cyb3rhq_params):
    for agent_names, agent_params in cyb3rhq_params['agents'].items():
        assert GeneralComponentActions.is_component_active(agent_params, 'cyb3rhq-agent'), logger.error(f'{agent_names} is not active by command')


def test_clientKeys(cyb3rhq_params):
    for agent_names, agent_params in cyb3rhq_params['agents'].items():
        assert GeneralComponentActions.has_agent_client_keys(agent_params), logger.error(f'{agent_names} has not ClientKeys file')


def test_port(cyb3rhq_params):
    for _, agent_params in cyb3rhq_params['agents'].items():
        assert Cyb3rhqAgent.is_agent_port_open(agent_params), logger.error('Port is closed')


def test_processes(cyb3rhq_params):
    for _, agent_params in cyb3rhq_params['agents'].items():
        assert Cyb3rhqAgent.are_agent_processes_active(agent_params), logger.error('Agent processes are not active')