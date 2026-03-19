# Ansible Role infra.aap_configuration.gateway_role_definitions

## Description

An Ansible Role to create/update/remove Role Definitions on Ansible gateway.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---|:---:|:---:|:---|:---|
|`platform_state`|"present"|no|The state all objects will take unless overridden by object default|'absent'|
|`aap_hostname`|""|yes|URL to the Ansible Automation Platform Server.|127.0.0.1|
|`aap_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Platform Server's SSL certificate.||
|`aap_username`|""|no|Admin User on the Ansible Automation Platform Server. Either username / password or oauthtoken need to be specified.||
|`aap_password`|""|no|Platform Admin User's password on the Server.  This should be stored in an Ansible Vault at vars/platform-secrets.yml or elsewhere and called from a parent playbook.||
|`aap_token`|""|no|Controller Admin User's token on the Ansible Automation Platform Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.||
|`aap_request_timeout`|`10`|no|Specify the timeout in seconds Ansible should use in requests to the Ansible Automation Platform host.||
|`gateway_role_definitions`|`see below`|yes|Data structure describing your role definitions Described below.||

### Enforcing defaults

The following Variables complement each other.
If Both variables are not set, enforcing default values is not done.
Enabling these variables enforce default values on options that are optional in the controller API.
This should be enabled to enforce configuration and prevent configuration drift. It is recommended to be enabled, however it is not enforced by default.

Enabling this will enforce configuration without specifying every option in the configuration files.

'gateway_role_definitions_enforce_defaults' defaults to the value of 'aap_configuration_enforce_defaults' if it is not explicitly called. This allows for enforced defaults to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`gateway_role_definitions_enforce_defaults`|`false`|no|Whether or not to enforce default option values on only the role definitions role|
|`aap_configuration_enforce_defaults`|`false`|no|This variable enables enforced default values as well, but is shared globally.|

### Secure Logging Variables

The following Variables complement each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add role definitions task does not include sensitive information.
gateway_role_definitions_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of gateway configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`gateway_role_definitions_secure_logging`|`false`|no|Whether or not to include the sensitive role definitions role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`gateway_role_definitions_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`gateway_role_definitions_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|0|no|This variable sets the loop_delay for the role globally.|
|`gateway_role_definitions_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Role Definition Variables

**WARNING: This role will only work in AAP 2.6+** Options for the `gateway_role_definitions` variable:

| Variable Name       | Default Value | Required | Type | Description                                                                                           |
|:--------------------|:-------------:|:--------:|:----:|:------------------------------------------------------------------------------------------------------|
| `content_type`      |      N/A      |   yes    | str  | The content type for which the role applies (e.g., awx.inventory)                                     |
| `description`       |      N/A      |    no    | str  | Description of the role definition                                                                    |
| `name`              |      N/A      |   yes    | str  | The name of the role definition (must be unique)                                                      |
| `new_name`          |      N/A      |    no    | str  | Setting this option will change the existing name (looked up via the name field)                      |
| `permissions`       |      N/A      |   yes    | list | List of permission strings to associate with the role (e.g., awx.view_inventory)                      |
| `state`             |   `present`   |    no    | str  | Desired state of the resource.                                                                        |
|`register`           |         ""    |   no     | str  | Variable to set based on the result of the object creation/modification                               |

#### Content Type

Below are the available content_types that can be used when managing role definitions. Under the content type names, are available permissions that can used with those content types.

`shared.organization`

