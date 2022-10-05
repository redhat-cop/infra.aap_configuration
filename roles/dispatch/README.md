# ah_configuration.projects

## Description

An Ansible Role to run all roles for which variables are found on Ansible Automation Hub.

## Before Using

This collection is most useful for experienced AAP2 users who want to quickly configure a Automation Hub instance.

If you are new to AAP2 and/or to the redhat_cop.ah_configuration collection, it is highly recommended that you ensure that you're familiar with both AAP2 and the collection, before using this role.

## Variables

Each role that is called also has its own variables. For information on those, please see the README documents for those roles.

The key variable in this role is `ah_configuration_dispatcher_roles`. The default value is shown below:

```yaml
ah_configuration_dispatcher_roles:
  - {role: ansible_config, var: [ansible_config_list, automation_hub_list], tags: config}
  - {role: collection, var: [ah_collections], tags: collections}
  - {role: ee_image, var: [ah_ee_images], tags: images}
  - {role: ee_registry, var: [ah_ee_registries], tags: registries}
  - {role: ee_registry_index, var: [ah_ee_registries], tags: indices}
  - {role: ee_registry_sync, var: [ah_ee_registries], tags: regsync}
  - {role: ee_repository, var: [ah_ee_repositories], tags: repos}
  - {role: ee_repository_sync, var: [ah_ee_repository_sync], tags: reposync}
  - {role: namespace, var: [ah_ee_namespaces], tags: namespaces}
  - {role: group, var: [ah_groups], tags: groups}
  - {role: publish, var: [ah_collections], tags: publish}
  - {role: user, var: [ah_users], tags: users}
```

Each item within the variable has three elements:

- `role` which is the name of the role within redhat_cop.ah_configuration
- `var` which is the variable or variables in that role. We use this to prevent the role being called if the variable is not set.
- `tags` the tags which are applied to the role so it is possible to apply tags to a playbook using the dispatcher with these tags.

If the functionality of Automation Hub is extended in the future, and more variables are able to trigger a role, the new variable should be added into the `var` list for the role above.

### Authentication

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`ah_host`|""|yes|URL to the Automation Hub or Galaxy Server. (alias: `ah_hostname`)|127.0.0.1|
|`ah_username`|""|yes|Admin User on the Automation Hub or Galaxy Server.||
|`ah_password`|""|yes|Automation Hub Admin User's password on the Automation Hub Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`ah_token`|""|yes|Tower Admin User's token on the Automation Hub Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`ah_validate_certs`|`False`|no|Whether or not to validate the Ansible Automation Hub Server's SSL certificate.||
|`ah_path_prefix`|""|no|API path used to access the api. Either galaxy, automation-hub, or custom||

### Secure Logging Variables

The role defaults to False as normally most projects task does not include sensitive information.
Each role the dispatch role calls has a separate variable which can be turned on to enforce secure logging for that role but defaults to the value of controller_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it. If neither value is set then each role has a default value of true or false depending on the Red Hat COP suggestions.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
ah_configuration_ee_registry_secure_logging|`False`|no|Whether or not to include the sensitive Registry role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|""|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role. Each individual role has its own variable which can allow the individual setting of values. See each role for more the variable names.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`ah_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Playbook to configure Ansible Automation Hub post installation
  hosts: localhost
  connection: local
  # Define following vars here, or in ah_configs/controller_auth.yml
  # ah_hostname: ansible-ah-web-svc-test-project.example.com
  # ah_username: admin
  # ah_password: changeme
  pre_tasks:
    - name: Include vars from ah_configs directory
      include_vars:
        dir: ./yaml
        ignore_files: [ah_config.yml.template]
        extensions: ["yml"]
  roles:
    - redhat_cop.ah_configuration.dispatch
```

## License

[MIT](LICENSE)

## Author

[Alan Wong](https://github.com/alawong)
[Tom Page](https://github.com/Tompage1994)
