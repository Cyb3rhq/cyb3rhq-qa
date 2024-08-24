# Copyright (C) 2015, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import pytest

def pytest_addoption(parser):
    parser.addoption('--cyb3rhq_version', required=False, help='Cyb3rhq version to test files.')
    parser.addoption('--cyb3rhq_revision', required=False, help='Cyb3rhq revision to test.')
    parser.addoption('--system', required=False, help='OS version where cyb3rhq was installed.')
    parser.addoption('--component', required=False, help='Component to be tested.')
    parser.addoption('--dependencies', required=False, help='Dependency to be tested.')
    parser.addoption('--targets', required=False, help='Targets to be tested.')
    parser.addoption('--live', required=True, help='Packages repository.')

@pytest.fixture(scope='session')
def cyb3rhq_version(request):

    return request.config.getoption('cyb3rhq_version')


@pytest.fixture(scope='session')
def cyb3rhq_revision(request):

    return request.config.getoption('cyb3rhq_revision')


@pytest.fixture(scope='session')
def system(request):

    return request.config.getoption('system')


@pytest.fixture(scope='session')
def component(request):

    return request.config.getoption('component')


@pytest.fixture(scope='session')
def dependencies(request) -> dict | None:

    return request.config.getoption('dependencies')

@pytest.fixture(scope='session')
def targets(request) -> dict | None:

    return request.config.getoption('targets')


@pytest.fixture(scope='session')
def live(request) -> bool | None:
    live_value = request.config.getoption('live')

    return live_value.lower() == 'true' if live_value else None
