# controller_configuration.organizations
## Description
An Ansible Role to create Organizations on Ansible Controller.

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
|`controller_organizations`|`see below`|yes|Data structure describing your organization or organizations Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add organization task does not include sensitive information.
controller_configuration_organizations_secure_logging defaults to the value of controller_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_organizations_secure_logging`|`False`|no|Whether or not to include the sensitive Organization role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`controller_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables
The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`controller_configuration_organizations_async_retries`|30|no|This variable sets the number of retries to attempt for the role.|
|`controller_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`controller_configuration_organizations_async_delay`|1|no|This sets the delay between retries for the role.|

## Organization Data Structure
This role accepts two data models. A simple straightforward easy to maintain model, and another based on the controller api. The 2nd one is more complicated and includes more detail, and is compatiable with controller import/export.

### Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`name`|""|yes|Name of Organization|
|`description`|`False`|no|Description of  of Organization.|
|`custom_virtualenv`|""|no|Local absolute file path containing a custom Python virtualenv to use.|
|`max_hosts`|""|no|The max hosts allowed in this organization.|
|`instance_groups`|""|no|list of Instance Groups for this Organization to run on.|
|`galaxy_credentials`|""|no|The credentials to use with private automationhub.|
|`default_environment`|""|no|Default Execution Environment to use for jobs owned by the Organization.|
|`notification_templates_started`|""|no|The notifications on started to use for this organization in a list.|
|`notification_templates_success`|""|no|The notifications on success to use for this organization in a list.|
|`notification_templates_error`|""|no|The notifications on error to use for this organization in a list.|
|`notification_templates_approvals`|""|no|The notifications for approval to use for this organization in a list.|
|`state`|`present`|no|Desired state of the resource.|
|`assign_galaxy_credentials_to_org`|`True`|no|Boolean to indicate whether credentials should be assigned or not. It should be noted that credentials must exist before adding it. |

### Standard Organization Data Structure model
#### Json Example
```json
{
    "controller_organizations": [
      {
        "name": "Default",
        "description": "This is the Default Group"
      },
      {
        "name": "Automation Group",
        "description": "This is the Automation Group",
        "custom_virtualenv": "/opt/cust/enviroment/",
        "max_hosts": 10,
        "galaxy_credentials": "Automation Hub",
        "notification_templates_error": [
          "Slack_for_testing"
        ]
      }
    ]
}
```
#### Yaml Example
```yaml
---
controller_organizations:
- name: Default
  description: This is the Default Group
- name: Automation Group
  description: This is the Automation Group
  custom_virtualenv: "/opt/cust/enviroment/"
  max_hosts: 10
```

#### Controller Export Data structure model
##### Yaml Example
```yaml
---
controller_organizations:
- name: Satellite
  description: Satellite
  max_hosts: 0
  custom_virtualenv:
  related:
    notification_templates_started: []
    notification_templates_success: []
    notification_templates_error:
    - name: irc-satqe-chat-notification
    notification_templates_approvals: []
- name: Default
  description: Default
  max_hosts: 0
  custom_virtualenv:
  galaxy_credentials:
    - Automation Hub
  related:
    notification_templates_started: []
    notification_templates_success: []
    notification_templates_error: []
    notification_templates_approvals: []
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
    - {role: redhat_cop.controller_configuration.organizations, when: controller_organizations is defined}
```
## License
[MIT](LICENSE)

## Author
[Sean Sullivan](https://github.com/sean-m-sullivan)
