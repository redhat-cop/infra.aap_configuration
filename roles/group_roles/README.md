# group_roles

## Description

An Ansible Role to add roles to groups in Automation Hub.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`ah_host`|""|yes|URL to the Automation Hub or Galaxy Server. (alias: `ah_hostname`)|127.0.0.1|
|`ah_username`|""|yes|Admin User on the Automation Hub or Galaxy Server.||
|`ah_password`|""|yes|Automation Hub Admin User's password on the Automation Hub Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`ah_validate_certs`|`False`|no|Whether or not to validate the Ansible Automation Hub Server's SSL certificate.||
|`ah_request_timeout`|`10`|no|Specify the timeout Ansible should use in requests to the Galaxy or Automation Hub host.||
|`ah_path_prefix`|""|no|API path used to access the api. Either galaxy, automation-hub, or custom||
|`ah_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.||
|`ah_groups`|`see below`|yes|Data structure describing your groups, described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add group task does not include sensitive information.
ah_configuration_group_secure_logging defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_group_secure_logging`|`False`|no|Whether or not to include the sensitive Namespace role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`ah_configuration_group_async_retries`|`ah_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`ah_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`ah_configuration_group_async_delay`|`ah_configuration_async_delay`|no|This sets the delay between retries for the role.|

## Data Structure

### Group Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`groups`|""|yes|str| List of Group Names to apply the roles to. If the group does not exist, it will be created. Must be lower case containing only alphanumeric characters and underscores.|
|`role_list`|""|yes|str|The list of roles to add to or remove from the given group. See below for options.|
|`state`|`present`|no|str|Desired state of the group. Can be `present`, `enforced`, or `absent`. If absent, then the module deletes the given combination of roles for given groups. If present, then the module creates the group roles if it does not already exist. If enforced, then the module will remove any group role combinations not provided.|

#### role_list

The `role_list` variable is a combination of roles and targets that are applied to the groups listed in `groups`.
The structure look slike

```yaml
- roles:
    - container.containerdistribution_owner
  targets:
    execution_environments:
      - ee-minimal-rhel8
```

Roles can be those that were created using the `role` role, the `ah_role`, or the built in roles.

If no targets are listed, the roles are applied globally to the groups.
Targets consist of the following.

|Target|Description|
|:---:|:---:|
|`collection_namespaces`|List of collection namespaces to apply the roles to.|
|`collection_remotes`|List of collection remotes to apply the roles to.|
|`collection_repositories`|List of collection repositories to apply the roles to.|
|`execution_environments`|List of execution environments to apply the roles to.|
|`container_registery_remotes`|List of container registery remotes to apply the roles to.|

#### Yaml Example

```yaml
---
ah_group_roles:
  - state: present
    groups:
      - santa
      - group1
    role_list:
      - roles:
          - container.containerdistribution_owner
        targets:
          execution_environments:
            - redhat_cop/config_as_code_ee
      - roles:
          - galaxy.container_remote
        targets:
          container_registery_remotes:
            - quay
      - roles:
          - galaxy.user_admin
          - galaxy.group_admin
      - roles:
          - galaxy.ansible_repository_owner
        targets:
          collection_repositories:
            - validated
      - roles:
          - galaxy.collection_remote_owner
        targets:
          collection_remotes:
            - community
      - roles:
          - galaxy.collection_namespace_owner
        targets:
          collection_namespaces:
            - autohubtest2
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add group roles to Automation Hub
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    ah_validate_certs: false
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
    - ../../group_roles
```

## License

[GPLv3+](https://github.com/redhat-cop/ah_configuration#licensing)

## Author

[Tom Page](https://github.com/Tompage1994/)
