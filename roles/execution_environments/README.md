# controller_configuration.execution_environments
## Description
An Ansible Role to create execution_environments on Ansible Controller.

## Requirements
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx
  or
  ansible.controller

## Variables

### Authentication
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`controller_state`|"present"|no|The state all objects will take unless overridden by object default|'absent'|
|`controller_hostname`|""|yes|URL to the Ansible Controller Server.|127.0.0.1|
|`controller_validate_certs`|`True`|no|Whether or not to validate the Ansible Controller Server's SSL certificate.||
|`controller_username`|""|yes|Admin User on the Ansible Controller Server.||
|`controller_password`|""|yes|Controller Admin User's password on the Ansible Controller Server. This should be stored in an Ansible Vault at vars/controller-secrets.yml or elsewhere and called from a parent playbook.||
|`controller_oauthtoken`|""|yes|Controller Admin User's token on the Ansible Controller Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`controller_execution_environments`|`see below`|yes|Data structure describing your organization or organizations Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add execution_environments task does not include sensitive information.
controller_configuration_execution_environments_secure_logging defaults to the value of controller_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_execution_environments_secure_logging`|`False`|no|Whether or not to include the sensitive execution_environments role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`controller_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables
The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`controller_configuration_execution_environments_async_retries`|30|no|This variable sets the number of retries to attempt for the role.|
|`controller_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`controller_configuration_execution_environments_async_delay`|1|no|This sets the delay between retries for the role.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Name of Job Template|
|`description`|""|no|str|Description to use for the execution environment.|
|`image`|""|yes|str|Container image to use for the execution environment|
|`organization`|""|no|str|The organization the execution environment belongs to.|
|`credential`|""|no|str|Name of the credential to use for the execution environment.|
|`pull`|"missing"|no|choice("always", "missing", "never")|Determine image pull behavior|
|`state`|`present`|no|str|Desired state of the resource.|



### Standard Project Data Structure
#### Json Example
```json
{
  "controller_execution_environments": [
    {
      "name": "My EE",
      "image": "quay.io/ansible/awx-ee"
    }
  ]
}
```
#### Yaml Example
```yaml
---
controller_execution_environments:
  - name: "My EE"
    image: quay.io/ansible/awx-ee
```

## Playbook Examples
### Standard Role Usage
```yaml
---
- name: Add Execution Environments to controller
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    controller_execution_environments:
      name: "My EE"
      image: quay.io/ansible/awx-ee

  tasks:
    - name: Add Execution Environments
      include_role:
        name: redhat_cop.controller_configuration.execution_environments
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
