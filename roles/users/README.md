# Ansible Role ansible.gateway_configuration.users

## Description

An Ansible Role to configure users on Ansible Automation gateway.

## Variables

| Variable Name                                     |                    Default Value                    | Required | Description                                                                                                                                                 |                                                      |
|:--------------------------------------------------|:---------------------------------------------------:|:--------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `gateway_users` (Alias: `gateway_user_accounts`)  |              [below](#user-arguments)               |   yes    | Data structure describing your user entries described below.                                                                                                |        [more](../../README.md#data-variables)        |
| `gateway_configuration_users_secure_logging`      |  `gateway_configuration_secure_logging` OR `true`   |    no    | Whether or not to include the sensitive user role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |   [more](../../README.md#secure-logging-variables)   |
| `gateway_configuration_users_enforce_defaults`    | `gateway_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the user role.                                                                                      |      [more](../../README.md#enforcing-defaults)      |
| `gateway_configuration_users_async_retries`       |    `gateway_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                           | [more](../../README.md#asynchronous-retry-variables) |
| `gateway_configuration_users_async_delay`         |     `gateway_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                           | [more](../../README.md#asynchronous-retry-variables) |
| `gateway_user_default_password`                   |                         ""                          |    no    | Global variable to set the password for all users.                                                                                                          |                                                      |

**Note**: Secure Logging defaults to True if both variables are not set

## Data Structure

### User Arguments

Options for the `gateway_users` variable:

| Variable Name       |             Default Value             | Required | Type | Description                                                                                                                                                           |
|:--------------------|:-------------------------------------:|:--------:|:----:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `username`          |                  N/A                  |   yes    | str  | The username of the user                                                                                                                                              |
| `password`          | "{{ gateway_user_default_password }}" |    no    | str  | The password of the user                                                                                                                                              |
| `email`             |                  N/A                  |   yes    | str  | The email of the user                                                                                                                                                 |
| `first_name`        |                  ""                   |    no    | str  | The first name of the user                                                                                                                                            |
| `last_name`         |                  ""                   |    no    | str  | The last name of the user                                                                                                                                             |
| `is_superuser`      |                `false`                |    no    | bool | Whether the user is a superuser                                                                                                                                       |
| `authenticators`    |                 N/A                   |    no    | list | List of authenticators this user is associated with                                                                                                                   |
| `authenticator_uid` |                 N/A                   |    no    | bool | UID coming from the authenticators the user is associated with                                                                                                        |
| `state`             |               `present`               |    no    | str  | Desired state of the resource.                                                                                                                                        |
| `update_secrets`    |                'true'                 |    no    | bool | True will always change password if user specifies password, even if API gives $encrypted$ for password. False will only set the password if other values change too. |

**Unique value:**

- `username`

## Usage

### Json Example

- Creates (or updates) 2 users, one with default password "changeme".

```json
{
  "gateway_user_default_password": "changeme",
  "gateway_users": [
    {
      "username": "jsmith",
      "is_superuser": false,
      "password": "p4ssword",
      "email": "jsmith@example.com"
    },
    {
      "username": "jdoe",
      "email": "jdoe@example.com"
    }
  ]
}
```

#### Yaml Example

- Check that users exist

File name: `data/gateway_users.yml`

```yaml
---
gateway_state: exists
gateway_users:
- username: jsmith
- username: jdoe
- username: admin
```

## Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_users.yml
```

## License

[GPLv3](https://github.com/ansible/aap-gateway/gateway_configuration_collection/COPYING)
