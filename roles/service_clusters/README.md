# Ansible Role ansible.gateway_configuration.service_clusters

## Description

An Ansible Role to configure Service Clusters on Ansible Automation gateway.

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md)

Variables specific for this role are following:

| Variable Name                                             |                    Default Value                    | Required | Description                                                                                                                                                            |                                                      |
|:----------------------------------------------------------|:---------------------------------------------------:|:--------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `gateway_service_clusters` (Alias: service_clusters)      |         [below](#service-cluster-arguments)         |   yes    | Data structure describing your service_cluster entries described below.                                                                                                |        [more](../../README.md#data-variables)        |
| `gateway_configuration_service_clusters_secure_logging`   |  `gateway_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive service_cluster role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |   [more](../../README.md#secure-logging-variables)   |
| `gateway_configuration_service_clusters_enforce_defaults` | `gateway_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the service cluster role.                                                                                      |      [more](../../README.md#enforcing-defaults)      |
| `gateway_configuration_service_clusters_async_retries`    |    `gateway_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                                      | [more](../../README.md#asynchronous-retry-variables) |
| `gateway_configuration_service_clusters_async_delay`      |     `gateway_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                                      | [more](../../README.md#asynchronous-retry-variables) |

## Data Structure

### Service Cluster Arguments

Options for the `gateway_service_clusters` variable:

| Variable Name  | Default Value |      Required      | Type | Description                                                                             |
|:---------------|:-------------:|:------------------:|:----:|:----------------------------------------------------------------------------------------|
| `name`         |      N/A      |        yes         | str  | The name of the resource                                                                |
| `new_name`     |      N/A      |         no         | str  | Setting this option will change the existing name (looked up via the name field)        |
| `service_type` |      N/A      | state is 'present' | str  | The type of service for this cluster. Choices : ["hub", "controller", "eda", "gateway"] |
| `state`        |   `present`   |         no         | str  | [more](../../README.md#state-variable)                                                  | 

**Unique value:**

- `name`
- `service_type`

## Usage

#### Json Example

- Check that Controller and EDA (Event Driven Automation) services are deleted (if present) (from the database):
- Check that gateway service exists (in the database)

```json
{
  "gateway_state": "absent",
  "gateway_service_clusters": [
    {
      "name": "Automation Controller"
    },
    {
      "name": "Event Driven Automation"
    },
    {
      "name": "AAP gateway",
      "state": "exists"
    }
  ]
}
```

### Yaml Example

- Create or update Controller Service (in the database)
- CHeck that Service with ID 3 exists
- Renames Hub service

File name: `data/gateway_service_clusters.yml`

```yaml
---
gateway_service_clusters:
- name: "Automation Controller"
  service_type: controller
  state: present
- name: 3
  state: exists
- name: "Automation Hub"
  new_name: "Ansible Galaxy"
  ```

## Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_service_clusters.yml
```

## License

[GPLv3](https://github.com/ansible/aap-gateway/gateway_configuration_collection/COPYING)
