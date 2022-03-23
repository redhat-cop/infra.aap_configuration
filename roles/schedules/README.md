# controller_configuration.schedules
## Description
An Ansible Role to create Schedules on Ansible Controller.

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
|`controller_schedules`|`see below`|yes|Data structure describing your schedule or schedules Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add schedules task does not include sensitive information.
controller_configuration_schedules_secure_logging defaults to the value of controller_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_schedules_secure_logging`|`False`|no|Whether or not to include the sensitive Schedules role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`controller_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables
The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`controller_configuration_schedules_async_retries`|30|no|This variable sets the number of retries to attempt for the role.|
|`controller_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`controller_configuration_schedules_async_delay`|1|no|This sets the delay between retries for the role.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Name of Job Template|
|`new_name`|""|str|no|Setting this option will change the existing name (looked up via the name field).|
|`description`|`False`|no|str|Description to use for the job template.|
|`rrule`|""|yes|str|A value representing the schedules iCal recurrence rule. See the awx.awx.schedule plugin for help constructing this value|
|`extra_data`|`{}`|no|dict|Extra vars for the job template. Only allowed if prompt on launch|
|`inventory`|""|no|str|Inventory applied to job template, assuming the job template prompts for an inventory.|
|`scm_branch`|Project default|no|str|Branch to use in the job run. Project default used if not set. Only allowed if `allow_override` set to true on project|
|`job_type`|Job template default|no|str|The job type used for the job template.|
|`job_tags`|""|no|str|Comma separated list of tags to apply to the job|
|`skip_tags`|""|no|str|Comma separated list of tags to skip for the job|
|`limit`|""|no|str|A host pattern to constrain the list of hosts managed or affected by the playbook|
|`diff_mode`|Job template default|no|bool|Enable diff mode for the job template|
|`verbosity`|Job template default|no|int|Level of verbosity for the job. Only allowed if configured to prompt on launch|
|`unified_job_template`|""|no|string|Name of unified job template to schedule. Required if state='present.|
|`enabled`|`true`|no|bool|Enabled processing of this job template|
|`state`|`present`|no|str|Desired state of the resource.|



### Standard Schedule Data Structure
#### Json Example
```json
"controller_schedules": [
    {
      "name": "Demo Schedule",
      "description": "A demonstration",
      "unified_job_template": "Demo Job Template",
      "rrule": "DTSTART:20191219T130551Z RRULE:FREQ=DAILY;INTERVAL=1;COUNT=1",
      "extra_data": {
        "scheduled": true
      },
      "verbosity": 1
    }
  ]

```
#### Yaml Example
```yaml
---
controller_schedules:
  - name: Demo Schedule
    description: A demonstration
    unified_job_template: Demo Job Template
    rrule: "DTSTART:20191219T130551Z RRULE:FREQ=DAILY;INTERVAL=1;COUNT=1"
    extra_data:
      scheduled: true
    verbosity: 1
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
    - {role: redhat_cop.controller_configuration.schedules, when: controller_schedules is defined}
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
