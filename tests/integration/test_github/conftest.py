# Copyright (C) 2015-2021, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

import pytest

from cyb3rhq_testing.github import detect_github_start


@pytest.fixture(scope='module')
def wait_for_github_start(get_configuration, request):
    # Wait for module github starts
    file_monitor = getattr(request.module, 'cyb3rhq_log_monitor')
    detect_github_start(file_monitor)
