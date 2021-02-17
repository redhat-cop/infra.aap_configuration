# tower_configuration.workflow_launch
## Description
An Ansible Role to launch a job template in Ansible Tower.

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
|`tower_workflow_launch_jobs`|`see below`|yes|Data structure describing workflow or workflows to launch Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the workflow launch task does not include sensitive information.
tower_configuration_workflow_launch_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of tower configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_workflow_launch_secure_logging`|`False`|no|Whether or not to include the sensitive ad_hoc_command role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|The name or id of the project to update.|
|`organization`|""|no|str|Organization the workflow job template exists in. Used for lookup|
|`inventory`|""|no|str|Inventory to use for the job ran with this workflow, only used if prompt for inventory is set.|
|`limit`|""|no|str|Limit to use for the job_template.|
|`scm_branch`|""|no|str|A specific of the SCM project to run the template on.|
|`extra_vars`|""|no|str|Any extra vars required to launch the job. ask_extra_vars needs to be set to True via tower_job_template module.|
|`wait`|""|no|bool|Wait for the job to complete.|
|`interval`|""|no|int|The interval to request an update from Tower.|
|`timeout`|""|no|int|If waiting for the job to complete this will abort after this amount of seconds.|

### Standard Project Data Structure
#### Yaml Example
```yaml
---
tower_workflow_launch_jobs:
  - name: test-workflow

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
    - {role: redhat_cop.tower_configuration.workflow_launch, when: tower_ad_hoc_commands is defined}

```
## License
[MIT](LICENSE)

## Author
[Sean Sullivan](https://github.com/Wilk42)
