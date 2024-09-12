# Ansible Role ansible.gateway_configuration.service_nodes

## Description

An Ansible Role to configure Service Nodes on Ansible Automation gateway.

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md)

Variables specific for this role are following:

| Variable Name                                          |                    Default Value                    | Required | Description                                                                                                                                                         |                                                      |
|:-------------------------------------------------------|:---------------------------------------------------:|:--------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `gateway_service_nodes` (Alias: `service_nodes`)       |          [below](#service-node-arguments)           |   yes    | Data structure describing your service_node entries described below.                                                                                                |        [more](../../README.md#data-variables)        |
| `gateway_configuration_service_nodes_secure_logging`   |  `gateway_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive service_node role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |   [more](../../README.md#secure-logging-variables)   |
| `gateway_configuration_service_nodes_enforce_defaults` | `gateway_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the service node role.                                                                                      |      [more](../../README.md#enforcing-defaults)      |
| `gateway_configuration_service_nodes_async_retries`    |    `gateway_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                                   | [more](../../README.md#asynchronous-retry-variables) |
| `gateway_configuration_service_nodes_async_delay`      |     `gateway_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                                   | [more](../../README.md#asynchronous-retry-variables) |

## Data Structure

### Service Node Arguments

Options for the `gateway_service_nodes` variable:

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
  "gateway_service_nodes": [
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

File name: `data/gateway_service_nodes.yml`

```yaml
---
gateway_service_nodes:
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

[GPLv3](https://github.com/ansible/aap-gateway/gateway_configuration_collection/COPYING)
