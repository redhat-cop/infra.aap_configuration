# Ansible Role infra.platform_configuration.users

## Description

An Ansible Role to configure users on Ansible Automation gateway.

## Variables

| Variable Name                                     |                    Default Value                    | Required | Description                                                                                                                                                 |                                                      |
|:--------------------------------------------------|:---------------------------------------------------:|:--------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `users_list` (Alias: `users`)  |              [below](#user-arguments)               |   yes    | Data structure describing your user entries described below.                                                                                                |                |
| `users_secure_logging`      |  `aap_configuration_secure_logging` OR `true`   |    no    | Whether or not to include the sensitive user role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |      |
| `users_enforce_defaults`    | `aap_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the user role.                                                                                      |      README.md#enforcing-defaults)      |
| `users_async_retries`       |    `aap_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                           |  |
| `users_async_delay`         |     `aap_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                           |  |
| `users_default_password`                   |                         ""                          |    no    | Global variable to set the password for all users.                                                                                                          |                                                      |

**Note**: Secure Logging defaults to True if both variables are not set

## Data Structure

### User Arguments

Options for the `gateway_users` variable:

| Variable Name       |             Default Value             | Required | Type | Description                                                                                                                                                           |
|:--------------------|:-------------------------------------:|:--------:|:----:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `username`          |                  N/A                  |   yes    | str  | The username of the user                                                                                                                                              |
| `password`          | "{{ users_default_password }}" |    no    | str  | The password of the user                                                                                                                                              |
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
  "users_default_password": "changeme",
  "users_list": [
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
users_list:
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

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
