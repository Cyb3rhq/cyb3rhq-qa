# cyb3rhq-qa

Cyb3rhq - Manager Agents provisioning

## Enviroment description
This enviroment sets a Manager with three (3) agents. Each agent has a especific version. It is designed to allow testing on different versions of the cyb3rhq agent working in conjunction with a specific version of the cyb3rhq manager.

## Setting up the provisioning

To run this provisioning we need to use a **Linux** machine and install the following tools:

- [Docker](https://docs.docker.com/install/)
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

## Structure

```bash
manager_agent
├── ansible.cfg
├── destroy.yml
├── inventory.yml
├── playbook.yml
├── README.md
├── roles
│   ├── agent-role
│   │   ├── files
│   │   │   └── ossec.conf
│   │   └── tasks
│   │       └── main.yml
│   ├── manager-role
│   │   ├── files
│   │   │   └── ossec.conf
│   │   └── tasks
│   │       └── main.yml
└── vars
    ├── configurations.yml
    └── main.yml
```

#### ansible.cfg

Ansible configuration file in the current directory. In this file, we setup the configuration of Ansible for this
provisioning.

#### destroy.yml

In this file we will specify that we want to shut down the docker machines in our environment.

##### inventory.yml

File containing the inventory of machines in our environment. In this file we will set the connection method and its
python interpreter

##### playbook.yml

Here we will write the commands to be executed in order to use our environment

##### roles

Folder with all the general roles that could be used for start our environment. Within each role we can find the
following structure:

- **files**: Configuration files to be applied when the environment is setting up.
- **tasks**: Main tasks to be performed for each role

#### Vars

This folder contains the variables used to configure our environment. Variables like the cluster key or the agent key.
- **agent#-package**: link to the cyb3rhq agent package  to be installed on each agent host. (currently versions 4.1.5, 4.2.2 and 4.2.5)

## Environment

The base environment defined for Docker provisioning is

- A master node
- Three agents.

| Agent        | Reports to    |
|--------------|---------------|
| cyb3rhq-agent1 | cyb3rhq-manager |
| cyb3rhq-agent2 | cyb3rhq-manager |
| cyb3rhq-agent3 | cyb3rhq-manager |

## Environment management

For running the docker provisioning we must execute the following command:

```shell script
ansible-playbook -i inventory.yml playbook.yml --extra-vars='{"package_repository":"packages", "repository": "4.x", "package_version": "4.4.0", "package_revision": "1"}'
```

To destroy it, the command is:

```shell script
ansible-playbook -i inventory.yml destroy.yml
```

## Example

```shell script
ansible-playbook -i inventory.yml playbook.yml

PLAY [Create our container (Manager)] *********************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************
ok: [localhost]

TASK [Create a network] *************************************************************************************************************************
ok: [localhost]

TASK [docker_container] *************************************************************************************************************************
changed: [localhost]

PLAY [Create our container (Agent1)] **********************************************************************************************************************

TASK [Gathering Facts] **************************************************************************************************************************
ok: [localhost]

TASK [docker_container] **************************************************************************************************************************
changed: [localhost]

PLAY [Create our container (Agent2)] **********************************************************************************************************************

TASK [Gathering Facts] **************************************************************************************************************************
ok: [localhost]

TASK [docker_container] **************************************************************************************************************************
changed: [localhost]

PLAY [Create our container (Agent3)] **********************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************
ok: [localhost]

TASK [docker_container] ****************************************************************************************************************************
changed: [localhost]

PLAY [Cyb3rhq Manager] ************************************************************************************************************************

TASK [Gathering Facts] ************************************************************************************************************************
ok: [cyb3rhq-manager]

TASK [roles/manager-role : Check and update debian repositories] ******************************************************************************************
changed: [cyb3rhq-manager]

TASK [roles/manager-role : Installing dependencies using apt] *********************************************************************************************
changed: [cyb3rhq-manager]

TASK [roles/manager-role : Clone cyb3rhq repository] ********************************************************************************************************
changed: [cyb3rhq-manager]

TASK [roles/manager-role : Install manager] ***************************************************************************************************************
changed: [cyb3rhq-manager]

TASK [roles/manager-role : Copy ossec.conf file] **********************************************************************************************************
changed: [cyb3rhq-manager]

TASK [roles/manager-role : Set cluster key] ***************************************************************************************************************
changed: [cyb3rhq-manager]

TASK [roles/manager-role : Set Cyb3rhq Manager IP] **********************************************************************************************************
changed: [cyb3rhq-manager]

TASK [roles/manager-role : Stop Cyb3rhq] ********************************************************************************************************************
changed: [cyb3rhq-manager]

TASK [roles/manager-role : Remove client.keys] ************************************************************************************************************
changed: [cyb3rhq-manager]

TASK [roles/manager-role : enable execd debug mode] *******************************************************************************************************
changed: [cyb3rhq-manager]

TASK [roles/manager-role : Register agents] ***************************************************************************************************************
changed: [cyb3rhq-manager]

TASK [roles/manager-role : Start Cyb3rhq] *******************************************************************************************************************
changed: [cyb3rhq-manager]

PLAY [Cyb3rhq Agent1] **********************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************
ok: [cyb3rhq-agent1]

TASK [roles/agent-role : Check and update debian repositories] ********************************************************************************************
changed: [cyb3rhq-agent1]

TASK [roles/agent-role : Installing dependencies using apt] ***********************************************************************************************
changed: [cyb3rhq-agent1]

TASK [roles/agent-role : Create log source] ***************************************************************************************************************
changed: [cyb3rhq-agent1]

TASK [roles/agent-role : Download package] ****************************************************************************************************************
changed: [cyb3rhq-agent1]

TASK [roles/agent-role : Install agent] *******************************************************************************************************************
changed: [cyb3rhq-agent1]

TASK [roles/agent-role : Copy ossec.conf file] ************************************************************************************************************
changed: [cyb3rhq-agent1]

TASK [roles/agent-role : enable execd debug mode] *********************************************************************************************************
changed: [cyb3rhq-agent1]

TASK [roles/agent-role : Remove client.keys] **************************************************************************************************************
changed: [cyb3rhq-agent1]

TASK [roles/agent-role : Register agents] *****************************************************************************************************************
changed: [cyb3rhq-agent1]

TASK [roles/agent-role : Set Cyb3rhq Manager IP] ************************************************************************************************************
changed: [cyb3rhq-agent1]

TASK [roles/agent-role : Restart Cyb3rhq] *******************************************************************************************************************
changed: [cyb3rhq-agent1]

PLAY [Cyb3rhq Agent2] ***************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************
ok: [cyb3rhq-agent2]

TASK [roles/agent-role : Check and update debian repositories] ******************************************************************************************** 
changed: [cyb3rhq-agent2]

TASK [roles/agent-role : Installing dependencies using apt] ***********************************************************************************************
changed: [cyb3rhq-agent2]

TASK [roles/agent-role : Create log source] ***************************************************************************************************************
changed: [cyb3rhq-agent2]

TASK [roles/agent-role : Download package] ****************************************************************************************************************
changed: [cyb3rhq-agent2]

TASK [roles/agent-role : Install agent] *******************************************************************************************************************
changed: [cyb3rhq-agent2]

TASK [roles/agent-role : Copy ossec.conf file] ************************************************************************************************************
changed: [cyb3rhq-agent2]

TASK [roles/agent-role : enable execd debug mode] *********************************************************************************************************
changed: [cyb3rhq-agent2]

TASK [roles/agent-role : Remove client.keys] **************************************************************************************************************
changed: [cyb3rhq-agent2]

TASK [roles/agent-role : Register agents] *****************************************************************************************************************
changed: [cyb3rhq-agent2]

TASK [roles/agent-role : Set Cyb3rhq Manager IP] ************************************************************************************************************
changed: [cyb3rhq-agent2]

TASK [roles/agent-role : Restart Cyb3rhq] *******************************************************************************************************************
changed: [cyb3rhq-agent2]

PLAY [Cyb3rhq Agent3] **********************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************
ok: [cyb3rhq-agent3]

TASK [roles/agent-role : Check and update debian repositories] *******************************************************************************************
changed: [cyb3rhq-agent3]

TASK [roles/agent-role : Installing dependencies using apt] ***********************************************************************************************
changed: [cyb3rhq-agent3]

TASK [roles/agent-role : Create log source] ***************************************************************************************************************
changed: [cyb3rhq-agent3]

TASK [roles/agent-role : Download package] ****************************************************************************************************************
changed: [cyb3rhq-agent3]

TASK [roles/agent-role : Install agent] *******************************************************************************************************************
changed: [cyb3rhq-agent3]

TASK [roles/agent-role : Copy ossec.conf file] ************************************************************************************************************
changed: [cyb3rhq-agent3]

TASK [roles/agent-role : enable execd debug mode] *********************************************************************************************************
changed: [cyb3rhq-agent3]

TASK [roles/agent-role : Remove client.keys] **************************************************************************************************************
changed: [cyb3rhq-agent3]

TASK [roles/agent-role : Register agents] *****************************************************************************************************************
changed: [cyb3rhq-agent3]

TASK [roles/agent-role : Set Cyb3rhq Manager IP] ************************************************************************************************************
changed: [cyb3rhq-agent3]

TASK [roles/agent-role : Restart Cyb3rhq] *******************************************************************************************************************
changed: [cyb3rhq-agent3]

PLAY RECAP ************************************************************************************************************************************************
localhost                  : ok=9    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
cyb3rhq-agent1               : ok=12   changed=11   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
cyb3rhq-agent2               : ok=12   changed=11   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
cyb3rhq-agent3               : ok=12   changed=11   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
cyb3rhq-manager              : ok=13   changed=12   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
=============================================================================== 
Playbook run took 0 days, 0 hours, 15 minutes, 47 seconds 

```

```shell script
ansible-playbook -i inventory.yml destroy.yml

PLAY [localhost] **********************************************************************************************************************************************************

TASK [Gathering Facts] ****************************************************************************************************************************************************
ok: [localhost]

TASK [docker_container] ***************************************************************************************************************************************************
changed: [localhost]

TASK [docker_container] ***************************************************************************************************************************************************
changed: [localhost]

TASK [docker_container] ***************************************************************************************************************************************************
changed: [localhost]

TASK [docker_container] ***************************************************************************************************************************************************
changed: [localhost]
PLAY RECAP ****************************************************************************************************************************************************************
localhost                  : ok=5    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```
