# Copyright (C) 2015-2021, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
import json
from setuptools import setup, find_packages
import os

package_data_list = [
    'data/agent.conf',
    'data/syscheck_event.json',
    'data/syscheck_event_windows.json',
    'data/mitre_event.json',
    'data/analysis_alert.json',
    'data/analysis_alert_windows.json',
    'data/state_integrity_analysis_schema.json',
    'data/gcp_event.json',
    'data/keepalives.txt',
    'data/rootcheck.txt',
    'data/syscollector.py',
    'data/winevt.py',
    'data/sslmanager.key',
    'data/sslmanager.cert',
    'tools/macos_log/log_generator.m',
    'qa_docs/schema.yaml',
    'qa_docs/VERSION.json',
    'qa_docs/dockerfiles/*',
    'qa_ctl/deployment/dockerfiles/*',
    'qa_ctl/deployment/dockerfiles/qa_ctl/*',
    'qa_ctl/deployment/vagrantfile_template.txt',
    'qa_ctl/provisioning/cyb3rhq_deployment/templates/preloaded_vars.conf.j2',
    'data/qactl_conf_validator_schema.json',
    'data/all_disabled_ossec.conf',
    'data/vulnerability_parsed_packages.json',
    'tools/migration_tool/delta_schema.json',
    'end_to_end/vulnerability_detector_packages/vuln_packages.json',
    'tools/migration_tool/CVE_JSON_5.0_bundled.json',
    'data/data_visualizer/*'
]

scripts_list = [
    'simulate-agents=cyb3rhq_testing.scripts.simulate_agents:main',
    'cyb3rhq-metrics=cyb3rhq_testing.scripts.cyb3rhq_metrics:main',
    'cyb3rhq-report=cyb3rhq_testing.scripts.cyb3rhq_report:main',
    'cyb3rhq-statistics=cyb3rhq_testing.scripts.cyb3rhq_statistics:main',
    'data-visualizer=cyb3rhq_testing.scripts.data_visualizations:main',
    'simulate-api-load=cyb3rhq_testing.scripts.simulate_api_load:main',
    'cyb3rhq-log-metrics=cyb3rhq_testing.scripts.cyb3rhq_log_metrics:main',
    'qa-docs=cyb3rhq_testing.scripts.qa_docs:main',
    'qa-ctl=cyb3rhq_testing.scripts.qa_ctl:main',
    'check-files=cyb3rhq_testing.scripts.check_files:main',
    'add-agents-client-keys=cyb3rhq_testing.scripts.add_agents_client_keys:main',
    'unsync-agents=cyb3rhq_testing.scripts.unsync_agents:main',
    'stress_results_comparator=cyb3rhq_testing.scripts.stress_results_comparator:main'
]


def get_files_from_directory(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


def get_version():
    script_path = os.path.dirname(__file__)
    rel_path = "../../version.json"
    abs_file_path = os.path.join(script_path, rel_path)
    f = open(abs_file_path)
    data = json.load(f)
    version = data['version']
    return version


package_data_list.extend(get_files_from_directory('cyb3rhq_testing/qa_docs/search_ui'))

setup(
    name='cyb3rhq_testing',
    version=get_version(),
    description='Cyb3rhq testing utilities to help programmers automate tests',
    url='https://github.com/cyb3rhq',
    author='Cyb3rhq',
    author_email='hello@cyb3rhq.com',
    license='GPLv2',
    packages=find_packages(),
    package_data={'cyb3rhq_testing': package_data_list},
    entry_points={'console_scripts': scripts_list},
    include_package_data=True,
    zip_safe=False
)
