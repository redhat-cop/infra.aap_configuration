# Ansible Role ansible.gateway_configuration.authenticators

## Description

An Ansible Role to add Authenticators on Ansible Automation gateway.

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md)

Variables specific for this role are following:

| Variable Name                                           |                    Default Value                    | Required | Description                                                                                                                                                          |                                                      |
|:--------------------------------------------------------|:---------------------------------------------------:|:--------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `gateway_authenticators` (Alias: `authenticators`)      |          [below](#authenticator-arguments)          |   yes    | Data structure describing your organization entries described below.                                                                                                 |        [more](../../README.md#data-variables)        |
| `gateway_configuration_authenticators_secure_logging`   |  `gateway_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive organizations role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |   [more](../../README.md#secure-logging-variables)   |
| `gateway_configuration_authenticators_enforce_defaults` | `gateway_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the organizations role.                                                                                      |      [more](../../README.md#enforcing-defaults)      |
| `gateway_configuration_authenticators_async_retries`    |    `gateway_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                                    | [more](../../README.md#asynchronous-retry-variables) |
| `gateway_configuration_authenticators_async_delay`      |     `gateway_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                                    | [more](../../README.md#asynchronous-retry-variables) |

## Data Structure

### Authenticator Arguments

Options for the `gateway_authenticators` variable:

| Variable Name    |    Default Value    | Required | Type | Description                                                                                                                  |
|:-----------------|:-------------------:|:--------:|:----:|:-----------------------------------------------------------------------------------------------------------------------------|
| `name`           |         N/A         |   yes    | str  | The name of the resource                                                                                                     |
| `new_name`       |         N/A         |    no    | str  | Setting this option will change the existing name (looked up via the name field)                                             |
| `slug`           |         N/A         |    no    | str  | An immutable identifier for the authenticator                                                                                |
| `enabled`        | N/A(`false` by API) |    no    | bool | Enable/Disable the authenticator                                                                                             |
| `create_objects` | N/A(`true` by API)  |    no    | bool | Allow authenticator to create objects (users, teams, organizations)                                                          |
| `remove_users`   | N/A(`true` by API)  |    no    | bool | When a user authenticates from this source should they be removed from any other groups they were previously added to        |
| `configuration`  |         N/A         |    no    | dict | The required configuration for this source (dict keys specified by the module in 'type')                                     |
| `type`           |         N/A         |    no    | str  | The type of authentication service this is. Can be one of the modules: `ansible_base.authentication.authenticator_plugins.*` |
| `order`          |  N/A (`1` by API)   |    no    | int  | The order in which an authenticator will be tried. This only pertains to username/password authenticators                    |
| `state`          |      `present`      |    no    | str  | Desired state of the resource.                                                                                               |

** Unique value: **

- `name`
- `slug` (can't be used as an identificator)

## Usage

### Json Example

- Creates local authenticator
- Renames authenticator

```json
{
  "gateway_authenticators": [
    {
      "name": "local authenticator",
      "slug": "local-authenticator",
      "type": "ansible_base.authentication.authenticator_plugins.local",
      "enabled": true,
      "configuration": {}
    },
    {
      "name": "github authenticator",
      "new_name": "New GitHub Authenticator"
    }
  ]
}
```

### Yaml Example

- Deletes 1 authenticator
- Creates an AzureAD authenticator with configuration provided by the `ansible_base.authentication.authenticator_plugins.azuread` module
  - configuration class can be found in https://github.com/ansible/django-ansible-base/tree/devel/ansible_base/authentication/authenticator_plugins 

File name: `data/gateway_authenticators.yml`

```yaml
---
gateway_authenticators:
- name: "Deprecated Authenticator"
  state: absent
- name: Auth AzureAD
  type: 'ansible_base.authentication.authenticator_plugins.azuread'
  slug: authenticator-azuread
  enabled: true
  configuration:
    CALLBACK_URL: 'https://127.0.0.1'
    KEY: 'oidc-key'
    SECRET: 'oidc-secret'
```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_authenticators.yml
```

## License

[GPLv3](https://github.com/ansible/aap-gateway/gateway_configuration_collection/COPYING)
