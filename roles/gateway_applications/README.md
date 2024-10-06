<<<<<<< HEAD
# controller_configuration.applications

## Description

An Ansible Role to create/update/remove Applications on Ansible Controller.

## Requirements

ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx
  or
  ansible.controller

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---|:---:|:---:|:---|:---|
|`controller_state`|"present"|no|The state all objects will take unless overridden by object default|'absent'|
|`controller_hostname`|""|yes|URL to the Ansible Controller Server.|127.0.0.1|
|`controller_validate_certs`|`True`|no|Whether or not to validate the Ansible Controller Server's SSL certificate.||
|`controller_username`|""|no|Admin User on the Ansible Controller Server. Either username / password or oauthtoken need to be specified.||
|`controller_password`|""|no|Controller Admin User's password on the Ansible Controller Server. This should be stored in an Ansible Vault at vars/controller-secrets.yml or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.||
|`controller_oauthtoken`|""|no|Controller Admin User's token on the Ansible Controller Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.||
|`controller_request_timeout`|`10`|no|Specify the timeout in seconds Ansible should use in requests to the controller host.||
|`controller_applications`|`see below`|yes|Data structure describing your applications, described below. Alias: applications ||

### Enforcing defaults

The following Variables compliment each other.
If Both variables are not set, enforcing default values is not done.
Enabling these variables enforce default values on options that are optional in the controller API.
This should be enabled to enforce configuration and prevent configuration drift. It is recomended to be enabled, however it is not enforced by default.

Enabling this will enforce configurtion without specifying every option in the configuration files.

'controller_configuration_applications_enforce_defaults' defaults to the value of 'controller_configuration_enforce_defaults' if it is not explicitly called. This allows for enforced defaults to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_applications_enforce_defaults`|`False`|no|Whether or not to enforce default option values on only the applications role|
|`controller_configuration_enforce_defaults`|`False`|no|This variable enables enforced default values as well, but is shared across multiple roles, see above.|

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add application task does not include sensitive information.
controller_configuration_applications_secure_logging defaults to the value of controller_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_applications_secure_logging`|`False`|no|Whether or not to include the sensitive Application role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`controller_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`controller_configuration_applications_async_retries`|`{{ controller_configuration_async_retries }}`|no|This variable sets the number of retries to attempt for the role.|
|`controller_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`controller_configuration_applications_async_delay`|`controller_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`controller_configuration_loop_delay`|0|no|This sets the pause between each item in the loop for the roles globally. To help when API is getting overloaded.|
|`controller_configuration_applications_loop_delay`|`controller_configuration_loop_delay`|no|This sets the pause between each item in the loop for the role. To help when API is getting overloaded.|
|`controller_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Application Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Name of application|
|`new_name`|""|no|str|Setting this option will change the existing name (looked up via the name field).|
|`organization`|""|yes|str|Name of the organization for the application|
|`description`|""|no|str|Description to use for the application.|
|`authorization_grant_type`|"password"|yes|str|Grant type for tokens in this application, "password" or "authorization-code"|
|`client_type`|"public"|yes|str|Application client type, "confidential" or "public"|
|`redirect_uris`|""|no|str|Allowed urls list, space separated. Required with "authorization-code" grant type|
|`skip_authorization`|"false"|yes|bool|Set True to skip authorization step for completely trusted applications.|
|`state`|`present`|no|str|Desired state of the application.|
=======
# Ansible Role infra.platform_configuration.applications

## Description

An Ansible Role to create/update/remove Applications on Ansible gateway.

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md)

Variables specific for this role are following:

