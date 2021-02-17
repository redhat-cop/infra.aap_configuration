# tower_configuration_instance_groups
## Description
An Ansible Role to create instance groups in Ansible Tower.

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
|`tower_instance_groups`|`see below`|yes|Data structure describing your instance groups Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add instance groups task does not include sensitive information.
tower_configuration_instance_groups_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of tower configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_instance_groups_secure_logging`|`False`|no|Whether or not to include the sensitive instance groups role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Name of this instance group.|
|`new_name`|""|str|no|Setting this option will change the existing name (looked up via the name field).|
|`description`|`False`|no|str|Description to use for the job template.|
|`credential`|""|no|str|Credential to authenticate with Kubernetes or OpenShift.  Must be of type "Kubernetes/OpenShift API Bearer Token". Will make instance part of a Container Group. |
|`policy_instance_percentage`|""|no|int|Minimum percentage of all instances that will be automatically assigned to this group when new instances come online.|
|`policy_instance_minimum`|""|no|int|Static minimum number of Instances that will be automatically assign to this group when new instances come online.|
|`policy_instance_list`|""|no|list|List of exact-match Instances that will be assigned to this group.|
|`pod_spec_override`|""|no|str|A custom Kubernetes or OpenShift Pod specification.|
|`instances`|""|no|list|The instances associated with this instance_group.|
|`state`|`present`|no|str|Desired state of the resource.|

### Standard Project Data Structure
#### Yaml Example
```yaml
---
tower_instance_groups:
  - name: test_instance_group
```

## Playbook Examples
### Standard Role Usage
```yaml
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
    - {role: redhat_cop.tower_configuration.instance_groups, when: tower_instance_groups is defined}
```
## License
[MIT](LICENSE)

## Author
[Sean Sullivan](https://github.com/Wilk42)
