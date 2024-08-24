# Copyright (C) 2015, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2
from pathlib import Path


# --- Paths ---
CYB3RHQ_ROOT = Path("/var", "ossec")
# Configuration paths
CONFIGURATIONS_DIR = Path(CYB3RHQ_ROOT, "etc")
CYB3RHQ_CONF = Path(CONFIGURATIONS_DIR, "ossec.conf")
CLIENT_KEYS = Path(CONFIGURATIONS_DIR, "client.keys")

WINDOWS_ROOT_DIR = Path("C:", "Program Files (x86)", "ossec-agent")
WINDOWS_CONFIGURATIONS_DIR = Path(WINDOWS_ROOT_DIR, "etc")
CYB3RHQ_WINDOWS_CONF  = Path(WINDOWS_ROOT_DIR, "ossec.conf")
WINDOWS_CLIENT_KEYS = Path(WINDOWS_ROOT_DIR, "client.keys")
WINDOWS_VERSION = Path(WINDOWS_ROOT_DIR, "VERSION")
WINDOWS_REVISION = Path(WINDOWS_ROOT_DIR, "REVISION")

MACOS_ROOT_DIR = Path("/Library", "Ossec")
MACOS_CONFIGURATIONS_DIR = Path(MACOS_ROOT_DIR, "etc")
CYB3RHQ_MACOS_CONF  = Path(MACOS_CONFIGURATIONS_DIR, "ossec.conf")
MACOS_CLIENT_KEYS = Path(MACOS_CONFIGURATIONS_DIR, "client.keys")
MACOS_VERSION = Path(MACOS_ROOT_DIR, "VERSION")
MACOS_REVISION = Path(MACOS_ROOT_DIR, "REVISION")


# Binaries paths
BINARIES_DIR = Path(CYB3RHQ_ROOT, "bin")
CYB3RHQ_CONTROL = Path(BINARIES_DIR, "cyb3rhq-control")
AGENT_CONTROL = Path(BINARIES_DIR, "agent_control")
CLUSTER_CONTROL = Path(BINARIES_DIR, "cluster_control")

MACOS_BINARIES_DIR = Path(MACOS_ROOT_DIR, "bin")
MACOS_CYB3RHQ_CONTROL = Path(MACOS_BINARIES_DIR, "cyb3rhq-control")

# Logs paths
LOGS_DIR = Path(CYB3RHQ_ROOT, "logs")
CYB3RHQ_LOG = Path(LOGS_DIR, "ossec.log")
ALERTS_DIR = Path(LOGS_DIR, "alerts")
ALERTS_JSON = Path(ALERTS_DIR, "alerts.json")

MACOS_LOGS_DIR = Path(MACOS_ROOT_DIR, "logs")
CYB3RHQ_MACOS_LOG = Path(MACOS_LOGS_DIR, "ossec.log")
MACOS_ALERTS_DIR = Path(MACOS_LOGS_DIR, "alerts")
MACOS_ALERTS_JSON = Path(MACOS_ALERTS_DIR, "alerts.json")

# Daemons running paths
DAEMONS_DIR = Path(CYB3RHQ_ROOT, "var", "run")
AGENTD_STATE = Path(DAEMONS_DIR, "cyb3rhq-agentd.state")

# --- Users & Groups ---
CYB3RHQ_USER = "cyb3rhq"
CYB3RHQ_GROUP = "cyb3rhq"

# --- Daemons ---
AGENTD = 'cyb3rhq-agentd'
AGENTLESSD = 'cyb3rhq-agentlessd'
ANALYSISDD = 'cyb3rhq-analysisd'
APID = 'cyb3rhq-apid'
CLUSTERD = 'cyb3rhq-clusterd'
CSYSLOGD = 'cyb3rhq-csyslogd'
EXECD = 'cyb3rhq-execd'
INTEGRATORD = 'cyb3rhq-integratord'
MAILD = 'cyb3rhq-maild'
MODULESD = 'cyb3rhq-modulesd'
MONITORD = 'cyb3rhq-monitord'
LOGCOLLECTORD = 'cyb3rhq-logcollector'
REMOTED = 'cyb3rhq-remoted'
SYSCHECKD = 'cyb3rhq-syscheckd'
CYB3RHQ_DBD = 'cyb3rhq-db'
# Daemons lists
AGENT_DAEMONS = [AGENTD,
                 EXECD,
                 MODULESD,
                 LOGCOLLECTORD,
                 SYSCHECKD]
MANAGER_DAEMONS = [AGENTLESSD,
                   ANALYSISDD,
                   APID,
                   CLUSTERD,
                   CSYSLOGD,
                   EXECD,
                   INTEGRATORD,
                   LOGCOLLECTORD,
                   MAILD,
                   MODULESD,
                   MONITORD,
                   REMOTED,
                   SYSCHECKD,
                   CYB3RHQ_DBD]

# --- Log messages ---
CONNECTION_SERVER = "New cyb3rhq agent connected"
CONNECTION_AGENT = "Connected to the server"
KEY_REQ_AGENT = "Requesting a key from server"
KEY_REQ_SERVER = "Received request for a new agent"
RELEASING_RESOURCES = "Shutdown received. Releasing resources"
DELETING_RESPONSES = "Shutdown received. Deleting responses"
STARTED = 'INFO: Started'
