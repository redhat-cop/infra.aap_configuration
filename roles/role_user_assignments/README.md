# Ansible Role ansible.gateway_configuration.role_user_assignments

## Description

An Ansible Role to give a user permission to a resource like an organization.

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md)

Variables specific for this role are following:

| Variable Name                                                    |                    Default Value                    | Required | Description                                                                                                                                                                  |                                                      |
|:-----------------------------------------------------------------|:---------------------------------------------------:|:--------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `gateway_role_user_assignments` (Alias: `role_user_assignments`) |      [below](#role-user-assignments-arguments)      |   yes    | Data structure describing your organization entries described below.                                                                                                         |        [more](../../README.md#data-variables)        |
| `gateway_configuration_role_user_assignments_secure_logging`     |  `gateway_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive role_user_assignments role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |   [more](../../README.md#secure-logging-variables)   |
| `gateway_configuration_role_user_assignments_enforce_defaults`   | `gateway_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the role_user_assignments role.                                                                                      |      [more](../../README.md#enforcing-defaults)      |
| `gateway_configuration_role_user_assignments_async_retries`      |    `gateway_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                                            | [more](../../README.md#asynchronous-retry-variables) |
| `gateway_configuration_role_user_assignments_async_delay`        |     `gateway_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                                            | [more](../../README.md#asynchronous-retry-variables) |

## Data Structure

### Role User Assignments Arguments

Options for the `gateway_role_user_assignments` variable:

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
  "gateway_role_user_assignments": [
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
gateway_role_user_assignments:
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

[GPLv3](https://github.com/ansible/aap-gateway/gateway_configuration_collection/COPYING)
