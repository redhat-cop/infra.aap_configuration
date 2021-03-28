# tower_configuration.ad_hoc_command
## Description
An Ansible Role to run a list of ad hoc commands in Ansible Tower.

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
|`tower_ad_hoc_commands`|`see below`|yes|Data structure describing your ad hoc commands to run Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add ad hoc commands task does not include sensitive information.
tower_configuration_ad_hoc_command_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of tower configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_ad_hoc_command_secure_logging`|`False`|no|Whether or not to include the sensitive ad_hoc_command role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`job_type`|"run"|no|str|Job_type to use for the ad hoc command. Either run or check.|
|`inventory`|""|str|yes|Inventory to use for the ad hoc command.|
|`limit`|`False`|no|str|Limit to use for the ad hoc command.|
|`credential`|""|yes|str|Credential to use for ad hoc command.|
|`execution_environment`|""|no|str|Execution Environment to use for ad hoc command.|
|`module_name`|""|str|yes|The Ansible module to execute.|
|`module_args`|`False`|no|str|The arguments to pass to the module.|
|`forks`|0|yes|int|The number of forks to use for this ad hoc execution.|
|`verbosity`|0|no|int|Verbosity level for this ad hoc command run|
|`extra_vars`|`False`|no|dict|Extra variables to use for the ad hoc command.|
|`become_enabled`|""|no|bool|If the become flag should be set.|
|`diff_mode`|""|no|bool|Show the changes made by Ansible tasks where supported|
|`wait`|`False`|no|bool|Wait for the command to complete.|
|`interval`|1|no|int|The interval to request an update from Tower.|
|`timeout`|""|no|int|If waiting for the command to complete this will abort after this amount of seconds.|


### Standard Project Data Structure
#### Yaml Example
```yaml
---
tower_ad_hoc_commands:
  - job_type: run
    inventory: localhost
    credential: Demo Credential
    module_name: ping


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
    - {role: redhat_cop.tower_configuration.ad_hoc_command, when: tower_ad_hoc_commands is defined}

```
## License
[MIT](LICENSE)

## Author
[Sean Sullivan](https://github.com/Wilk42)
