# Ansible Role infra.platform_configuration.role_user_assignments

## Description

An Ansible Role to give a user permission to a resource like an organization.

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md)

Variables specific for this role are following:

| Variable Name                                                    |                    Default Value                    | Required | Description                                                                                                                                                                  |                                                      |
|:-----------------------------------------------------------------|:---------------------------------------------------:|:--------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `role_user_assignments_list` (Alias: `role_user_assignments`) |      [below](#role-user-assignments-arguments)      |   yes    | Data structure describing your organization entries described below.                                                                                                         |        [more](../../README.md#data-variables)        |
| `role_user_assignments_secure_logging`     |  `platform_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive role_user_assignments role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |   [more](../../README.md#secure-logging-variables)   |
| `role_user_assignments_enforce_defaults`   | `platform_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the role_user_assignments role.                                                                                      |      [more](../../README.md#enforcing-defaults)      |
| `role_user_assignments_async_retries`      |    `platform_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                                            | [more](../../README.md#asynchronous-retry-variables) |
| `role_user_assignments_async_delay`        |     `platform_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                                            | [more](../../README.md#asynchronous-retry-variables) |

## Data Structure

### Role User Assignments Arguments

Options for the `role_user_assignments` variable:

| Variable Name       | Default Value | Required | Type | Description                                                                                           |
|:--------------------|:-------------:|:--------:|:----:|:------------------------------------------------------------------------------------------------------|
| `role_definition`   |      N/A      |   yes    | str  | The name or id of the role definition to assign to the user.                                          |
| `user`              |      N/A      |    no    | str  | The username or id of the user to assign to the object.                                               |
| `user_ansible_id`   |      N/A      |    no    | str  | Resource id of the user who will receive permissions from this assignment. Alternative to user field. |
| `object_id`         |      N/A      |    no    | int  | Primary key of the object this assignment applies to.                                                 |
| `object_ansible_id` |      N/A      |    no    | str  | Resource id of the object this role applies to. Alternative to the object_id field.                   |
| `state`             |   `present`   |    no    | str  | Desired state of the resource.                                                                        |

** Unique value: **

- [`user`, `object_id`] (`*_ansible_id` alternatives can be provided)

## Usage

### Json Example

- Assign Organization Member role (object_id is an organization with ID 1)

```json
{
  "role_user_assignments_list": [
    {
      "role_definition": "Organization Member",
      "user": "Bob",
      "object_id": "1",
    }
  ]
}
```

### Yaml Example

- Assign Team Admin role (object_id is a team with ID 10)

File name: `data/gateway_role_user_assignments.yml`

```yaml
---
role_user_assignments_list:
- role_definition: Team Admin
  user: 1
  object_id: 10
```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_role_user_assignments.yml
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
