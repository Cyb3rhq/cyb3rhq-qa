# Copyright (C) 2015-2021, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
import pytest

from cyb3rhq_testing.tools.services import control_service


@pytest.fixture(scope='package')
def restart_logcollector_required_daemons_package():
    control_service('restart', 'cyb3rhq-agentd')
    control_service('restart', 'cyb3rhq-logcollector')
    control_service('restart', 'cyb3rhq-modulesd')

    yield

    control_service('restart', 'cyb3rhq-agentd')
    control_service('restart', 'cyb3rhq-logcollector')
    control_service('restart', 'cyb3rhq-modulesd')
