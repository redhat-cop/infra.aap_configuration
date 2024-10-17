# Ansible Role infra.platform_configuration.http_ports

## Description

An Ansible Role to add proxy Http Ports on Ansible Automation gateway.

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md)

Variables specific for this role are following:

| Variable Name                                       |                    Default Value                    | Required | Description                                                                                                                                                       |                                                      |
|:----------------------------------------------------|:---------------------------------------------------:|:--------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `http_ports_list` (Alias: `http_ports`)          |            [below](#http-port-arguments)            |   yes    | Data structure describing your http port entries described below.                                                                                                 |                |
| `http_ports_secure_logging`   |  `aap_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive http_ports role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |      |
| `http_ports_enforce_defaults` | `aap_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the http port role.                                                                                       |      README.md#enforcing-defaults)      |
| `http_ports_async_retries`    |    `aap_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                                 |  |
| `http_ports_async_delay`      |     `aap_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                                 |  |

## Data Structure

### Http Port Arguments

Options for the `http_ports_list` variable:

| Variable Name | Default Value | Required | Type | Description                                                                      |
|:--------------|:-------------:|:--------:|:----:|:---------------------------------------------------------------------------------|
| `name`        |      N/A      |   yes    | str  | The name of the resource                                                         |
| `new_name`    |      N/A      |    no    | str  | Setting this option will change the existing name (looked up via the name field) |
| `number`      |      N/A      |    no    | int  | Port number, must be unique                                                      |
| `use_https`   |    `false`    |    no    | bool | Secure this port with HTTPS                                                      |
| `is_api_port` |    `false`    |    no    | bool | If true, port is used for serving remote AAP APIs. Only one can be set to True   |
| `state`       |   `present`   |    no    | str  | Desired state of the resource.                                                   |

**Unique value:**

- `name`
- `number`

## Usage

### Json Example

- Create or update the proxy http port 443, renames it to "Proxy API Port"

```json
{
  "http_ports_list": [
    {
      "name": "API port",
      "new_name": "Proxy API port",
      "number": 443,
      "is_api_port": true,
      "use_https": true
    }
  ]
}
```

### Yaml Example

- Delete port (if exists) 8001
- Create port (if not exists) 8002
- Create or update port 8003

File name: `data/gateway_http_ports.yml`

```yaml
---
http_ports_list:
- name: "Service Port 8001"
  number: 8001
  state: absent
- name: "Reserved port"
  number: 8002
- name: "Backup port"
  number: 8003
  use_https: true
```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_http_ports.yml
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
