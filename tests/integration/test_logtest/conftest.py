# Copyright (C) 2015-2021, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

import pytest

from cyb3rhq_testing.logcollector import LOG_COLLECTOR_GLOBAL_TIMEOUT
from cyb3rhq_testing.logtest import callback_logtest_started
from cyb3rhq_testing.tools.services import control_service
from cyb3rhq_testing.tools.monitoring import FileMonitor
from cyb3rhq_testing.tools.file import truncate_file
from cyb3rhq_testing.tools import LOG_FILE_PATH


@pytest.fixture(scope='module')
def restart_required_logtest_daemons():
    """Cyb3rhq logtests daemons handler."""
    required_logtest_daemons = ['cyb3rhq-analysisd', 'cyb3rhq-db']

    for daemon in required_logtest_daemons:
        control_service('stop', daemon=daemon)

    truncate_file(LOG_FILE_PATH)

    for daemon in required_logtest_daemons:
        control_service('start', daemon=daemon)

    yield

    for daemon in required_logtest_daemons:
        control_service('stop', daemon=daemon)


@pytest.fixture(scope='module')
def wait_for_logtest_startup(request):
    """Wait until logtest has begun."""
    log_monitor = FileMonitor(LOG_FILE_PATH)
    log_monitor.start(timeout=LOG_COLLECTOR_GLOBAL_TIMEOUT, callback=callback_logtest_started)
