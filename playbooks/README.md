# tower_configuration.configure_tower.yml playbook
## Description
An Ansible playbook to run any defined configurations on Ansible tower.

## Requirements
ansible-galaxy collection install  -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx
  or
  ansible.tower

## Usage
The following command will invoke the playbook with the awx collection
```console
ansible-playbook redhat_cop.tower_configuration.configure_awx.yml
```
The following command will invoke the playbook with the ansible.tower collection
```console
ansible-playbook redhat_cop.tower_configuration.configure_tower.yml
```

## Variables

### Standard Tower Variables
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`tower_state`|"present"|no|The state all objects will take unless overriden by object default|'absent'|
|`tower_hostname`|""|yes|URL to the Ansible tower Server.|127.0.0.1|
|`tower_validate_certs`|`True`|no|Whether or not to validate the Ansible tower Server's SSL certificate.||
|`tower_username`|""|yes|Admin User on the Ansible tower Server.||
|`tower_password`|""|yes|tower Admin User's password on the Ansible tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`tower_oauthtoken`|""|yes|tower Admin User's token on the Ansible tower Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`tower_configs_dir`|`see role`|no|.|Directory with tower configs. Falls back to env TOWER_CONFIGS_DIR. Defaults to $PWD/configs|

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add ad hoc commands task does not include sensitive information.
tower_configuration_ad_hoc_command_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of tower configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Config Top Level Vars
|Variable Name|Default Value|Description|
|:---:|:---:|:---:|
|`tower_ad_hoc_commands`|`see role`|Data structure describing your ad hoc commands to run . Described in role.|
|`tower_ad_hoc_commands_cancel`|`see role`|Data structure describing your ad hoc jobs to cancel . Described in role.|
|`tower_applications`|`see role`|Data structure describing your applications. Described in role.|
|`tower_credential_input_sources`|`see role`|Data structure describing your credential input sources . Described in role.|
|`tower_credential_types`|`see role`|Data structure describing your credential types . Described in role.|
|`tower_credentials`|`see role`|Data structure describing your credentials . Described in role.|
|`tower_execution_environments`|`see role`|Data structure describing your organization or organizations . Described in role.|
|`tower_groups`|`see role`|Data structure describing your group or groups . Described in role.|
|`tower_hosts`|`see role`|Data structure describing your host entries . Described in role.|
|`tower_instance_groups`|`see role`|Data structure describing your instance groups . Described in role.|
|`tower_inventories`|`see role`|Data structure describing your inventories . Described in role.|
|`tower_inventory_sources`|`see role`|Data structure describing your inventory sources . Described in role.|
|`tower_launch_jobs`|`see role`|Data structure describing the jobs to launch . Described in role.|
|`tower_templates`|`see role`|Data structure describing your job template or job templates . Described in role.|
|`tower_cancel_jobs`|`see role`|Data structure describing jobs to cancel . Described in role.|
|`tower_labels`|`see role`|Data structure describing your label or labels . Described in role.|
|`tower_license`|`see role`|Data structure describing your license for tower, . Described in role.|
|`tower_notifications`|`see role`|Data structure describing your notification entries . Described in role.|
|`tower_organizations`|`see role`|Data structure describing your organization or organizations . Described in role.|
|`tower_projects`|`see role`|Data structure describing your project or projects . Described in role.|
|`tower_roles`|`see role`|Data structure describing your RBAC entries . Described in role.|
|`tower_schedules`|`see role`|Data structure describing your schedule or schedules . Described in role.|
|`tower_settings`|`see role`|Data structure describing your settings . Described in role.|
|`tower_teams`|`see role`|Data structure describing your Teams . Described in role.|
|`tower_user_accounts`|`see role`|Data structure describing your user entries . Described in role.|
|`workflow_job_templates`|`see role`|Data structure describing your workflow job templates . Described in role.|
|`tower_workflow_launch_jobs`|`see role`|Data structure describing workflow or workflows to launch . Described in role.|


### Standard Configs Folder Data Structure
```yaml
---
└── configs
    ├── ad_hoc_command_cancel_defaults.yml
    ├── ad_hoc_commands.yml
    ├── applications.yml
    ├── tower_auth.yml
    ├── credential_input_sources.yml
    ├── credentials.yml
    ├── credential_types.yml
    ├── execution_environments.yml
    ├── groups.yml
    ├── hosts.yml
    ├── instance_groups.yml
    ├── inventories.yml
    ├── inventory_sources.yml
    ├── labels.yml
    ├── launch_jobs.yml
    ├── notifications.yml
    ├── organizations.yml
    ├── projects.yml
    ├── roles.yml
    ├── schedule.yml
    ├── settings_individuale.yml
    ├── settings.yml
    ├── ssh_private_key.yml
    ├── teams.yml
    ├── templates.yml
    ├── user_accounts.yml
    ├── workflows.yml
    └── workfows_launch.yml
```


## License
[MIT](LICENSE)

## Author
[Sean Sullivan](https://github.com/sean-m-sullivan)
