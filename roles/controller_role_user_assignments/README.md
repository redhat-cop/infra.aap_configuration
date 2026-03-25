# Ansible Role infra.aap_configuration.controller_role_user_assignments

## Description

An Ansible Role to create/update/remove Role User Assignments on Ansible Controller **AAP 2.5 ONLY**.

>[!NOTE]
>This role is not included in the default dispatch role dispatcher list because it is AAP 2.5-only. To use it, either call the role directly in your playbook or create a custom dispatcher list that includes it. See the dispatch role's aap_configuration_dispatcher_roles variable for details.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---|:---:|:---:|:---|:---|
|`platform_state`|"present"|no|The state all objects will take unless overridden by object default|'absent'|
|`aap_hostname`|""|yes|URL to the Ansible Automation Platform Server.|127.0.0.1|
|`aap_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Platform Server's SSL certificate.||
|`aap_username`|""|no|Admin User on the Ansible Automation Platform Server. Either username / password or oauthtoken need to be specified.||
|`aap_password`|""|no|Platform Admin User's password on the Server.  This should be stored in an Ansible Vault at vars/platform-secrets.yml or elsewhere and called from a parent playbook.||
|`aap_token`|""|no|Controller Admin User's token on the Ansible Automation Platform Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.||
|`aap_request_timeout`|""|no|Specify the timeout in seconds Ansible should use in requests to the Ansible Automation Platform host.||
|`controller_role_user_assignments`|`see below`|yes|Data structure describing your role user assignments Described below.||

### Enforcing defaults

The following Variables complement each other.
If Both variables are not set, enforcing default values is not done.
Enabling these variables enforce default values on options that are optional in the controller API.
This should be enabled to enforce configuration and prevent configuration drift. It is recommended to be enabled, however it is not enforced by default.

Enabling this will enforce configuration without specifying every option in the configuration files.

'controller_role_user_assignments_enforce_defaults' defaults to the value of 'aap_configuration_enforce_defaults' if it is not explicitly called. This allows for enforced defaults to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_role_user_assignments_enforce_defaults`|`false`|no|Whether or not to enforce default option values on only the role user assignments role|
|`aap_configuration_enforce_defaults`|`false`|no|This variable enables enforced default values as well, but is shared globally.|

### Secure Logging Variables

The following Variables complement each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add role user assignments task does not include sensitive information.
controller_role_user_assignments_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_role_user_assignments_secure_logging`|`false`|no|Whether or not to include the sensitive Role User Assignments role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`controller_role_user_assignments_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`controller_role_user_assignments_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|0|no|This variable sets the loop_delay for the role globally.|
|`controller_role_user_assignments_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Role User Assignment Variables

**WARNING: This role will only work in AAP 2.5** Options for the `controller_role_user_assignments` variable:

| Variable Name       | Default Value | Required | Type | Description                                                                                           |
|:--------------------|:-------------:|:--------:|:----:|:------------------------------------------------------------------------------------------------------|
| `object_id`         |      N/A      |    yes   | int  | Primary key of the object this assignment applies to.                                                 |
| `role_definition`   |      N/A      |    yes   | str  | The name or id of the role definition to assign to the user.                                          |
| `state`             |   `present`   |    no    | str  | Desired state of the resource.                                                                        |
| `user`              |      N/A      |    no    | str  | The name or id of the user to assign to the object.                                                   |
| `user_ansible_id`   |      N/A      |    no    | int  | Resource id of the user who will receive permissions from this assignment. Alternative to user field. |

### Standard Role User Assignment Data Structure

#### Json Example

```json
{
  "controller_role_user_assignments": [
    {
        "role_definition": "Inventory Admin",
        "object_id": 1,
        "user": "user"
    }
  ]
}
```

#### Yaml Example

File name: `configs/controller/controller_role_user_assignments.yml`

```yaml
---

controller_role_user_assignments:
  # This will apply the role 'Inventory Admin' to the user 'user123' on the inventory with the id of '1'
  - role_definition: Inventory Admin
    object_id: 1
    user: user123
  # This will apply the role 'Credential Use' to the user 'user456' on the credential with the id of '23'
  - role_definition: Credential Use
    object_id: 23
    user: user456
```

## License

[GPLv3+](https://github.com/redhat-cop/infra.aap_configuration/blob/devel/LICENSE)
