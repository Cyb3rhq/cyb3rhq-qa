# Copyright (C) 2015, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import pytest

from modules.testing.utils import logger
from ..helpers.generic import HostInformation, GeneralComponentActions
from ..helpers.manager import Cyb3rhqManager
from ..helpers.dashboard import Cyb3rhqDashboard
from ..helpers.indexer import Cyb3rhqIndexer


@pytest.fixture(scope="module", autouse=True)
def cyb3rhq_params(request):
    cyb3rhq_version = request.config.getoption('--cyb3rhq_version')
    cyb3rhq_revision = request.config.getoption('--cyb3rhq_revision')
    dependencies = request.config.getoption('--dependencies')
    targets = request.config.getoption('--targets')

    params = {
        'cyb3rhq_version': cyb3rhq_version,
        'cyb3rhq_revision': cyb3rhq_revision,
        'dependencies': dependencies,
        'targets': targets
    }
    yield params
    logger.info('Restoring Cyb3rhq central components statuses')
    GeneralComponentActions.component_restart(params['master'], 'cyb3rhq-manager')

    for indexer_params in params['indexers']:
        GeneralComponentActions.component_restart(indexer_params, 'cyb3rhq-indexer')

    GeneralComponentActions.component_restart(params['dashboard'], 'cyb3rhq-dashboard')
    GeneralComponentActions.component_restart(params['master'], 'filebeat')


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
    cyb3rhq_params['indexers'] = [value for key, value in targets_dict.items() if key.startswith('node-')]
    cyb3rhq_params['dashboard'] = targets_dict.get('dashboard', cyb3rhq_params['master'])

    # If there are no indexers, we choose cyb3rhq-1 by default
    if not cyb3rhq_params['indexers']:
        cyb3rhq_params['indexers'].append(cyb3rhq_params['master'])

    cyb3rhq_params['managers'] = {key: value for key, value in targets_dict.items() if key.startswith('cyb3rhq-')}

def test_stop(cyb3rhq_params):
    GeneralComponentActions.component_stop(cyb3rhq_params['master'], 'cyb3rhq-manager')

    for indexer_params in cyb3rhq_params['indexers']:
        GeneralComponentActions.component_stop(indexer_params, 'cyb3rhq-indexer')

    GeneralComponentActions.component_stop(cyb3rhq_params['dashboard'], 'cyb3rhq-dashboard')
    GeneralComponentActions.component_stop(cyb3rhq_params['master'], 'filebeat')

def test_manager_status(cyb3rhq_params):
    assert 'inactive' in GeneralComponentActions.get_component_status(cyb3rhq_params['master'], 'cyb3rhq-manager'), logger.error(f"The Cyb3rhq manager in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['master'])} is not active")


def test_dashboard_status(cyb3rhq_params):
    assert 'inactive' in GeneralComponentActions.get_component_status(cyb3rhq_params['dashboard'], 'cyb3rhq-dashboard'), logger.error(f"The Cyb3rhq dashboard in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['dashboard'])} is not active")


def test_indexer_status(cyb3rhq_params):
    for indexer_params in cyb3rhq_params['indexers']:
        assert 'inactive' in GeneralComponentActions.get_component_status(indexer_params, 'cyb3rhq-indexer'), logger.error(f'The Cyb3rhq indexer in {HostInformation.get_os_name_and_version_from_inventory(indexer_params)} is not active')


def test_filebeat_status(cyb3rhq_params):
    assert 'inactive' in GeneralComponentActions.get_component_status(cyb3rhq_params['master'], 'filebeat'), logger.error(f"The Filebeat in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['master'])} is not active")


def test_manager_api_port(cyb3rhq_params):
    assert not Cyb3rhqManager.is_cyb3rhq_api_port_open(cyb3rhq_params['master'], cycles=1, wait=1), logger.error(f"The Cyb3rhq manager API port in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['master'])} is still active")


def test_manager_agent_port(cyb3rhq_params):
    assert not Cyb3rhqManager.is_cyb3rhq_agent_port_open(cyb3rhq_params['master'], cycles=1, wait=1), logger.error(f"The Cyb3rhq manager port in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['master'])} is still active")


def test_manager_agent_enrollment_port(cyb3rhq_params):
    assert not Cyb3rhqManager.is_cyb3rhq_agent_enrollment_port_open(cyb3rhq_params['master'], cycles=1, wait=1), logger.error(f"The Cyb3rhq manager agent enrollment port in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['master'])} is still active")


def test_dashboard_port(cyb3rhq_params):
    assert not Cyb3rhqDashboard.is_dashboard_port_open(cyb3rhq_params['dashboard'], cycles=1, wait=1), logger.error(f"The Cyb3rhq dashboard port in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['dashboard'])} is still active")


def test_indexer_port(cyb3rhq_params):
    for indexer_params in cyb3rhq_params['indexers']:
        assert not Cyb3rhqIndexer.is_indexer_port_open(indexer_params, cycles=1, wait=1), logger.error(f"Some Cyb3rhq indexer port in {HostInformation.get_os_name_and_version_from_inventory(indexer_params)} is still active")
