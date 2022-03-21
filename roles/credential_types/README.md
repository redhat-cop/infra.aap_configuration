# controller_configuration.credential_types
## Description
An Ansible Role to create Credential Types on Ansible Controller.

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
|`controller_credential_types`|`see below`|yes|Data structure describing your credential types Described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add credential type task does not include sensitive information.
controller_configuration_credential_types_secure_logging defaults to the value of controller_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|:---:|:---:|:---:|:---:|
|`controller_configuration_secure_logging`|`False`|no|Whether or not to include the sensitive Credential Type role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`controller_configuration_credential_types_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables
The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`controller_configuration_credential_types_async_retries`|30|no|This variable sets the number of retries to attempt for the role.|
|`controller_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`controller_configuration_credential_types_async_delay`|1|no|This sets the delay between retries for the role.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`name`|""|yes|Name of Credential Type|
|`description`|`False`|no|The description of the credential type to give more detail about it.|
|`injectors`|""|no|Enter injectors using either JSON or YAML syntax. Refer to the Ansible controller documentation for example syntax. See not below on proper formatting.|
|`inputs`|""|no|Enter inputs using either JSON or YAML syntax. Refer to the Ansible controller documentation for example syntax.|
|`kind`|"cloud"|no|The type of credential type being added. Note that only cloud and net can be used for creating credential types.|
|`state`|`present`|no|Desired state of the resource.|

### Formating Injectors
Injectors use a standard Jinja templating format to describe the resource.

Example:
```json
{{ variable }}
```

Because of this it is difficult to provide controller with the required format for these fields.

The workaround is to use the following format:
```json
{  { variable }}
```
The role will strip the double space between the curly bracket in order to provide controller with the correct format for the Injectors.

### Input and Injector Schema
The following detais the data format to use for inputs and injectors. These can be in either YAML or JSON For the most up to date information and more details see [Custom Credential Types - Ansible Tower Documentation](https://docs.ansible.com/ansible-tower/latest/html/userguide/credential_types.html)

#### Input Schema
```yaml
fields:
  - type: string
    id: username
    label: Username
  - type: string
    id: password
    label: Password
    secret: true
required:
  - username
  - password
```
#### Injector Schema
```json
{
  "file": {
      "template": "[mycloud]\ntoken={{ api_token }}"
  },
  "env": {
      "THIRD_PARTY_CLOUD_API_TOKEN": "{{ api_token }}"
  },
  "extra_vars": {
      "some_extra_var": "{{ username }}:{{ password }}"
  }
}
```

### Standard Organization Data Structure
#### Json Example
```json
{
    "controller_credential_types": [
      {
        "name": "REST API Credential",
        "description": "REST API Credential",
        "kind": "cloud",
        "inputs": {
          "fields": [
            {
              "type": "string",
              "id": "rest_username",
              "label": "REST Username"
            },
            {
              "secret": true,
              "type": "string",
              "id": "rest_password",
              "label": "REST Password"
            }
          ],
          "required": [
            "rest_username",
            "rest_password"
          ]
        },
        "injectors": {
          "extra_vars": {
            "rest_password": "{  { rest_password }}",
            "rest_username": "{  { rest_username }}"
          },
          "env": {
            "rest_username_env": "{  { rest_username }}",
            "rest_password_env": "{  { rest_password }}"
          }
        }
      }
    ]
}
```
#### Yaml Example
```yaml
---
controller_credential_types:
- name: REST API Credential
  description: REST API Credential
  inputs:
    fields:
    - type: string
      id: rest_username
      label: REST Username
    - secret: true
      type: string
      id: rest_password
      label: REST Password
    required:
    - rest_username
    - rest_password
  injectors:
    extra_vars:
      rest_password: "{  { rest_password }}"
      rest_username: "{  { rest_username }}"
    env:
      rest_username_env: "{  { rest_username }}"
      rest_password_env: "{  { rest_password }}"
```
## Playbook Examples
### Standard Role Usage
```yaml
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
    - {role: redhat_cop.controller_configuration.credential_types, when: controller_credential_types is defined}
```
## License
[MIT](LICENSE)

## Author
[Sean Sullivan](https://github.com/sean-m-sullivan)