- shared.audit_organization
- shared.change_organization
- shared.delete_organization
- shared.member_organization
- shared.view_organization
- shared.add_team
- shared.change_team
- shared.delete_team
- shared.member_team
- shared.view_team
- awx.add_executionenvironment
- awx.change_executionenvironment
- awx.delete_executionenvironment
- awx.add_project
- awx.change_project
- awx.delete_project
- awx.update_project
- awx.use_project
- awx.view_project
- awx.change_jobtemplate
- awx.delete_jobtemplate
- awx.execute_jobtemplate
- awx.view_jobtemplate
- awx.add_credential
- awx.change_credential
- awx.delete_credential
- awx.use_credential
- awx.view_credential
- awx.add_notificationtemplate
- awx.change_notificationtemplate
- awx.delete_notificationtemplate
- awx.view_notificationtemplate
- awx.add_inventory
- awx.adhoc_inventory
- awx.change_inventory
- awx.delete_inventory
- awx.update_inventory
- awx.use_inventory
- awx.view_inventory
- awx.add_workflowjobtemplate
- awx.approve_workflowjobtemplate
- awx.change_workflowjobtemplate
- awx.delete_workflowjobtemplate
- awx.execute_workflowjobtemplate
- awx.view_workflowjobtemplate
- eda.add_activation
- eda.change_activation
- eda.delete_activation
- eda.disable_activation
- eda.enable_activation
- eda.restart_activation
- eda.view_activation
- eda.view_auditrule
- eda.view_rulebookprocess
- eda.add_credentialinputsource
- eda.change_credentialinputsource
- eda.delete_credentialinputsource
- eda.view_credentialinputsource
- eda.add_decisionenvironment
- eda.change_decisionenvironment
- eda.delete_decisionenvironment
- eda.view_decisionenvironment
- eda.add_edacredential
- eda.change_edacredential
- eda.delete_edacredential
- eda.view_edacredential
- eda.add_eventstream
- eda.change_eventstream
- eda.delete_eventstream
- eda.view_eventstream
- eda.add_project
- eda.change_project
- eda.delete_project
- eda.sync_project
- eda.view_project
- eda.view_rulebook

`shared.team`

- shared.change_team
- shared.delete_team
- shared.member_team
- shared.view_team

`awx.credential`

- awx.change_credential
- awx.delete_credential
- awx.use_credential
- awx.view_credential

`awx.executionenvironment`

- awx.change_executionenvironment
- awx.delete_executionenvironment

`awx.instancegroup`

- awx.change_instancegroup
- awx.delete_instancegroup
- awx.use_instancegroup
- awx.view_instancegroup

`awx.inventory`

- awx.adhoc_inventory
- awx.change_inventory
- awx.delete_inventory
- awx.update_inventory
- awx.use_inventory
- awx.view_inventory

`awx.jobtemplate`

- awx.change_jobtemplate
- awx.delete_jobtemplate
- awx.execute_jobtemplate
- awx.view_jobtemplate

`awx.notificationtemplate`

- awx.change_notificationtemplate
- awx.delete_notificationtemplate
- awx.view_notificationtemplate

`awx.project`

- awx.change_project
- awx.delete_project
- awx.update_project
- awx.use_project
- awx.view_project

`awx.workflowjobtemplate`

- awx.approve_workflowjobtemplate
- awx.change_workflowjobtemplate
- awx.delete_workflowjobtemplate
- awx.execute_workflowjobtemplate
- awx.view_workflowjobtemplate

`eda.activation`

- eda.change_activation
- eda.delete_activation
- eda.disable_activation
- eda.enable_activation
- eda.restart_activation
- eda.view_activation
- eda.view_auditrule
- eda.view_rulebookprocess

`eda.credentialinputsource`

- eda.change_credentialinputsource
- eda.delete_credentialinputsource
- eda.view_credentialinputsource

`eda.decisionenvironment`

- eda.change_decisionenvironment
- eda.delete_decisionenvironment
- eda.view_decisionenvironment

`eda.edacredential`

- eda.change_edacredential
- eda.delete_edacredential
- eda.view_edacredential

`eda.eventstream`

- eda.change_eventstream
- eda.delete_eventstream
- eda.view_eventstream

`eda.project`

- eda.change_project
- eda.delete_project
- eda.sync_project
- eda.view_project
- eda.view_rulebook

`galaxy.ansiblerepository`