| Variable Name                                         |                    Default Value                    | Required | Description                                                                                                                                                        |                                        |
|:------------------------------------------------------|:---------------------------------------------------:|:--------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------:|
| `applications_list` (Alias: `applications`)        |           [below](#application-arguments)           |   yes    | Data structure describing your applications entries described below. Alias: applications                                                                           | [more](../../README.md#data-variables) |
| `applications_secure_logging`   |  `gateway_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive Application role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |
| `applications_enforce_defaults` | `gateway_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the applications role                                                                                      |
| `applications_async_retries`    |    `gateway_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                                  |
| `applications_async_delay`      |     `gateway_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                                  |

## Data Structure

### Application Arguments

Options for the `applications_list` variable:

| Variable Name               |    Default Value    | Required | Type | Description                                                                            |
|:----------------------------|:-------------------:|:--------:|:----:|:---------------------------------------------------------------------------------------|
| `name`                      |         N/A         |   yes    | str  | Name of application                                                                    |
| `new_name`                  |         N/A         |    no    | str  | Setting this option will change the existing name (looked up via the name field).      |
| `organization`              |         N/A         |   yes    | str  | Name of the organization for the application                                           |
| `new_organization`          |         N/A         |    no    | str  | The name or ID referencing newly associated organization                               |
| `algorithm`                 |         N/A         |    no    | str  | The OIDC token signing algorithm for this application. Choices: ["", "RS256", "HS256"] |
| `description`               |         N/A         |    no    | str  | Description to use for the application.                                                |
| `authorization_grant_type`  |         N/A         |   yes    | str  | Grant type for tokens in this application, Choices: ["password", "authorization-code"] |
| `client_type`               |         N/A         |   yes    | str  | Application client type. Choices: ["confidential", "public"]                           |
| `redirect_uris`             |         ""          |    no    | str  | Allowed urls list, space separated. Required with "authorization-code" grant type      |
| `skip_authorization`        | N/A(`false` by API) |   yes    | bool | Set True to skip authorization step for completely trusted applications.               |
| `post_logout_redirect_uris` |         ""          |    no    | str  | Allowed Post Logout URIs list, space separated.                                        |
| `user`                      |         ""          |    no    | str  | The user who owns this application.                                                    |
| `state`                     |      `present`      |    no    | str  | Desired state of the application.                                                      |
>>>>>>> 40b40ddac1c00aac7d878bd41af23a6d562296e5

### Standard Application Data Structure

#### Json Example

```json
 {
<<<<<<< HEAD
    "controller_applications": [
      {
        "name": "controller Config Default Application",
        "description": "Generic application, which can be used for oauth tokens",
        "organization": "Default",
        "state": "present",
        "client_type": "confidential",
        "authorization_grant_type": "password"
      }
    ]
=======
  "applications_list": [
    {
      "name": "gateway Config Default Application",
      "description": "Generic application, which can be used for oauth tokens",
      "organization": "Default",
      "state": "present",
      "client_type": "confidential",
      "authorization_grant_type": "password"
    }
  ]
>>>>>>> 40b40ddac1c00aac7d878bd41af23a6d562296e5
}
```

#### Yaml Example

<<<<<<< HEAD
```yaml
---
controller_applications:
  - name: "controller Config Default Application"
    description: "Generic application, which can be used for oauth tokens"
    organization: "Default"
    state: "present"
    client_type: "confidential"
    authorization_grant_type: "password"
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
      ansible.builtin.include_vars:
        dir: ./yaml
        ignore_files: [controller_config.yml.template]
        extensions: ["yml"]
  roles:
    - {role: infra.controller_configuration.applications, when: controller_applications is defined}
=======
File name: `data/gateway_applications.yml`

```yaml
---
applications_list:
- name: "gateway Config Default Application"
  description: "Generic application, which can be used for oauth tokens"
  organization: "Default"
  state: "present"
  client_type: "confidential"
  authorization_grant_type: "password"
```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_applications.yml
>>>>>>> 40b40ddac1c00aac7d878bd41af23a6d562296e5
```

## License

<<<<<<< HEAD
[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)

## Author

[Mike Shriver](https://github.com/mshriver)
=======
[GPLv3](https://github.com/ansible/aap-gateway/gateway_configuration_collection/COPYING)
>>>>>>> 40b40ddac1c00aac7d878bd41af23a6d562296e5
