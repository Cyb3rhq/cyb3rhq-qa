# Copyright (C) 2015, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import pytest

from modules.testing.utils import logger
from ..helpers.constants import CYB3RHQ_ROOT
from ..helpers.executor import Cyb3rhqAPI
from ..helpers.generic import HostConfiguration, HostInformation, GeneralComponentActions
from ..helpers.manager import Cyb3rhqManager
from ..helpers.indexer import Cyb3rhqIndexer
from ..helpers.dashboard import Cyb3rhqDashboard
from ..helpers.central import Cyb3rhqCentralComponents
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
    cyb3rhq_params['indexers'] = [value for key, value in targets_dict.items() if key.startswith('node-')]
    cyb3rhq_params['dashboard'] = targets_dict.get('dashboard', cyb3rhq_params['master'])

    # If there are no indexers, we choose cyb3rhq-1 by default
    if not cyb3rhq_params['indexers']:
        cyb3rhq_params['indexers'].append(cyb3rhq_params['master'])

    cyb3rhq_params['managers'] = {key: value for key, value in targets_dict.items() if key.startswith('cyb3rhq-')}


def test_installation(cyb3rhq_params):
    # Disabling firewall for all managers
    for _, manager_params in cyb3rhq_params['managers'].items():
        Utils.check_inventory_connection(manager_params)
        HostConfiguration.disable_firewall(manager_params)

    # Certs create and scp from master to worker
    HostConfiguration.certs_create(cyb3rhq_params['cyb3rhq_version'], cyb3rhq_params['master'], cyb3rhq_params['dashboard'], cyb3rhq_params['indexers'], cyb3rhq_params['workers'], cyb3rhq_params['live'])

    # Install central components and perform checkfile testing
    for _, manager_params in cyb3rhq_params['managers'].items():
        Cyb3rhqCentralComponents.install_aio(manager_params, cyb3rhq_params['cyb3rhq_version'], cyb3rhq_params['live'])

    # Validation of directory of the components
    for manager in cyb3rhq_params['managers'].values():
        assert HostInformation.dir_exists(manager, CYB3RHQ_ROOT), logger.error(f'The {CYB3RHQ_ROOT} is not present in {HostInformation.get_os_name_and_version_from_inventory(manager)}')


def test_manager_status(cyb3rhq_params):
    assert 'active' in GeneralComponentActions.get_component_status(cyb3rhq_params['master'], 'cyb3rhq-manager'), logger.error(f'The Cyb3rhq manager in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params["master"])} is not active')

def test_manager_version(cyb3rhq_params):
    for manager in cyb3rhq_params['managers'].values():
        manager_status = GeneralComponentActions.get_component_version(manager)
        assert cyb3rhq_params['cyb3rhq_version'] in manager_status, logger.error(f"The version {HostInformation.get_os_name_and_version_from_inventory(manager)} is not {cyb3rhq_params['cyb3rhq_version']} by using commands")
        cyb3rhq_api = Cyb3rhqAPI(cyb3rhq_params['master'])
        assert cyb3rhq_params['cyb3rhq_version'] in Cyb3rhqManager.get_manager_version(cyb3rhq_api), logger.error(f"The version {HostInformation.get_os_name_and_version_from_inventory(manager)} is not {cyb3rhq_params['cyb3rhq_version']} in the API")


def test_manager_revision(cyb3rhq_params):
    for manager in cyb3rhq_params['managers'].values():
        manager_status = GeneralComponentActions.get_component_revision(manager)
        assert cyb3rhq_params['cyb3rhq_revision'] in manager_status, logger.error(f"The revision {HostInformation.get_os_name_and_version_from_inventory(manager)} is not {cyb3rhq_params['cyb3rhq_revision']} by using commands")
        cyb3rhq_api = Cyb3rhqAPI(cyb3rhq_params['master'])
        assert cyb3rhq_params['cyb3rhq_revision'] in str(Cyb3rhqManager.get_manager_revision(cyb3rhq_api)), logger.error(f"The revision {HostInformation.get_os_name_and_version_from_inventory(manager)} is not {cyb3rhq_params['cyb3rhq_revision']} in the API")


def test_manager_installed_directory(cyb3rhq_params):
    for manager in cyb3rhq_params['managers'].values():
        assert HostInformation.dir_exists(manager, CYB3RHQ_ROOT), logger.error(f'The {CYB3RHQ_ROOT} is not present in {HostInformation.get_os_name_and_version_from_inventory(manager)}')


def test_manager_api_port(cyb3rhq_params):
    assert Cyb3rhqManager.is_cyb3rhq_api_port_open(cyb3rhq_params['master']), logger.error(f"The Cyb3rhq manager's API port in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['master'])} is closed")


def test_manager_agent_port(cyb3rhq_params):
    assert Cyb3rhqManager.is_cyb3rhq_agent_port_open(cyb3rhq_params['master']), logger.error(f"The Cyb3rhq manager port in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['master'])} is closed")


