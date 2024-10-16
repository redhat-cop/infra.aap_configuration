# Ansible Role infra.platform_configuration.organizations

## Description

An Ansible Role to add Organizations on Ansible Automation gateway.

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md)

Variables specific for this role are following:

| Variable Name                                          |                    Default Value                    | Required | Description                                                                                                                                                          |                                                      |
|:-------------------------------------------------------|:---------------------------------------------------:|:--------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------:|
| `organizations_list` (Alias: `organizations`)       |          [below](#organization-arguments)           |   yes    | Data structure describing your organization entries described below.                                                                                                 |                |
| `organizations_secure_logging`   |  `aap_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive organizations role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |      |
| `organizations_enforce_defaults` | `aap_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the organizations role.                                                                                      |      README.md#enforcing-defaults)      |
| `organizations_async_retries`    |    `aap_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                                    |  |
| `organizations_async_delay`      |     `aap_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                                    |  |

## Data Structure

### Organization Arguments

Options for the `gateway_organizations` variable:

| Variable Name | Default Value | Required | Type | Description                                                                      |
|:--------------|:-------------:|:--------:|:----:|:---------------------------------------------------------------------------------|
| `name`        |      N/A      |   yes    | str  | The name of the resource                                                         |
| `new_name`    |      N/A      |    no    | str  | Setting this option will change the existing name (looked up via the name field) |
| `description` |      N/A      |    no    | str  | Description of the organization                                                  |
| `state`       |   `present`   |    no    | str  | Desired state of the resource.                                                   |

### Unique value

- `name`

## Usage

### Json Example

- Create 2 Organizations

```json
{
  "organizations_list": [
    {
      "name": "Org 1",
      "description": "First Organization"
    },
    {
      "name": "Org 2"
    }
  ]
}
```

### Yaml Example

- Check that "Deprecated Org" doesn't exist
- Check that Org 1 exists
- Get or create Org 2
- Rename Org 3

File name: `data/gateway_organizations.yml`

```yaml
---
organizations_list:
- name: "Deprecated Org"
  state: absent
- name: Org 1
  state: exists
- name: Org 2
- name: Org 3
  new_name: Organization 3
```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_organizations.yml
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
