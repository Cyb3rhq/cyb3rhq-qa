import os
from pathlib import Path

from cyb3rhq_testing.qa_ctl.provisioning.cyb3rhq_deployment.cyb3rhq_package import Cyb3rhqPackage
from cyb3rhq_testing.qa_ctl.provisioning.ansible.ansible_task import AnsibleTask
from cyb3rhq_testing.qa_ctl import QACTL_LOGGER
from cyb3rhq_testing.tools.logging import Logging
from cyb3rhq_testing.tools.exceptions import QAValueError
from cyb3rhq_testing.tools.s3_package import get_s3_package_url
from cyb3rhq_testing.tools.file import join_path


class Cyb3rhqS3Package(Cyb3rhqPackage):
    """Install Cyb3rhq from a S3 URL package

    Args:
        cyb3rhq_target (string): Type of the Cyb3rhq instance desired (agent or manager).
        s3_package_url (string): URL of the S3 Cyb3rhq package.
        installation_files_path (string): Path where is located the Cyb3rhq instalation files.
        qa_ctl_configuration (QACTLConfiguration): QACTL configuration.
        version (string): The version of Cyb3rhq. Parameter set by default to 'None'.
        system (string): System of the Cyb3rhq installation files. Parameter set by default to 'None'.
        revision (string): Revision of the cyb3rhq package. Parameter set by default to 'None'.
        repository (string): Repository of the cyb3rhq package. Parameter set by default to 'None'.
        architecture (string): Architecture of the Cyb3rhq package. Parameter set by default to 'None'.

    Attributes:
        cyb3rhq_target (string): Type of the Cyb3rhq instance desired (agent or manager).
        s3_package_url (string): URL of the S3 Cyb3rhq package.
        package_name (string): Name of the S3 package.
        installation_files_path (string): Path where is located the Cyb3rhq instalation files.
        qa_ctl_configuration (QACTLConfiguration): QACTL configuration.
        version (string): The version of Cyb3rhq. Parameter set by default to 'None'.
        system (string): System of the Cyb3rhq installation files. Parameter set by default to 'None'.
        revision (string): Revision of the cyb3rhq package. Parameter set by default to 'None'.
        repository (string): Repository of the cyb3rhq package. Parameter set by default to 'None'.
        architecture (string): Architecture of the Cyb3rhq package. Parameter set by default to 'None'.
    """

    LOGGER = Logging.get_logger(QACTL_LOGGER)

    def __init__(self, cyb3rhq_target, installation_files_path, qa_ctl_configuration,
                 s3_package_url=None, system=None, version=None, revision=None, repository=None):
        self.system = system
        self.revision = revision
        self.repository = repository
        self.s3_package_url = s3_package_url if s3_package_url is not None else self.__get_package_url()
        super().__init__(cyb3rhq_target=cyb3rhq_target, installation_files_path=installation_files_path,
                         system=system, version=version, qa_ctl_configuration=qa_ctl_configuration)

    def __get_package_url(self):
        """ Get S3 package URL from repository, version, revision and system parameters.

        Returns:
            str: S3 package URL.
        """
        if self.version is not None and self.repository is not None and self.system is not None and \
                self.revision is not None:
            architecture = Cyb3rhqS3Package.get_architecture(self.system)
            return get_s3_package_url(self.repository, self.cyb3rhq_target, self.version,
                                      self.revision, self.system, architecture)
        else:
            raise QAValueError('Could not get Cyb3rhq Package S3 URL. s3_package_url or '
                               '(version, repository, system, revision) has None value', Cyb3rhqS3Package.LOGGER.error,
                               QACTL_LOGGER)

    @staticmethod
    def get_architecture(system):
        """Get the needed architecture for the cyb3rhq package

        Args:
            system (string): String with the system value given

        Returns:
            str: String with the default architecture for the system
        """
        default_architectures = {
            'deb': 'amd64',
            'rpm': 'x86_64',
            'rpm5': 'x86_64',
            'windows': 'i386',
            'macos': 'amd64',
            'solaris10': 'i386',
            'solaris11': 'i386',
            'wpk-linux': 'x86_64',
            'wpk-windows': 'i386',
        }
        return default_architectures[system]

    def download_installation_files(self, inventory_file_path, hosts='all'):
        """Download the installation files of Cyb3rhq in the given inventory file path

        Args:
            s3_package_url (string): URL of the S3 Cyb3rhq package.
            inventory_file_path (string): path where the instalation files are going to be stored.
            hosts (string): Parameter set to `all` by default.
            repository (string): Repository of the cyb3rhq package.
            cyb3rhq_target (string): Type of the Cyb3rhq instance desired (agent or manager).
            version (string): The version of Cyb3rhq.
            revision (string): Revision of the cyb3rhq package.
            system (string): System for the cyb3rhq package.

        Returns:
            str: String with the complete path of the downloaded installation package
        """
        package_name = Path(self.s3_package_url).name
        Cyb3rhqS3Package.LOGGER.debug(f"Downloading Cyb3rhq S3 package from {self.s3_package_url} in {hosts} hosts")

        download_unix_s3_package = AnsibleTask({
            'name': 'Download S3 package (Unix)',
            'get_url': {'url': self.s3_package_url, 'dest': self.installation_files_path},
            'register': 'download_state', 'retries': 6, 'delay': 10,
            'until': 'download_state is success',
            'when': 'ansible_system != "Win32NT"'
        })

        download_windows_s3_package = AnsibleTask({
            'name': 'Download S3 package (Windows)',
            'win_get_url': {'url': self.s3_package_url, 'dest': self.installation_files_path},
            'register': 'download_state', 'retries': 6, 'delay': 10,
            'until': 'download_state is success',
            'when': 'ansible_system == "Win32NT"'
        })

        Cyb3rhqS3Package.LOGGER.debug(f"Cyb3rhq S3 package was successfully downloaded in {hosts} hosts")

        super().download_installation_files(inventory_file_path, [download_unix_s3_package,
                                                                  download_windows_s3_package], hosts)

        package_system = 'windows' if '.msi' in package_name else 'generic'
        path_list = self.installation_files_path.split('\\') if package_system == 'windows' else \
            self.installation_files_path.split('/')
        path_list.append(package_name)

        return join_path(path_list, package_system)
