# Ansible Role infra.platform_configuration.service_nodes

## Description

An Ansible Role to configure Service Nodes on Ansible Automation gateway.

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md)

Variables specific for this role are following:

| Variable Name                                          |                    Default Value                    | Required | Description                                                                                                                                                         |                                                      |
|:-------------------------------------------------------|:---------------------------------------------------:|:--------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `service_nodes_list` (Alias: `service_nodes`)       |          [below](#service-node-arguments)           |   yes    | Data structure describing your service_node entries described below.                                                                                                |        [more](../../README.md#data-variables)        |
| `service_nodes_secure_logging`   |  `aap_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive service_node role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |   [more](../../README.md#secure-logging-variables)   |
| `service_nodes_enforce_defaults` | `aap_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the service node role.                                                                                      |      [more](../../README.md#enforcing-defaults)      |
| `service_nodes_async_retries`    |    `aap_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                                   | [more](../../README.md#asynchronous-retry-variables) |
| `service_nodes_async_delay`      |     `aap_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                                   | [more](../../README.md#asynchronous-retry-variables) |

## Data Structure

### Service Node Arguments

Options for the `service_nodes_list` variable:

| Variable Name     | Default Value | Required | Type | Description                                                                      |
|:------------------|:-------------:|:--------:|:----:|:---------------------------------------------------------------------------------|
| `name`            |      N/A      |   yes    | str  | The name of the resource                                                         |
| `new_name`        |      N/A      |    no    | str  | Setting this option will change the existing name (looked up via the name field) |
| `address`         |      N/A      |    no    | str  | Network address for this service                                                 |
| `service_cluster` |      N/A      |    no    | str  | ID or name referencing the [Service Cluster](../service_clusters/README.md)      |
| `tags`            |      N/A      |    no    | str  | Comma separated list of tags to assign to the node, for filtering route traffic  |
| `state`           |   `present`   |    no    | str  | [more](../../README.md#state-variable)                                           |

**Unique value:**

- `name`
- `address` + `service_cluster`

## Usage

### Json Example

- Check the node on 10.0.0.1 for EDA service exists (in the database):
- Check the node with ID 1 exists (in the database):

```json
{
  "service_nodes_list": [
    {
      "name": "EDA - 10.0.0.1",
      "state": "exists"
    },
    {
      "name": 1,
      "state": "exists"
    }
  ]
}
```

### Yaml Example

- Create node (if not exists) for Controller service (in the database)
- Delete node (if exists) for Automation Hub Service (from the database)

File name: `data/service_nodes.yml`

```yaml
---
service_nodes_list:
- name: "Controller Node 1"
  address: 10.0.0.1
  service_cluster: controller
- name: "Hub on 10.0.1.1"
  state: absent
```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_service_nodes.yml
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
