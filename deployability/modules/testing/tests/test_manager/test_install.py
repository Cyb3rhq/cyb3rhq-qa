# Copyright (C) 2015, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import pytest

from modules.testing.utils import logger
from ..helpers.constants import CYB3RHQ_ROOT
from ..helpers.executor import Cyb3rhqAPI
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
    cyb3rhq_params['indexers'] = [value for key, value in targets_dict.items() if key.startswith('node-')]
    cyb3rhq_params['dashboard'] = targets_dict.get('dashboard', cyb3rhq_params['master'])

    # If there are no indexers, we choose cyb3rhq-1 by default
    if not cyb3rhq_params['indexers']:
        cyb3rhq_params['indexers'].append(cyb3rhq_params['master'])

    cyb3rhq_params['managers'] = {key: value for key, value in targets_dict.items() if key.startswith('cyb3rhq-')}

def test_installation(cyb3rhq_params):
    # Disabling firewall for all managers
    for manager_name, manager_params in cyb3rhq_params['managers'].items():
        Utils.check_inventory_connection(manager_params)
        HostConfiguration.disable_firewall(manager_params)

    # Certs create and scp from master to worker
    HostConfiguration.certs_create(cyb3rhq_params['cyb3rhq_version'], cyb3rhq_params['master'], cyb3rhq_params['dashboard'], cyb3rhq_params['indexers'], cyb3rhq_params['workers'], cyb3rhq_params['live'])

    for workers in cyb3rhq_params['workers']:
        HostConfiguration.scp_to(cyb3rhq_params['master'], workers, 'cyb3rhq-install-files.tar')

    # Install managers and perform checkfile testing
    for manager_name, manager_params in cyb3rhq_params['managers'].items():
        Cyb3rhqManager.install_manager(manager_params, manager_name, cyb3rhq_params['cyb3rhq_version'], cyb3rhq_params['live'])

    # Validation of activity and directory of the managers
    for manager in cyb3rhq_params['managers'].values():
        manager_status = GeneralComponentActions.get_component_status(manager, 'cyb3rhq-manager')
        assert 'active' in manager_status, logger.error(f'The {HostInformation.get_os_name_and_version_from_inventory(manager)} is not active')
        assert HostInformation.dir_exists(manager, CYB3RHQ_ROOT), logger.error(f'The {CYB3RHQ_ROOT} is not present in {HostInformation.get_os_name_and_version_from_inventory(manager)}')

    # Configuring cluster for all managers
    hex16_code = 'eecda366dded9b32bcfbf3b057bf3ede'
    for manager_name, manager_params in cyb3rhq_params['managers'].items():
        node_type = 'master' if manager_name == 'cyb3rhq-1' else 'worker'
        Cyb3rhqManager.configuring_clusters(manager_params, manager_name, node_type, cyb3rhq_params['master'], hex16_code, 'no')

    # Cluster info check
    cluster_info = Cyb3rhqManager.get_cluster_info(cyb3rhq_params['master'])
    for manager_name, manager_params in cyb3rhq_params['managers'].items():
        rest_of_managers = [k for k in cyb3rhq_params['managers'].keys() if k != manager_name]
        assert manager_name in cluster_info, logger.error(f'The cluster {manager_name} is not connected to {rest_of_managers}')


def test_manager_status(cyb3rhq_params):
    for manager in cyb3rhq_params['managers'].values():
        manager_status = GeneralComponentActions.get_component_status(manager, 'cyb3rhq-manager')
        assert 'active' in manager_status, logger.error(f'The {HostInformation.get_os_name_and_version_from_inventory(manager)} is not active')


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
