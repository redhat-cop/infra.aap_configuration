# tower_configuration.project_update
## Description
An Ansible Role to update a list of projects in Ansible Tower.

## Requirements
ansible-galaxy collectioninstall  -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx

## Variables
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`tower_state`|"present"|no|The state all objects will take unless overriden by object default|'absent'|
|`tower_hostname`|""|yes|URL to the Ansible Tower Server.|127.0.0.1|
|`tower_validate_certs`|`True`|no|Whether or not to validate the Ansible Tower Server's SSL certificate.||
|`tower_username`|""|yes|Admin User on the Ansible Tower Server.||
|`tower_password`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`tower_oauthtoken`|""|yes|Tower Admin User's token on the Ansible Tower Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`tower_projects`|`see below`|yes|Data structure describing the project to update Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the project update task does not include sensitive information.
tower_configuration_project_update_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of tower configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_project_update_secure_logging`|`False`|no|Whether or not to include the sensitive ad_hoc_command role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|The name or id of the project to update.|
|`organization`|""|no|str|Organization the project exists in. Used for lookup only.|
|`wait`|""|no|str|Wait for the project to complete.|
|`interval`|""|no|str|The interval to request an update from Tower.|
|`timeout`|""|no|str|If waiting for the job to complete this will abort after this amount of seconds.|

### Standard Project Data Structure
#### Yaml Example
```yaml
---
tower_projects:
  - name: Test Project
    scm_type: git
    scm_url: https://github.com/ansible/tower-example.git
    scm_branch: master
    scm_clean: true
    description: Test Project 1
    organization: Satellite
    wait: true
  - name: Test Project 2
    scm_type: git
    scm_url: https://github.com/ansible/tower-example.git
    description: Test Project 2
    organization: Satellite
    wait: true
  - name: Test Inventory source project
    scm_type: git
    scm_url: https://github.com/ansible/ansible-examples.git
    description: ansible-examples
    organization: Satellite
    wait: true

```

## Playbook Examples
### Standard Role Usage
```yaml
---
- name: Playbook to configure ansible tower post installation
  hosts: localhost
  connection: local
  # Define following vars here, or in tower_configs/tower_auth.yml
  # tower_hostname: ansible-tower-web-svc-test-project.example.com
  # tower_username: admin
  # tower_password: changeme
  pre_tasks:
    - name: Include vars from tower_configs directory
      include_vars:
        dir: ./yaml
        ignore_files: [tower_config.yml.template]
        extensions: ["yml"]
  roles:
    - {role: redhat_cop.tower_configuration.project_update, when: tower_ad_hoc_commands is defined}

```
## License
[MIT](LICENSE)

## Author
[Sean Sullivan](https://github.com/Wilk42)
