#!/bin/bash

BRANCH="$1"
CONFIG_FILE_PATH="$2"
EXTRA_ARGS="${@:3}"

# Download the custom branch of cyb3rhq-qa repository
curl -Ls https://github.com/cyb3rhq/cyb3rhq-qa/archive/${BRANCH}.tar.gz | tar zx &> /dev/null && mv cyb3rhq-* cyb3rhq-qa

# Install python dependencies not installed from
python3 -m pip install -r cyb3rhq-qa/requirements.txt &> /dev/null

# Install Cyb3rhq QA framework
cd cyb3rhq-qa/deps/cyb3rhq_testing &> /dev/null
python3 setup.py install &> /dev/null

# Run qa-ctl tool
/usr/local/bin/qa-ctl -c /cyb3rhq_qa_ctl/${CONFIG_FILE_PATH} ${EXTRA_ARGS}
