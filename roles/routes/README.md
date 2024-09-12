# Ansible Role ansible.gateway_configuration.routes

## Description

An Ansible Role to configure gateway non-API Routes to services (controller, hub,...) on Ansible Automation gateway.
They define http port and path (**not** starting with prefix /api/) used in gateway and
http port and path in the destination service (gateway, controller, hub, eda).

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md)

Variables specific for this role are following:

| Variable Name                                   |                    Default Value                    | Required | Description                                                                                                                                                  |                                                      |
|:------------------------------------------------|:---------------------------------------------------:|:--------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `gateway_routes` (Alias: routes)                |             [below](#service-arguments)             |   yes    | Data structure describing your route entries described below.                                                                                                |        [more](../../README.md#data-variables)        |
| `gateway_configuration_routes_secure_logging`   |  `gateway_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive route role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |   [more](../../README.md#secure-logging-variables)   |
| `gateway_configuration_routes_enforce_defaults` | `gateway_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the route role.                                                                                      |      [more](../../README.md#enforcing-defaults)      |
| `gateway_configuration_routes_async_retries`    |    `gateway_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                            | [more](../../README.md#asynchronous-retry-variables) |
| `gateway_configuration_routes_async_delay`      |     `gateway_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                            | [more](../../README.md#asynchronous-retry-variables) |

## Data Structure

### Service Arguments

Options for the `gateway_routes` variable:

| Variable Name         |    Default Value    | Required | Type | Description                                                                         |
|:----------------------|:-------------------:|:--------:|:----:|:------------------------------------------------------------------------------------|
| `name`                |         N/A         |   yes    | str  | The name of the route                                                               |
| `new_name`            |         N/A         |    no    | str  | Setting this option will change the existing name (looked up via the name field)    |
| `description`         |         ""          |    no    | str  | Description of the route                                                            |
| `gateway_path`        |         N/A         |    no    | str  | Path on the AAP gateway to listen to traffic on                                     |
| `http_port`           |         N/A         |    no    | str  | ID or name referencing the [Http Port](../http_ports/README.md)                     |
| `service_cluster`     |         N/A         |    no    | str  | ID or name referencing the [Service Cluster](../service_clusters/README.md)         |
| `is_service_https`    |       `false`       |    no    | bool | Flag whether or not the service cluster uses https                                  |
| `enable_gateway_auth` | N/A (`true` by API) |    no    | bool | If false, the AAP gateway will not insert a gateway token into the proxied request  |
| `service_path`        |         N/A         |    no    | str  | URL path on the AAP Service cluster to route traffic to                             |
| `service_port`        |         N/A         |    no    | int  | Port on the service cluster to route traffic to                                     |
| `tags`                |         ""          |    no    | str  | Comma-separated string, selects which (tagged) nodes receive traffic from this route|
| `state`               |      `present`      |    no    | str  | [more](../../README.md#state-variable)                                              |

**Unique value:**

- `name`
- `http_port` + `gateway_path`

**Note**: `gateway_path` can't start with `/api/` prefix

## Usage

#### Json Example

- Check that Controller's config route exists
- Update gateway route to the port 8000 and path '/non-api/v2'
- Create or update EDA Route to gateway proxy port (http port) with id 1 and Service Cluster with id 2 (in the database)

```json
{
  "gateway_services": [
    {
      "name": "Controller Config Route",
      "state": "exists"
    },
    {
      "name": "Gateway Non-api Route",
      "http_port": "Port 8000",
      "gateway_path": "/non-api/v2",
      "enable_gateway_auth": false
    },
    {
      "name": "EDA Config Route",
      "service_cluster": 2,
      "http_port": 1,
      "gateway_path": "/config/eda/",
      "service_path": "/config/v1/",
      "service_port": 9000
    }
  ]
}
```

### Yaml Example

- Checks that non-api routes to services exist
- If at least one doesn't exist, playbook fails.

File name: `data/gateway_routes.yml`

```yaml
---
gateway_state: exists
gateway_routes:
- name: "Controller Config route"
  gateway_path: '/config/controller/'
  http_port: Port 8000
- name: "Hub Config route"
- name: 3
- name: 4
```

## Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_routes.yml
```

## License

[GPLv3](https://github.com/ansible/aap-gateway/gateway_configuration_collection/COPYING)
