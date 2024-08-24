'''
copyright: Copyright (C) 2015-2023, Cyb3rhq Inc.
           Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
           This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
'''
import pytest

# Services Variables
CYB3RHQ_SERVICES_STOPPED = 'stopped'
CYB3RHQ_SERVICE_PREFIX = 'cyb3rhq'
CYB3RHQ_SERVICES_STOP = 'stop'
CYB3RHQ_SERVICES_START = 'start'

# Configurations
DATA = 'data'
CYB3RHQ_LOG_MONITOR = 'cyb3rhq_log_monitor'

# Marks Executions

TIER0 = pytest.mark.tier(level=0)
TIER1 = pytest.mark.tier(level=1)
TIER2 = pytest.mark.tier(level=2)

WINDOWS = pytest.mark.win32
LINUX = pytest.mark.linux
MACOS = pytest.mark.darwin
SOLARIS = pytest.mark.sunos5

AGENT = pytest.mark.agent
SERVER = pytest.mark.server

# Local internal options
WINDOWS_DEBUG = 'windows.debug'
SYSCHECK_DEBUG = 'syscheck.debug'
VERBOSE_DEBUG_OUTPUT = 2
