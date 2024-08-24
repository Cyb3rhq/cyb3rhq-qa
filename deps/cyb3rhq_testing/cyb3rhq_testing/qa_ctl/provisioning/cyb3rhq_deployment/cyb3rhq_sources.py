from cyb3rhq_testing.qa_ctl.provisioning.cyb3rhq_deployment.cyb3rhq_installation import Cyb3rhqInstallation
from cyb3rhq_testing.qa_ctl.provisioning.ansible.ansible_task import AnsibleTask
from cyb3rhq_testing.qa_ctl import QACTL_LOGGER
from cyb3rhq_testing.tools.logging import Logging


class Cyb3rhqSources(Cyb3rhqInstallation):
    """Install Cyb3rhq from the given sources. In this case, the installation
        will be done from the source files of a repository.

    Args:
        cyb3rhq_target (string): Type of the Cyb3rhq instance desired (agent or manager).
        installation_files_path (string): Path where is located the Cyb3rhq instalation files.
        qa_ctl_configuration (QACTLConfiguration): QACTL configuration.
        cyb3rhq_branch (string): String containing the branch from where the files are going to be downloaded.
        This field is set to 'master' by default.
        cyb3rhq_repository_url (string): URL from the repo where the cyb3rhq sources files are located.
        This parameter is set to 'https://github.com/cyb3rhq/cyb3rhq.git' by default.

    Attributes:
        cyb3rhq_target (string): Type of the Cyb3rhq instance desired (agent or manager).
        installation_files_path (string): Path where is located the Cyb3rhq instalation files.
        qa_ctl_configuration (QACTLConfiguration): QACTL configuration.
        cyb3rhq_branch (string): String containing the branch from where the files are going to be downloaded.
        This field is set to 'master' by default.
        cyb3rhq_repository_url (string): URL from the repo where the cyb3rhq sources files are located.
        This parameter is set to 'https://github.com/cyb3rhq/cyb3rhq.git' by default.
    """
    LOGGER = Logging.get_logger(QACTL_LOGGER)

    def __init__(self, cyb3rhq_target, installation_files_path, qa_ctl_configuration, cyb3rhq_branch='master',
                 cyb3rhq_repository_url='https://github.com/cyb3rhq/cyb3rhq.git'):
        self.cyb3rhq_branch = cyb3rhq_branch
        self.cyb3rhq_repository_url = cyb3rhq_repository_url
        super().__init__(cyb3rhq_target=cyb3rhq_target, qa_ctl_configuration=qa_ctl_configuration,
                         installation_files_path=f"{installation_files_path}/cyb3rhq-{self.cyb3rhq_branch}")

    def download_installation_files(self, inventory_file_path, hosts='all'):
        """Download the source files of Cyb3rhq using an AnsibleTask instance.

        Args:
            inventory_file_path (string): path where the instalation files are going to be stored
            hosts (string): Parameter set to `all` by default

        Returns:
            str: String with the path where the installation files are located
        """
        Cyb3rhqSources.LOGGER.debug(f"Downloading Cyb3rhq sources from {self.cyb3rhq_branch} branch in {hosts} hosts")

        download_cyb3rhq_sources_task = AnsibleTask({
            'name': f"Download Cyb3rhq branch in {self.installation_files_path}",
            'shell': f"cd {self.installation_files_path} && curl -Ls https://github.com/cyb3rhq/cyb3rhq/archive/"
                     f"{self.cyb3rhq_branch}.tar.gz | tar zx && mv cyb3rhq-*/* ."
        })
        Cyb3rhqSources.LOGGER.debug(f"Cyb3rhq sources from {self.cyb3rhq_branch} branch were successfully downloaded in "
                                  f"{hosts} hosts")
        super().download_installation_files(inventory_file_path, [download_cyb3rhq_sources_task], hosts)

        return self.installation_files_path
