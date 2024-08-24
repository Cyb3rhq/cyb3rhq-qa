# Copyright (C) 2015, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import pytest

from modules.testing.utils import logger
from ..helpers.generic import HostInformation, GeneralComponentActions


@pytest.fixture(scope="module", autouse=True)
def cyb3rhq_params(request):
    cyb3rhq_version = request.config.getoption('--cyb3rhq_version')
    cyb3rhq_revision = request.config.getoption('--cyb3rhq_revision')
    dependencies = request.config.getoption('--dependencies')
    targets = request.config.getoption('--targets')

    return {
        'cyb3rhq_version': cyb3rhq_version,
        'cyb3rhq_revision': cyb3rhq_revision,
        'dependencies': dependencies,
        'targets': targets
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

def test_restart(cyb3rhq_params):
    for worker in cyb3rhq_params['workers']:
        GeneralComponentActions.component_restart(worker, 'cyb3rhq-manager')

    assert 'active ' in GeneralComponentActions.get_component_status(cyb3rhq_params['master'], 'cyb3rhq-manager'), logger.error(f"The {HostInformation.get_os_name_and_version_from_inventory(cyb3rhq_params['master'])} is not active")

    for worker in cyb3rhq_params['workers']:
        assert 'active ' in GeneralComponentActions.get_component_status(worker, 'cyb3rhq-manager'), logger.error(f'The {HostInformation.get_os_name_and_version_from_inventory(worker)} is not active')
