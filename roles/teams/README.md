# Ansible Role ansible.gateway_configuration.teams

## Description

An Ansible Role to add Teams on Ansible Automation gateway.

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md)

Variables specific for this role are following:

| Variable Name                                  |                    Default Value                    | Required | Description                                                                                                                                                 |                                                      |
|:-----------------------------------------------|:---------------------------------------------------:|:--------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `gateway_teams` (Alias: `teams`)               |          [below](#organization-arguments)           |   yes    | Data structure describing your team entries described below.                                                                                                |        [more](../../README.md#data-variables)        |
| `gateway_configuration_teams_secure_logging`   |  `gateway_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive team role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |   [more](../../README.md#secure-logging-variables)   |
| `gateway_configuration_teams_enforce_defaults` | `gateway_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the team role.                                                                                      |      [more](../../README.md#enforcing-defaults)      |
| `gateway_configuration_teams_async_retries`    |    `gateway_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                           | [more](../../README.md#asynchronous-retry-variables) |
| `gateway_configuration_teams_async_delay`      |     `gateway_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                           | [more](../../README.md#asynchronous-retry-variables) |

## Data Structure

### Team Arguments

Options for the `gateway_teams` variable:

| Variable Name      | Default Value | Required | Type | Description                                                                       |
|:-------------------|:-------------:|:--------:|:----:|:----------------------------------------------------------------------------------|
| `name`             |      N/A      |   yes    | str  | The name of the resource                                                          |
| `new_name`         |      N/A      |    no    | str  | Setting this option will change the existing name (looked up via the name field)  |
| `description`      |      N/A      |    no    | str  | Description of the organization                                                   |
| `organization`     |      N/A      |   yes    | str  | The name or ID referencing the [Organization](../organizations/README.md)         |
| `new_organization` |      N/A      |    no    | str  | The name or ID referencing newly associated organization                          |
| `state`            |   `present`   |    no    | str  | Desired state of the resource.                                                    |

** Unique value: **

- [`name`, `organization`]

## Usage

### Json Example

- Create 2 Teams

```json
{
  "gateway_teams": [
    {
      "name": "Team 1",
      "description": "Best team",
      "organization": "IT Department"
    },
    {
      "name": "Team 2",
      "organization": "1"
    }
  ]
}
```

### Yaml Example

- Check that Happy Team in Productive Organization exists
- Check that Managers Team doesn't exist, or delete it
- Rename Team X and Reassign it to another organization

File name: `data/gateway_teams.yml`

```yaml
---
gateway_teams:
- name: "Happy Team"
  organization: "Productive Organization"
  state: exists
- name: "Managers"
  organization: "Org X"
  state: absent
- name: "Team X"
  new_name: "Secret Team"
  organization: "Org X"
  new_organization: "Secret Organization"
```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_teams.yml
```

## License

[GPLv3](https://github.com/ansible/aap-gateway/gateway_configuration_collection/COPYING)
