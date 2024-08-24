# Cyb3rhq

[![Slack](https://img.shields.io/badge/slack-join-blue.svg)](https://cyb3rhq.com/community/join-us-on-slack/)
[![Email](https://img.shields.io/badge/email-join-blue.svg)](https://groups.google.com/forum/#!forum/cyb3rhq)
[![Documentation](https://img.shields.io/badge/docs-view-green.svg)](https://documentation.cyb3rhq.com)
[![Documentation](https://img.shields.io/badge/web-view-green.svg)](https://cyb3rhq.com)
[![Twitter](https://img.shields.io/twitter/follow/cyb3rhq?style=social)](https://twitter.com/cyb3rhq)
[![YouTube](https://img.shields.io/youtube/views/peTSzcAueEc?style=social)](https://www.youtube.com/watch?v=peTSzcAueEc)


Cyb3rhq is a free and open source platform used for threat prevention, detection, and response. It is capable of protecting workloads across on-premises, virtualized, containerized, and cloud-based environments.

Cyb3rhq solution consists of an endpoint security agent, deployed to the monitored systems, and a management server, which collects and analyzes data gathered by the agents. Besides, Cyb3rhq has been fully integrated with the Elastic Stack, providing a search engine and data visualization tool that allows users to navigate through their security alerts.

## Cyb3rhq QA repository

In this repository you will find the tests used in the CI environment to test Cyb3rhq's capabilities and daemons. This is the structure of the repository:
- `deps/cyb3rhq_testing`: contains a Python's framework used to automatize tasks and interact with Cyb3rhq.
- `tests`: directory containing the test suite. These are tests developed using Pytest.
    - `integration`: integration tests of the different daemons/components.
    - `system`: system tests of Cyb3rhq.
    - `scans`: tests used to scan and verify Cyb3rhq Python code and dependencies.
- `docs`:  contains the technical documentation about the code and documentation about the tests.