def test_manager_agent_enrollment_port(cyb3rhq_params):
    assert Cyb3rhqManager.is_cyb3rhq_agent_enrollment_port_open(cyb3rhq_params['master']), logger.error(f"The Cyb3rhq manager agent enrollment port in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['master'])} is closed")


def test_dashboard_status(cyb3rhq_params):
    assert 'active' in GeneralComponentActions.get_component_status(cyb3rhq_params['dashboard'], 'cyb3rhq-dashboard'), logger.error(f"The dashboard in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['dashboard'])} is not active")
    cyb3rhq_api = Cyb3rhqAPI(cyb3rhq_params['dashboard'], component='dashboard')
    assert Cyb3rhqDashboard.is_dashboard_active(cyb3rhq_params['dashboard']), logger.error(f"The Cyb3rhq dashboard is not active in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['dashboard'])}")


def test_dashboard_version(cyb3rhq_params):
    assert cyb3rhq_params['cyb3rhq_version'] == Cyb3rhqDashboard.get_dashboard_version(cyb3rhq_params['dashboard']), logger.error(f"There is dismatch in the Cyb3rhq dashboard version in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['dashboard'])}")


def test_dashboard_nodes(cyb3rhq_params):
    cyb3rhq_api = Cyb3rhqAPI(cyb3rhq_params['dashboard'], component='dashboard')
    assert Cyb3rhqDashboard.are_dashboard_nodes_working(cyb3rhq_api), logger.error(f"There is a problem in the Cyb3rhq dashboard node in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['dashboard'])}")


def test_dashboard_keystore(cyb3rhq_params):
    assert Cyb3rhqDashboard.is_dashboard_keystore_working(cyb3rhq_params['dashboard']), logger.error(f"There is a problem in the Cyb3rhq dashboard keystore in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['dashboard'])}")


def test_dashboard_port(cyb3rhq_params):
    assert Cyb3rhqDashboard.is_dashboard_port_open(cyb3rhq_params['dashboard']), logger.error(f"The Cyb3rhq dashboard port in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['dashboard'])} is closed")


def test_indexer_status(cyb3rhq_params):
    for indexer_params in cyb3rhq_params['indexers']:
        assert 'active' in GeneralComponentActions.get_component_status(indexer_params, 'cyb3rhq-indexer'), logger.error(f'The Cyb3rhq indexer in {HostInformation.get_os_name_and_version_from_inventory(indexer_params)} is not active')


def test_indexer_clusters_status(cyb3rhq_params):
    for indexer_params in cyb3rhq_params['indexers']:
        cyb3rhq_api = Cyb3rhqAPI(indexer_params, component='indexer')
        assert Cyb3rhqIndexer.is_index_cluster_working(cyb3rhq_api, indexer_params), logger.error(f'There is a problem in a Cyb3rhq indexer cluster in {HostInformation.get_os_name_and_version_from_inventory(indexer_params)}')


def test_indexer_indexes(cyb3rhq_params):
    for indexer_params in cyb3rhq_params['indexers']:
        cyb3rhq_api = Cyb3rhqAPI(indexer_params, component='indexer')
        assert Cyb3rhqIndexer.are_indexes_working(cyb3rhq_api, indexer_params), logger.error(f'There is a problem in a Cyb3rhq indexer index in {HostInformation.get_os_name_and_version_from_inventory(indexer_params)}')


def test_indexer_internalUsers(cyb3rhq_params):
    for indexer_params in cyb3rhq_params['indexers']:
        assert Cyb3rhqIndexer.are_indexer_internal_users_complete(indexer_params), logger.error(f'There is a problem in a Cyb3rhq indexer internal user in {HostInformation.get_os_name_and_version_from_inventory(indexer_params)}')


def test_indexer_version(cyb3rhq_params):
    for indexer_params in cyb3rhq_params['indexers']:
        assert cyb3rhq_params['cyb3rhq_version'] == Cyb3rhqIndexer.get_indexer_version(indexer_params), logger.error(f'There is dismatch in Cyb3rhq indexer version in {HostInformation.get_os_name_and_version_from_inventory(indexer_params)}')


def test_indexer_port(cyb3rhq_params):
    for indexer_params in cyb3rhq_params['indexers']:
        assert Cyb3rhqIndexer.is_indexer_port_open(indexer_params), logger.error(f"Some Cyb3rhq indexer port in {HostInformation.get_os_name_and_version_from_inventory(indexer_params)} is closed")


def test_filebeat_status(cyb3rhq_params):
    assert 'active' in GeneralComponentActions.get_component_status(cyb3rhq_params['master'], 'filebeat'), logger.error(f"The Filebeat in {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['master'])} is not active")


def test_indexer_conexion(cyb3rhq_params):
    for indexer_params in cyb3rhq_params['indexers']:
        assert Cyb3rhqManager.get_indexer_status(indexer_params), logger.error(f'IndexerConnector initialization failed {HostInformation.get_os_name_and_version_from_inventory(indexer_params)}')
