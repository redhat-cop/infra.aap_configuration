# Ansible Role infra.platform_configuration.settings

An Ansible role to alter Settings on Ansible Automation gateway settings.

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md).  
Settings doesn't implement the `gateway_configuration_enforce_defaults` because it's not applicable.

Variables specific for this role are following:

| Variable Name                                   |                   Default Value                    | Required | Description                                                                                                                                                     |                                                      |
|:------------------------------------------------|:--------------------------------------------------:|:--------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `settings_list` (Alias: `settings`)          |            [below](#settings-arguments)            |   yes    | Data structure describing your setting entries described below.                                                                                                 |        [more](../../README.md#data-variables)        |
| `settings_secure_logging` | `gateway_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive settings role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |   [more](../../README.md#secure-logging-variables)   |
| `settings_async_retries`  |   `gateway_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                               | [more](../../README.md#asynchronous-retry-variables) |
| `settings_async_delay`    |     `gateway_configuration_async_delay` OR `1`     |    no    | This sets the delay between retries for the role.                                                                                                               | [more](../../README.md#asynchronous-retry-variables) |

**Note**: Secure Logging defaults to `True` if both variables are not set

## Data Structure

### Settings arguments

Provide settings as a single dict under `settings_list`.

## Usage

#### Json Example

```json
{
  "settings_list": {
    "gateway_token_name": "X-DAB-JW-TOKEN",
    "gateway_access_token_expiration": 600,
    "gateway_basic_auth_enabled": true,
    "gateway_proxy_url": "https://localhost:9080",
    "gateway_proxy_url_ignore_cert": false,
    "password_min_length": 0,
    "password_min_digits": 0,
    "password_min_upper": 0,
    "password_min_special": 0,
    "allow_admins_to_set_insecure": false
  }
}

```

#### Yaml Example

File name: `data/gateway_settings.yml`

```yaml
---
settings_list:
  gateway_token_name: X-DAB-JW-TOKEN
  gateway_access_token_expiration: 600
  gateway_basic_auth_enabled: true
  gateway_proxy_url: https://localhost:9080
  gateway_proxy_url_ignore_cert: false
  password_min_length: 0
  password_min_digits: 0
  password_min_upper: 0
  password_min_special: 0
  allow_admins_to_set_insecure: false


```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_settings.yml
```

## License

[GPLv3](https://github.com/ansible/aap-gateway/gateway_configuration_collection/COPYING)
