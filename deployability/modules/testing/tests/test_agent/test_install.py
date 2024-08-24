# Copyright (C) 2015, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import re
import pytest

from modules.testing.utils import logger
from ..helpers.agent import Cyb3rhqAgent
from ..helpers.constants import CYB3RHQ_ROOT, WINDOWS_ROOT_DIR, MACOS_ROOT_DIR
from ..helpers.generic import HostConfiguration, HostInformation, GeneralComponentActions
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

def test_installation(cyb3rhq_params):
    # Checking connection
    for _, manager_params in cyb3rhq_params['managers'].items():
        Utils.check_inventory_connection(manager_params)

    # Certs creation, firewall management and Manager installation
    for agent_name, agent_params in cyb3rhq_params['agents'].items():
        HostConfiguration.disable_firewall(agent_params)


    if HostInformation.dir_exists(cyb3rhq_params['master'], CYB3RHQ_ROOT):
        logger.info(f'Manager is already installed in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params["master"])}')
    else:
        HostConfiguration.disable_firewall(manager_params)
        HostConfiguration.certs_create(cyb3rhq_params['cyb3rhq_version'], cyb3rhq_params['master'], cyb3rhq_params['dashboard'], cyb3rhq_params['indexers'], cyb3rhq_params['workers'], cyb3rhq_params['live'])
        Cyb3rhqManager.install_manager(cyb3rhq_params['master'], 'cyb3rhq-1', cyb3rhq_params['cyb3rhq_version'], cyb3rhq_params['live'])
    assert HostInformation.dir_exists(cyb3rhq_params['master'], CYB3RHQ_ROOT), logger.error(f'The {CYB3RHQ_ROOT} is not present in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params["master"])}')

    # Agent installation
    for agent_name, agent_params in cyb3rhq_params['agents'].items():
        Cyb3rhqAgent.install_agent(agent_params, agent_name, cyb3rhq_params['cyb3rhq_version'], cyb3rhq_params['cyb3rhq_revision'], cyb3rhq_params['live'])


    # Testing installation directory
    for agent in cyb3rhq_params['agents'].values():
        os_type = HostInformation.get_os_type(agent)
        if os_type == 'linux':
            path_to_check = CYB3RHQ_ROOT
        elif os_type == 'windows':
            path_to_check = WINDOWS_ROOT_DIR
        elif os_type == 'macos':
            path_to_check = MACOS_ROOT_DIR
        assert HostInformation.dir_exists(agent, path_to_check), logger.error(f'The {path_to_check} is not present in {HostInformation.get_os_name_and_version_from_inventory(agent)}')


def test_status(cyb3rhq_params):
    for agent in cyb3rhq_params['agents'].values():
        agent_status = GeneralComponentActions.get_component_status(agent, 'cyb3rhq-agent')
        valid_statuses = ['loaded', 'Stopped', 'not running']
        assert any(valid_status in agent_status for valid_status in valid_statuses), logger.error(f'The {HostInformation.get_os_name_and_version_from_inventory(agent)} status is not loaded')
