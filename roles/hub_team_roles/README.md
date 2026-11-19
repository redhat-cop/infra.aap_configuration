# infra.aap_configuration.hub_team_roles

## Description

An Ansible Role to assign roles to teams in Automation Hub.

The teams and roles must already exist. Requires private automation hub version 4.11 or later.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`aap_hostname`|""|yes|URL to the Ansible Automation Platform Server.|127.0.0.1|
|`aap_username`|""|no|Admin User on the Ansible Automation Platform Server. Either username / password or token need to be specified.||
|`aap_password`|""|no|Platform Admin User's password on the Server.  This should be stored in an Ansible Vault at vars/platform-secrets.yml or elsewhere and called from a parent playbook.||
|`hub_token`|""|no|Admin User's token on the Automation Hub Server. This should be stored in an Ansible Vault or elsewhere and called from a parent playbook. Either username / password or token need to be specified.||
|`aap_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Platform Server's SSL certificate.||
|`aap_request_timeout`|`10`|no|Specify the timeout Ansible should use in requests to the Galaxy or Automation Hub host.||
|`aap_configuration_collect_logs`|`false`|no|Specify whether to collect async results and continue for all failed async tasks instead of failing on the first error. Collected results are available in the `aap_configuration_role_errors` variable.||
|`aap_configuration_register`|""|no|Specify a variable to register the values of all aap_configuration tasks. This will create an object with each aap object as an element containing a list of each item created.||
|`hub_path_prefix`|""|no|API path used to access the api. Either galaxy, automation-hub, or custom||
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.||
|`hub_team_roles`|`see below`|yes|Data structure describing the roles which are applied to teams, described below.||

### Secure Logging Variables

The following Variables complement each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the team role assignment task does not include sensitive information.
hub_configuration_team_roles_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`hub_configuration_team_roles_secure_logging`|`false`|no|Whether or not to include the sensitive Team role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_timeout`|1000|no|This variable sets the async timeout for the role globally.|
|`hub_configuration_team_roles_async_timeout`|`aap_configuration_async_timeout`|no|This variable sets the async timeout for the role.|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`hub_configuration_team_roles_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`hub_configuration_team_roles_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`hub_configuration_team_roles_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|

## Data Structure

### Team Role Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`team`|""|yes|str|Name of the team to assign the role to. The team must already exist.|
|`organization`|""|no|str|Name or ID of the organization containing the team. Required when teams with the same name exist in multiple organizations.|
|`role`|""|yes|str|Role name to assign to the team (e.g. `galaxy.collection_namespace_owner`). The role must already exist.|
|`targets`|""|no|dict|Resource targets to scope the role to. Required for object-level roles. See below for options.|
|`state`|`present`|no|str|Desired state of the role assignment. Can be `present` or `absent`. If absent, the role is removed from the team.|
|`register`|""|no|str|Variable to set based on the result of the object creation/modification|

#### targets

If no targets are listed, the role is applied globally to the team.
Targets consist of the following.

|Target|Description|
|:---:|:---:|
|`collection_namespaces`|List of collection namespaces to limit the role to. Each namespace receives its own role assignment.|

#### Yaml Example

```yaml
---
hub_team_roles:
  - team: satellite-qe
    organization: Satellite
    role: galaxy.collection_namespace_owner
    targets:
      collection_namespaces:
        - infra
        - test_namespace
    state: present
  - team: satlab-admin
    organization: Satellite
    role: galaxy.user_admin
    state: present
  - team: satlab-admin
    organization: Satellite
    role: galaxy.collection_namespace_owner
    targets:
      collection_namespaces:
        - test_namespace
    state: absent
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add team roles to Automation Hub
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    aap_validate_certs: false
  # Define following vars here, or in ah_configs/ah_auth.yml
  # ah_host: ansible-ah-web-svc-test-project.example.com
  pre_tasks:
    - name: Include vars from ah_configs directory
      ansible.builtin.include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  roles:
    - infra.aap_configuration.hub_team_roles
```

## License

[GPLv3+](https://github.com/redhat-cop/infra.aap_configuration/blob/devel/LICENSE)
