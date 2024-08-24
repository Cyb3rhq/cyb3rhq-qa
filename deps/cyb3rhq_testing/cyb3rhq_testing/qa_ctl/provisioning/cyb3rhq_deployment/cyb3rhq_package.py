from abc import ABC, abstractmethod

from cyb3rhq_testing.qa_ctl.provisioning.cyb3rhq_deployment.cyb3rhq_installation import Cyb3rhqInstallation


class Cyb3rhqPackage(Cyb3rhqInstallation, ABC):
    """Install Cyb3rhq from the given sources. In this case, the installation
        will be done from a package file.

    Args:
        version (string): The version of Cyb3rhq.
        system (string): System of the Cyb3rhq installation files.
        cyb3rhq_target (string): Type of the Cyb3rhq instance desired (agent or manager).
        installation_files_path (string): Path where is located the Cyb3rhq instalation files.
        qa_ctl_configuration (QACTLConfiguration): QACTL configuration.

    Attributes:
        version (string): The version of Cyb3rhq.
        system (string): System of the Cyb3rhq installation files.
        cyb3rhq_target (string): Type of the Cyb3rhq instance desired (agent or manager).
        installation_files_path (string): Path where is located the Cyb3rhq instalation files.
        qa_ctl_configuration (QACTLConfiguration): QACTL configuration.
    """
    def __init__(self, version, system, cyb3rhq_target, installation_files_path, qa_ctl_configuration):
        self.version = version
        self.system = system
        super().__init__(cyb3rhq_target=cyb3rhq_target, installation_files_path=installation_files_path,
                         qa_ctl_configuration=qa_ctl_configuration)

    @abstractmethod
    def download_installation_files(self, inventory_file_path, ansible_tasks, hosts='all'):
        """Download the installation files of Cyb3rhq.

        Args:
            inventory_file_path (string): path where the instalation files are going to be stored
            ansible_tasks (ansible object): ansible instance with already provided tasks to run
            hosts (string): Parameter set to `all` by default
        """
        super().download_installation_files(inventory_file_path, ansible_tasks, hosts)
