# Copyright (C) 2015, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

from .executor import ConnectionManager
from .generic import HostInformation, CheckFiles
from modules.testing.utils import logger


class Cyb3rhqCentralComponents:

    @staticmethod
    def install_aio(inventory_path, cyb3rhq_version, live) -> None:
        """
        Installs Cyb3rhq central components (AIO) in the host

        Args:
            inventory_path (str): host's inventory path
            cyb3rhq_version (str): major.minor.patch

        """
        os_name = HostInformation.get_os_name_from_inventory(inventory_path)

        if live == "False":
            s3_url = 'packages-dev.cyb3rhq.com'
        else:
            s3_url = 'packages.cyb3rhq.com'

        release = '.'.join(cyb3rhq_version.split('.')[:2])


        logger.info(f'Installing the Cyb3rhq manager with https://{s3_url}/{release}/cyb3rhq-install.sh')

        if HostInformation.has_curl(inventory_path):
            commands = [
                f"curl -sO https://{s3_url}/{release}/cyb3rhq-install.sh && sudo bash ./cyb3rhq-install.sh -a --ignore-check"
            ]
        else:
            commands = [
                f"wget https://{s3_url}/{release}/cyb3rhq-install.sh && sudo bash ./cyb3rhq-install.sh -a --ignore-check"
            ]


        logger.info(f'Installing Cyb3rhq central components (AIO) in {HostInformation.get_os_name_and_version_from_inventory(inventory_path)}')
        ConnectionManager.execute_commands(inventory_path, commands)

    @staticmethod
    def uninstall_aio(inventory_path) -> None:
        """
        Uninstall Cyb3rhq Central Components (AIO) in the host

        Args:
            inventory_paths (str): hosts' inventory path
        """

        commands = ['bash cyb3rhq-install.sh --uninstall --ignore-check']

        logger.info(f'Uninstalling Cyb3rhq central components (AIO) in {HostInformation.get_os_name_and_version_from_inventory(inventory_path)}')
        ConnectionManager.execute_commands(inventory_path, commands)


    @staticmethod
    def _install_aio_callback(cyb3rhq_params, host_params):
        Cyb3rhqCentralComponents.install_aio(host_params, cyb3rhq_params['cyb3rhq_version'], cyb3rhq_params['live'])


    @staticmethod
    def _uninstall_aio_callback(host_params):
        Cyb3rhqCentralComponents.uninstall_aio(host_params)


    @staticmethod
    def perform_action_and_scan(host_params, action_callback) -> dict:
        """
        Takes scans using filters, the callback action and compares the result

        Args:
            host_params (str): host parameters
            callback (cb): callback (action)

        Returns:
            result (dict): comparison brief

        """
        result = CheckFiles.perform_action_and_scan(host_params, action_callback)
        os_name = HostInformation.get_os_name_from_inventory(host_params)
        logger.info(f'Applying filters in checkfiles in {HostInformation.get_os_name_and_version_from_inventory(host_params)}')

        if 'debian' in os_name:
            filter_data = {
                '/boot': {'added': [], 'removed': [], 'modified': ['grubenv']},
                '/usr/bin': {
                    'added': [
                        'unattended-upgrade', 'gapplication', 'add-apt-repository', 'gpg-wks-server', 'pkexec', 'gpgsplit',
                        'watchgnupg', 'pinentry-curses', 'gpg-zip', 'gsettings', 'gpg-agent', 'gresource', 'gdbus',
                        'gpg-connect-agent', 'gpgconf', 'gpgparsemail', 'lspgpot', 'pkaction', 'pkttyagent', 'pkmon',
                        'dirmngr', 'kbxutil', 'migrate-pubring-from-classic-gpg', 'gpgcompose', 'pkcheck', 'gpgsm', 'gio',
                        'pkcon', 'gpgtar', 'dirmngr-client', 'gpg', 'filebeat', 'gawk', 'curl', 'update-mime-database',
                        'dh_installxmlcatalogs', 'appstreamcli', 'lspgpot', 'symcryptrun'
                    ],
                    'removed': ['filebeat'],
                    'modified': []
                },
                '/root': {'added': ['trustdb.gpg', 'lesshst', 'ssh'], 'removed': ['filebeat'], 'modified': []},
                '/usr/sbin': {
                    'added': [
                        'update-catalog', 'applygnupgdefaults', 'addgnupghome', 'install-sgmlcatalog', 'update-xmlcatalog'
                    ],
                    'removed': [],
                    'modified': []
                }
            }
        else:
            filter_data = {
                '/boot': {
                    'added': ['grub2', 'loader', 'vmlinuz', 'System.map', 'config-', 'initramfs'],
                    'removed': [],
                    'modified': ['grubenv']
                },
                '/usr/bin': {'added': ['filebeat'], 'removed': ['filebeat'], 'modified': []},
                '/root': {'added': ['trustdb.gpg', 'lesshst'], 'removed': [], 'modified': ['.rnd']},
                '/usr/sbin': {'added': [], 'removed': [], 'modified': []}
            }

        # Use of filters
        for directory, changes in result.items():
            if directory in filter_data:
                for change, files in changes.items():
                    if change in filter_data[directory]:
                        result[directory][change] = [file for file in files if file.split('/')[-1] not in filter_data[directory][change]]

        return result

    @staticmethod
    def perform_install_and_scan_for_aio(host_params, cyb3rhq_params) -> None:
        """
        Coordinates the action of install the Cyb3rhq central components (AIO) and compares the checkfiles

        Args:
            host_params (str): host parameters
            cyb3rhq_params (str): cyb3rhq parameters

        """
        action_callback = lambda: Cyb3rhqCentralComponents._install_aio_callback(cyb3rhq_params, host_params)
        result = Cyb3rhqCentralComponents.perform_action_and_scan(host_params, action_callback)
        logger.info(f'Pre and post install checkfile comparison in {HostInformation.get_os_name_and_version_from_inventory(host_params)}: {result}')
        Cyb3rhqCentralComponents.assert_results(result)


    @staticmethod
    def perform_uninstall_and_scan_for_aio(host_params) -> None:
        """
        Coordinates the action of uninstall the Cyb3rhq central components (AIO) and compares the checkfiles

        Args:
            host_params (str): host parameters
            cyb3rhq_params (str): cyb3rhq parameters

        """
        action_callback = lambda: Cyb3rhqCentralComponents._uninstall_aio_callback(host_params)
        result = Cyb3rhqCentralComponents.perform_action_and_scan(host_params, action_callback)
        logger.info(f'Pre and post uninstall checkfile comparison in {HostInformation.get_os_name_and_version_from_inventory(host_params)}: {result}')
        Cyb3rhqCentralComponents.assert_results(result)


    @staticmethod
    def assert_results(result) -> None:
        """
        Gets the status of an agent given its name.

        Args:
            result (dict): result of comparison between pre and post action scan

        """
        categories = ['/root', '/usr/bin', '/usr/sbin', '/boot']
        actions = ['added', 'modified', 'removed']
        # Testing the results
        for category in categories:
            for action in actions:
                assert result[category][action] == [], logger.error(f'{result[category][action]} was found in: {category} {action}')
