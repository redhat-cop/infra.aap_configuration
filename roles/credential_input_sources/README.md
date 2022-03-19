# controller_configuration.credential_input_sources
## Description
An Ansible Role to create credential input sources on Ansible Controller, the below example is for CyberArk as an input source, change accordingly to match your input source type.

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
|`controller_credential_input_sources`|`see below`|yes|Data structure describing your credential input sources Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add credential input source task does not include sensitive information.
controller_configuration_credential_input_sources_secure_logging defaults to the value of controller_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_credential_input_sources_secure_logging`|`False`|no|Whether or not to include the sensitive credential_input_source role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`controller_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables
The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`controller_configuration_credential_input_sources_async_retries`|30|no|This variable sets the number of retries to attempt for the role.|
|`controller_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`controller_configuration_credential_input_sources_async_delay`|1|no|This sets the delay between retries for the role.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`target_credential`|""|yes|str|Name of credential to have the input source applied|
|`input_field_name`|""|yes|str|Name of field which will be written by the input source|
|`source_credential`|""|str|no|Name of the source credential which points to a credential source|
|`metadata`|""|str|no|The metadata applied to the source.|
|`description`|`False`|no|str|Description to use for the credential input source.|
|`state`|`present`|no|str|Desired state of the resource.|

For further details on fields see https://docs.ansible.com/ansible-tower/latest/html/userguide/credential_plugins.html

### Standard Project Data Structure
#### Json Example
```json
{
    "controller_credential_input_sources": [
      {
        "source_credential": "cyberark",
        "target_credential": "gitlab",
        "input_field_name": "password",
        "metadata": {
          "object_query": "Safe=MY_SAFE;Object=AWX-user",
          "object_query_format": "Exact"
        },
        "description": "Fill the gitlab credential from CyberArk"
      }
    ]
}
```
#### Yaml Example
```yaml
---
controller_credential_input_sources:
  - source_credential: cyberark
    target_credential: gitlab
    input_field_name: password
    metadata:
      object_query: "Safe=MY_SAFE;Object=AWX-user"
      object_query_format: "Exact"
    description: Fill the gitlab credential from CyberArk
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
    - {role: redhat_cop.controller_configuration.credential_input_sources, when: controller_credential_input_sources is defined}
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
