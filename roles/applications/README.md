# Ansible Role ansible.gateway_configuration.applications

## Description

An Ansible Role to create/update/remove Applications on Ansible gateway.

## Variables

Detailed description of variables are provided in the [top-level README](../../README.md)

Variables specific for this role are following:

| Variable Name                                         |                    Default Value                    | Required | Description                                                                                                                                                        |                                        |
|:------------------------------------------------------|:---------------------------------------------------:|:--------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------:|
| `gateway_applications` (Alias: `applications`)        |           [below](#application-arguments)           |   yes    | Data structure describing your applications entries described below. Alias: applications                                                                           | [more](../../README.md#data-variables) |
| `gateway_configuration_applications_secure_logging`   |  `gateway_configuration_secure_logging` OR `false`  |    no    | Whether or not to include the sensitive Application role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere. |
| `gateway_configuration_applications_enforce_defaults` | `gateway_configuration_enforce_defaults` OR `false` |    no    | Whether or not to enforce default option values on only the applications role                                                                                      |
| `gateway_configuration_applications_async_retries`    |    `gateway_configuration_async_retries` OR `30`    |    no    | This variable sets the number of retries to attempt for the role.                                                                                                  |
| `gateway_configuration_applications_async_delay`      |     `gateway_configuration_async_delay` OR `1`      |    no    | This sets the delay between retries for the role.                                                                                                                  |

## Data Structure

### Application Arguments

Options for the `gateway_applications` variable:

| Variable Name               |    Default Value    | Required | Type | Description                                                                            |
|:----------------------------|:-------------------:|:--------:|:----:|:---------------------------------------------------------------------------------------|
| `name`                      |         N/A         |   yes    | str  | Name of application                                                                    |
| `new_name`                  |         N/A         |    no    | str  | Setting this option will change the existing name (looked up via the name field).      |
| `organization`              |         N/A         |   yes    | str  | Name of the organization for the application                                           |
| `new_organization`          |         N/A         |    no    | str  | The name or ID referencing newly associated organization                               |
| `algorithm`                 |         N/A         |    no    | str  | The OIDC token signing algorithm for this application. Choices: ["", "RS256", "HS256"] |
| `description`               |         N/A         |    no    | str  | Description to use for the application.                                                |
| `authorization_grant_type`  |         N/A         |   yes    | str  | Grant type for tokens in this application, Choices: ["password", "authorization-code"] |
| `client_type`               |         N/A         |   yes    | str  | Application client type. Choices: ["confidential", "public"]                           |
| `redirect_uris`             |         ""          |    no    | str  | Allowed urls list, space separated. Required with "authorization-code" grant type      |
| `skip_authorization`        | N/A(`false` by API) |   yes    | bool | Set True to skip authorization step for completely trusted applications.               |
| `post_logout_redirect_uris` |         ""          |    no    | str  | Allowed Post Logout URIs list, space separated.                                        |
| `user`                      |         ""          |    no    | str  | The user who owns this application.                                                    |
| `state`                     |      `present`      |    no    | str  | Desired state of the application.                                                      |

### Standard Application Data Structure

#### Json Example

```json
 {
  "gateway_applications": [
    {
      "name": "gateway Config Default Application",
      "description": "Generic application, which can be used for oauth tokens",
      "organization": "Default",
      "state": "present",
      "client_type": "confidential",
      "authorization_grant_type": "password"
    }
  ]
}
```

#### Yaml Example

File name: `data/gateway_applications.yml`

```yaml
---
gateway_applications:
- name: "gateway Config Default Application"
  description: "Generic application, which can be used for oauth tokens"
  organization: "Default"
  state: "present"
  client_type: "confidential"
  authorization_grant_type: "password"
```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_applications.yml
```

## License

[GPLv3](https://github.com/ansible/aap-gateway/gateway_configuration_collection/COPYING)
