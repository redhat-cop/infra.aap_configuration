# controller_configuration.configure_controller.yml playbook

## Description

An Ansible playbook to run any defined configurations on Ansible Controller.

## Requirements

ansible-galaxy collection install  -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx
  or
  ansible.controller

## Usage

The following command will invoke the playbook with the ansible.controller collection

```console
ansible-playbook infra.controller_configuration.configure_controller.yml
```

## Examples

Examples of the playbooks in use can be found in the examples folder.

## Variables

### Standard Controller Variables

|Variable Name|Default Value|Required|Description|Example|
|:---|:---:|:---:|:---|:---|
|`controller_state`|"present"|no|The state all objects will take unless overriden by object default|'absent'|
|`controller_hostname`|""|yes|URL to the Ansible Controller Server.|127.0.0.1|
|`controller_validate_certs`|`True`|no|Whether or not to validate the Ansible Controller Server's SSL certificate.||
|`controller_username`|""|yes|Admin User on the Ansible Controller Server.||
|`controller_password`|""|yes|Controller Admin User's password on the Ansible Controller Server.  This should be stored in an Ansible Vault at vars/controller-secrets.yml or elsewhere and called from a parent playbook.||
|`controller_oauthtoken`|""|yes|Controller Admin User's token on the Ansible Controller Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`controller_configs_dir`|`see role`|no|.|Directory with Controller configs. Falls back to env CONTROLLER_CONFIGS_DIR. Defaults to $PWD/configs|

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add ad hoc commands task does not include sensitive information.
controller_configuration_ad_hoc_command_secure_logging defaults to the value of controller_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure

### Config Top Level Vars

|Variable Name|Default Value|Description|
|:---:|:---:|:---:|
|`controller_ad_hoc_commands`|`see role`|Data structure describing your ad hoc commands to run . Described in role.|
|`controller_ad_hoc_commands_cancel`|`see role`|Data structure describing your ad hoc jobs to cancel . Described in role.|
|`controller_applications`|`see role`|Data structure describing your applications. Described in role.|
|`controller_credential_input_sources`|`see role`|Data structure describing your credential input sources . Described in role.|
|`controller_credential_types`|`see role`|Data structure describing your credential types . Described in role.|
|`controller_credentials`|`see role`|Data structure describing your credentials . Described in role.|
|`controller_execution_environments`|`see role`|Data structure describing your organization or organizations . Described in role.|
|`controller_groups`|`see role`|Data structure describing your group or groups . Described in role.|
|`controller_hosts`|`see role`|Data structure describing your host entries . Described in role.|
|`controller_instance_groups`|`see role`|Data structure describing your instance groups . Described in role.|
|`controller_inventories`|`see role`|Data structure describing your inventories . Described in role.|
|`controller_inventory_sources`|`see role`|Data structure describing your inventory sources . Described in role.|
|`controller_launch_jobs`|`see role`|Data structure describing the jobs to launch . Described in role.|
|`controller_templates`|`see role`|Data structure describing your job template or job templates . Described in role.|
|`controller_cancel_jobs`|`see role`|Data structure describing jobs to cancel . Described in role.|
|`controller_labels`|`see role`|Data structure describing your label or labels . Described in role.|
|`controller_license`|`see role`|Data structure describing your license for controller, . Described in role.|
|`controller_notifications`|`see role`|Data structure describing your notification entries . Described in role.|
|`controller_organizations`|`see role`|Data structure describing your organization or organizations . Described in role.|
|`controller_projects`|`see role`|Data structure describing your project or projects . Described in role.|
|`controller_roles`|`see role`|Data structure describing your RBAC entries . Described in role.|
|`controller_schedules`|`see role`|Data structure describing your schedule or schedules . Described in role.|
|`controller_settings`|`see role`|Data structure describing your settings . Described in role.|
|`controller_teams`|`see role`|Data structure describing your Teams . Described in role.|
|`controller_user_accounts`|`see role`|Data structure describing your user entries . Described in role.|
|`workflow_job_templates`|`see role`|Data structure describing your workflow job templates . Described in role.|
|`controller_workflow_launch_jobs`|`see role`|Data structure describing workflow or workflows to launch . Described in role.|

### Standard Configs Folder Data Structure

```yaml
---
└── configs
    ├── ad_hoc_command_cancel_defaults.yml
    ├── ad_hoc_commands.yml
    ├── applications.yml
    ├── controller_auth.yml
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
    └── workflows_launch.yml
```

## Configuring Continuous Deployment

This section explains how to setup the Continuous Deployment (CD) of the defined configurations on Ansible controller when a event occurs(usually a merge event) in the git repository where the definitions are kept.

This procedure has been tested with **gitlab** git server

You have make the following configurations in order to configure CD integration:

1. Configure a Project and a job template with [webhook](https://docs.ansible.com/automation-controller/latest/html/userguide/webhooks.html#id2) property enabled in the Controller pointing to the playbook in charge of CD, you can find an example [here](https://github.com/redhat-cop/controller_configuration/blob/devel/tests/playbooks/cd_gitlab_webhook_trigger.yml).

2. Configure [project webhook](https://docs.gitlab.com/ee/user/project/integrations/webhook_events.html) on the project where defined configurations are hosted.

## License

[GPL-3.0](https://github.com/redhat-cop/controller_configuration#licensing)

## Author

[Sean Sullivan](https://github.com/sean-m-sullivan/)
