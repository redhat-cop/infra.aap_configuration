# Ansible Role infra.platform_configuration.authenticator_maps

## Description

An Ansible Role to add Authenticator Maps on Ansible Automation gateway.

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md)

Variables specific for this role are following:

| Variable Name                                               |                    Default Value                    | Required | Description                                                                                                                                                              |                                                      |
|:------------------------------------------------------------|:---------------------------------------------------:|:--------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `authenticator_maps_list` (Alias: `authenticator_maps`)  |          [below](#Authenticator Map Arguments)           |   yes    | Data structure describing your authenticator_map entries described below.                                                                                                |                |
| `gateway_authenticator_maps_secure_logging`   |  `aap_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive authenticator_map role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |      |
| `authenticator_maps_enforce_defaults` | `aap_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the authenticator_map role.                                                                                      |      README.md#enforcing-defaults)      |
| `gateway_authenticator_maps_async_retries`    |    `aap_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                                        |  |
| `gateway_authenticator_maps_async_delay`      |     `aap_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                                        |  |

## Data Structure

### Authenticator Map Arguments

Options for the `authenticator_maps_list` variable:

| Variable Name       |  Default Value  | Required | Type | Description                                                                                                                                 |
|:--------------------|:---------------:|:--------:|:----:|:--------------------------------------------------------------------------------------------------------------------------------------------|
| `name`              |       N/A       |   yes    | str  | The name of the resource                                                                                                                    |
| `new_name`          |       N/A       |    no    | str  | Setting this option will change the existing name (looked up via the name field)                                                            |
| `authenticator`     |       N/A       |   yes    | str  | The name or ID referencing the [Authenticator](../gateway_authenticators/README.md)                                                                 |
| `new_authenticator` |       N/A       |    no    | str  | The name or ID referencing newly associated authenticator                                                                                   |
| `revoke`            |     `false`     |    no    | bool | If a user does not meet this rule should we revoke the permission                                                                           |
| `map_type`          |     `team`      |    no    | str  | What does the map work on, a team, a user flag or is this an allow rule. choices: ["allow", "is_superuser", "team", "organization", "role"] |
| `role`              |       N/A       |    no    | str  | The name of RBAC Role Definition  to be used for this map                                                                                   |
| `team`              |       N/A       |    no    | str  | A team name this rule works on                                                                                                              |
| `organization`      |       N/A       |    no    | str  | An organization name this rule works on                                                                                                     |
| `triggers`          |      `{}`       |    no    | dict | Trigger information for this rule                                                                                                           |
| `order`             | N/A(`0` by API) |    no    | int  | The order in which this rule should be processed, smaller numbers are of higher precedence                                                  |
| `state`             |    `present`    |    no    | str  | Desired state of the resource.                                                                                                              |

### Unique value

- [`name`, `authenticator`]

## Usage

### Json Example

- Creates 1 authenticator map with map_type == 'organization' => requires value for "organization"
- Creates 1 authenticator map with map_type == 'team' => requires values for "team" and "organization"

```json
{
  "authenticator_maps_list": [
    {
      "name": "AMap-1",
      "authenticator": "Authenticator-1",
      "revoke": false,
      "map_type": "organization",
      "organization": "Organization 1",
      "triggers": {
        "always": {},
        "never": {}
      },
      "order": 10
    },
    {
      "name": "AMap-2",
      "authenticator": "Authenticator-2",
      "map_type": "team",
      "team": "Team 1",
      "organization": "Organization 1",
      "role": "Team Member",
      "triggers": {
        "never": {}
      }
    }
  ]
}
```

### Yaml Example

- Creates Authenticator Map with examples of triggers structure
- Renames Authenticator Map and changes Authenticator

```yaml
---
authenticator_maps_list:
- name: AuthMap 1
  authenticator: Auth 1
  revoke: true
  map_type: organization
  organization: Organization 1
  role: Organization Admin
  triggers:
    always: { }
    never: { }
    groups:
      has_or:
      - has_or_11
      - has_or_22
      has_and:
      - has_and_1
      - has_and_22
    attributes:
      join_condition: "or"
      attr_1:
        contains: aaa
        matches: "bbb"
        ends_with: "ccc"
      attr_2:
        in:
        - abc1
        - abc2
        - abc3
- name: "AuthMapX"
  new_name: "Authenticator Map X"
  authenticator: "Auth"
  new_authenticator: "Auth 2"
```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_authenticator_maps.yml
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
