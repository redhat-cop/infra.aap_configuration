# infra.eda_configuration.dispatch

## Description

An Ansible Role to run all roles on EDA Controller.

## Requirements

None

## Variables

Each role has its own variables, for information on those please see each role which this role will call. This role has one key variable `eda_configuration_dispatcher_roles` and its default value is shown below:

```yaml
eda_configuration_dispatcher_roles:
  - {role: user, var: eda_users, tags: user}
  - {role: credential, var: eda_credentials, tags: credential}
  - {role: controller_token, var: eda_controller_tokens, tags: controller_token}
  - {role: project, var: eda_projects, tags: project}
  - {role: project_sync, var: eda_projects, tags: project_sync}
  - {role: decision_environment, var: eda_decision_environments, tags: decision_environment}
  - {role: rulebook_activation, var: eda_rulebook_activations, tags: rulebook_activation}
```

Note that each item has three elements:

- `role` which is the name of the role within infra.eda_configuration
- `var` which is the variable which is used in that role. We use this to prevent the role being called if the variable is not set
- `tags` the tags which are applied to the role so it is possible to apply tags to a playbook using the dispatcher with these tags.

It is possible to redefine this variable with a subset of roles or with different tags. In general we suggest keeping the same structure and perhaps just using a subset.

### Authentication

|Variable Name|Default Value|Required|Description|Example|
|:---|:---:|:---:|:---|:---|
|`eda_state`|"present"|no|The state all objects will take unless overridden by object default|'absent'|
|`eda_hostname`|""|yes|URL to the EDA Server.|127.0.0.1|
|`eda_validate_certs`|`True`|no|Whether or not to validate the EDA Controller Server's SSL certificate.||
|`eda_username`|""|no|Admin User on the EDA Controller Server.||
|`eda_password`|""|no|EDA Admin User's password on the EDA Controller Server. This should be stored in an Ansible Vault at vars/eda-secrets.yml or elsewhere and called from a parent playbook.||

### Secure Logging Variables

The role defaults to False as normally most projects task does not include sensitive information.
Each role the dispatch role calls has a separate variable which can be turned on to enforce secure logging for that role but defaults to the value of eda_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it. If neither value is set then each role has a default value of true or false depending on the Red Hat COP suggestions.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`eda_configuration_secure_logging`|""|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role. Each individual role has its own variable which can allow the individual setting of values. See each role for more the variable names.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`eda_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`eda_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Playbook to configure EDA post installation
  hosts: localhost
  connection: local
  pre_tasks:
    - name: Include vars from eda_configs directory
      ansible.builtin.include_vars:
        dir: ./yaml
        ignore_files: [eda_config.yml.template]
        extensions: ["yml"]
  roles:
    - infra.eda_configuration.dispatch
```

## License

[GPL-3.0](https://github.com/redhat-cop/eda_configuration#licensing)

## Author

[Tom Page](https://github.com/Tompage1994)
