# controller_configuration.groups
## Description
An Ansible Role to create Groups on Ansible Controller.

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
|`controller_groups`|`see below`|yes|Data structure describing your group or groups Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add groups task does not include sensitive information.
controller_configuration_groups_secure_logging defaults to the value of controller_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_groups_secure_logging`|`False`|no|Whether or not to include the sensitive Group role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`controller_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables
The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`controller_configuration_groups_async_retries`|30|no|This variable sets the number of retries to attempt for the role.|
|`controller_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`controller_configuration_groups_async_delay`|1|no|This sets the delay between retries for the role.|

### Formating Variables
Variables can use a standard Jinja templating format to describe the resource.

Example:
```json
{{ variable }}
```

Because of this it is difficult to provide controller with the required format for these fields.

The workaround is to use the following format:
```json
{  { variable }}
```
The role will strip the double space between the curly bracket in order to provide controller with the correct format for the Variables.

## Data Structure
### Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`name`|""|yes|Name of Group|
|`new_name`|""|yes|Name of Group, used in updating a Group.|
|`description`|`False`|no|Description of  of Group.|
|`inventory`|""|yes| Name of inventory|
|`variables`|{}|no| variables applicable to group.|
|`hosts`|""|no | hosts (list) in group|
|`children`|""|no|  List of groups that should be nested inside in this group|
|`state`|`present`|no|Desired state of the resource.|


### Standard Organization Data Structure
#### Json Example
```json
{
    "controller_groups": [
      {
        "name": "PSQL_Servers",
        "description": "Default",
        "inventory": "Source Control",
        "variables": {
        "my_var": true
        }
      }
    ]
}
```
#### Yaml Example
```yaml
---
controller_groups:
- name: PSQL_Servers
  description: Group for Postgres SQL Servers
  inventory: Default
  variables:
    myvars: example1
  hosts:
   - PSQL1
   - PSQL2
   - PSQL3
  children:
   - group1
   - group2
   - group3
```

## Playbook Examples
### Standard Role Usage
```yaml
---
- name: Playbook to configure ansible controller post installation
  hosts: localhost
  connection: local
  # Define following vars here, or in controller_configs/controller_auth.yml
  # controller_hostname: ansible-controller-web-svc-test-project.example.com
  # controller_username: admin
  # controller_password: changeme
  pre_tasks:
    - name: Include vars from controller_configs directory
      include_vars:
        dir: ./yaml
        ignore_files: [controller_config.yml.template]
        extensions: ["yml"]
  roles:
    - {role: redhat_cop.controller_configuration.groups, when: controller_groups is defined}
```
## License
[MIT](LICENSE)

## Author
[Wei-Yen Tan](https://github.com/weiyentan)
[Andrew J. Huffman](https://github.com/ahuffman)
[Sean Sullivan](https://github.com/sean-m-sullivan)