- galaxy.add_ansiblerepository
- galaxy.change_ansiblerepository
- galaxy.delete_ansiblerepository
- galaxy.manage_roles_ansiblerepository
- galaxy.modify_ansible_repo_content
- galaxy.rebuild_metadata_ansiblerepository
- galaxy.repair_ansiblerepository
- galaxy.sign_ansiblerepository
- galaxy.sync_ansiblerepository
- galaxy.view_ansiblerepository

`galaxy.collectionremote`

- galaxy.add_collectionremote
- galaxy.change_collectionremote
- galaxy.delete_collectionremote
- galaxy.manage_roles_collectionremote
- galaxy.view_collectionremote

`galaxy.containernamespace`

- galaxy.add_containernamespace
- galaxy.change_containernamespace
- galaxy.delete_containernamespace
- galaxy.manage_roles_containernamespace
- galaxy.namespace_add_containerdistribution
- galaxy.namespace_change_containerdistribution
- galaxy.namespace_change_containerpushrepository
- galaxy.namespace_delete_containerdistribution
- galaxy.namespace_modify_content_containerpushrepository
- galaxy.namespace_pull_containerdistribution
- galaxy.namespace_push_containerdistribution
- galaxy.namespace_view_containerdistribution
- galaxy.namespace_view_containerpushrepository
- galaxy.view_containernamespace

`galaxy.containerrepository`

- galaxy.add_containerrepository
- galaxy.build_image_containerrepository
- galaxy.change_containerrepository
- galaxy.delete_containerrepository
- galaxy.delete_containerrepository_versions
- galaxy.manage_roles_containerrepository
- galaxy.modify_content_containerrepository
- galaxy.sync_containerrepository
- galaxy.view_containerrepository

`galaxy.namespace`

- galaxy.add_namespace
- galaxy.change_namespace
- galaxy.upload_to_namespace

`galaxy.task`

- galaxy.add_task
- galaxy.change_task
- galaxy.delete_task
- galaxy.manage_roles_task
- galaxy.view_task

### Standard Role Definition Data Structure

#### Json Example

```json
{
  "gateway_role_definitions": [
    {
      "name": "Organization Inventory Use",
      "description": "Grants use permissions to inventories for a single organization.",
      "content_type": "awx.inventory",
      "permissions": [
        "awx.view_inventory",
        "awx.use_inventory"
      ]
    },
    {
      "name": "Organization Credential Use",
      "description": "Grants use permissions to inventoriesfor a single organization.",
      "content_type": "awx.credential",
      "permissions": [
        "awx.view_credential",
        "awx.use_credential"
      ]
    },
    {
      "name": "Workflow Template Modify",
      "description": "Grants modify permissions to workflow templates.",
      "content_type": "awx.workflowjobtemplate",
      "permissions": [
        "awx.view_workflowjobtemplate",
        "awx.approve_workflowjobtemplate",
        "awx.change_workflowjobtemplate",
        "awx.delete_workflowjobtemplate",
      ]
    },
  ]
}
```

#### Yaml Example

File name: `configs/gateway_role_definitions.yml`

```yaml
---
gateway_role_definitions:
  - name: Organization Inventory Use
    description: Grants use permissions to inventories for a single organization.
    content_type: shared.organization
    permissions:
      - awx.view_inventory
      - awx.use_inventory
  - name: Organization Credential Use
    description: Grants use permissions to credentials for a single organization.
    content_type: shared.organization
    permissions:
      - awx.view_credential
      - awx.use_credential
  - name: Workflow Template Modify
    description: Grants modify permissions to workflow templates.
    content_type: awx.workflowjobtemplate
    permissions:
      - awx.view_workflowjobtemplate
      - awx.approve_workflowjobtemplate
      - awx.change_workflowjobtemplate
      - awx.delete_workflowjobtemplate
```

## License

[GPLv3+](https://github.com/redhat-cop/infra.aap_configuration/blob/devel/LICENSE)
