# Ansible Role infra.aap_configuration.gateway_organizations

## Description

An Ansible Role to add Organizations on Ansible Automation gateway.

## Requirements

This role requires both `ansible.platform` and `ansible.controller` collections. Note that the `awx.awx` collection will not work with this role. See the `controller_organizations` role for the AWX/Controller only implementation.

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
|`aap_organizations`|`see below`|yes|Data structure describing your organizations Described below.||
|`assign_galaxy_credentials_to_org`|`true`|no|Boolean to indicate whether credentials should be assigned or not. It should be noted that credentials must exist before adding it. The dispatch role will set this to `false`, before re-running the role with it set to `true`. ||
|`assign_default_ee_to_org`|`true`|no|Boolean to indicate whether default execution environment should be assigned or not. It should be noted that execution environment must exist before adding it. The dispatch role will set this to `false`, before re-running the role with it set to `true`. ||
|`assign_notification_templates_to_org`|`true`|no|Boolean to indicate whether notification templates should be assigned or not. It should be noted that the templates must exist before adding them. The dispatch role will set this to `false`, before re-running the role with it set to `true`. ||
|`assign_instance_groups_to_org`|`true`|no|Boolean to indicate whether an instance group should be assigned or not. It should be noted that the instance group must exist before adding it. ||

### Enforcing defaults

The following Variables compliment each other.
If Both variables are not set, enforcing default values is not done.
Enabling these variables enforce default values on options that are optional in the controller API.
This should be enabled to enforce configuration and prevent configuration drift. It is recommended to be enabled, however it is not enforced by default.

Enabling this will enforce configuration without specifying every option in the configuration files.

'gateway_organizations_enforce_defaults' defaults to the value of 'aap_configuration_enforce_defaults' if it is not explicitly called. This allows for enforced defaults to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`gateway_organizations_enforce_defaults`|`false`|no|Whether or not to enforce default option values on only the applications role|
|`aap_configuration_enforce_defaults`|`false`|no|This variable enables enforced default values as well, but is shared across multiple roles, see above.|

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add ee_registry task does not include sensitive information.
aap_organizations_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_organizations_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`aap_organizations_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`aap_organizations_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`aap_organizations_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Organization Arguments

Options for the `aap_organizations` variable:

| Variable Name                      | Default Value | Required | Type | Description                                                                      |
|:-----------------------------------|:-------------:|:--------:|:----:|:---------------------------------------------------------------------------------|
| `name`                             |      N/A      |   yes    | str  | The name of the resource                                                         |
| `new_name`                         |      N/A      |    no    | str  | Setting this option will change the existing name (looked up via the name field) |
| `description`                      |      N/A      |    no    | str  | Description of the organization                                                  |
| `custom_virtualenv`                |      N/A      |    no    | str  | Local absolute file path containing a custom Python virtualenv to use.           |
| `max_hosts`                        |      N/A      |    no    | int  | The max hosts allowed in this organization.                                      |
| `instance_groups`                  |      N/A      |    no    | list | list of Instance Groups for this Organization to run on.                         |
| `galaxy_credentials`               |      N/A      |    no    | list | The credentials to use with private automation hub.                              |
| `default_environment`              |      N/A      |    no    | str  | Default Execution Environment to use for jobs owned by the Organization.         |
| `notification_templates_started`   |      N/A      |    no    | list | The notifications on started to use for this organization in a list.             |
| `notification_templates_success`   |      N/A      |    no    | list | The notifications on success to use for this organization in a list.             |
| `notification_templates_error`     |      N/A      |    no    | list | The notifications on error to use for this organization in a list.               |
| `notification_templates_approvals` |      N/A      |    no    | list | The notifications for approval to use for this organization in a list.           |
| `state`                            |   `present`   |    no    | str  | Desired state of the resource.                                                   |

### Unique value

- `name`

## Usage

### Json Example

- Create 2 Organizations

```json
{
    "aap_organizations": [
      {
        "name": "Default",
        "description": "This is the Default Group"
      },
      {
        "name": "Automation Group",
        "description": "This is the Automation Group",
        "custom_virtualenv": "/opt/cust/environment/",
        "max_hosts": 10,
        "galaxy_credentials": "Automation Hub",
        "notification_templates_error": [
          "Slack_for_testing"
        ]
      }
    ]
}
```

### Yaml Example

- Check that "Deprecated Org" doesn't exist
- Check that Org 1 exists
- Get or create Org 2
- Rename Org 3

File name: `data/aap_organizations.yml`

```yaml
---
aap_organizations:
- name: Default
  description: This is the Default Group
- name: Automation Group
  description: This is the Automation Group
  custom_virtualenv: "/opt/cust/environment/"
  max_hosts: 10
```

### Run Playbook

File name: [configure_aap.yml](https://github.com/redhat-cop/infra.aap_configuration/blob/devel/playbooks/configure_aap.yml) can be found in the top level playbooks directory.

```shell
ansible-playbook infra.aap_configuration.configure_aap.yml
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
