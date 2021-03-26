# redhat_cop.tower_configuration.execution_environments
## Description
An Ansible Role to create execution_environments in Ansible Tower.

## Requirements
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
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
|`tower_execution_environments`|`see below`|yes|Data structure describing your organization or organizations Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add execution_environments task does not include sensitive information.
tower_configuration_execution_environments_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of tower configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_execution_environments_secure_logging`|`False`|no|Whether or not to include the sensitive execution_environments role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

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
  "tower_execution_environments": [
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
tower_execution_environments:
  - name: "My EE"
    image: quay.io/ansible/awx-ee
```

## Playbook Examples
### Standard Role Usage
```yaml
---
- name: Add Execution Environments to Tower
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    tower_execution_environments:
      name: "My EE"
      image: quay.io/ansible/awx-ee

  tasks:
    - name: Add Execution Environments
      include_role:
        name: redhat_cop.tower_configuration.execution_environments
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
