<<<<<<< HEAD
# controller_configuration.dispatch

## Description

An Ansible Role to run all roles on Ansible Controller.

## Requirements

ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx
  or
  ansible.controller

## Variables

Each role has its own variables, for information on those please see each role which this role will call. This role has one key variable `controller_configuration_dispatcher_roles` and its default value is shown below:

```yaml
controller_configuration_dispatcher_roles:
  - {role: settings, var: controller_settings, tags: settings}
  - {role: instances, var: controller_instances, tags: instances}
  - {role: instance_groups, var: controller_instance_groups, tags: instance_groups}
  - {role: organizations, var: controller_organizations, tags: organizations}
  - {role: labels, var: controller_labels, tags: labels}
  - {role: users, var: controller_user_accounts, tags: users}
  - {role: teams, var: controller_teams, tags: teams}
  - {role: credential_types, var: controller_credential_types, tags: credential_types}
  - {role: credentials, var: controller_credentials, tags: credentials}
  - {role: credential_input_sources, var: controller_credential_input_sources, tags: credential_input_sources}
  - {role: execution_environments, var: controller_execution_environments, tags: execution_environments}
  - {role: notification_templates, var: controller_notifications, tags: notification_templates}
  - {role: organizations, var: controller_organizations, tags: organizations} # Rerunning with additional dependant values set to be added to the org
  - {role: projects, var: controller_projects, tags: projects}
  - {role: inventories, var: controller_inventories, tags: inventories}
  - {role: inventory_sources, var: controller_inventory_sources, tags: inventory_sources}
  - {role: inventory_source_update, var: controller_inventory_sources, tags: inventory_sources}
  - {role: applications, var: controller_applications, tags: applications}
  - {role: hosts, var: controller_hosts, tags: hosts}
  - {role: bulk_host_create, var: controller_bulk_hosts, tags: bulk_hosts}
  - {role: groups, var: controller_groups, tags: inventories}
  - {role: job_templates, var: controller_templates, tags: job_templates}
  - {role: workflow_job_templates, var: controller_workflows, tags: workflow_job_templates}
  - {role: schedules, var: controller_schedules, tags: schedules}
  - {role: roles, var: controller_roles, tags: roles}
  - {role: job_launch, var: controller_launch_jobs, tags: job_launch}
  - {role: workflow_launch, var: controller_workflow_launch_jobs, tags: workflow_launch}
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
=======
# infra.platform_configuration.dispatch

## Description

An Ansible Role to run all roles in the infra.platform_configuration collection.

## Variables

Each role has its own variables, for information on those please see each role which this role will call. This role has one key variable `dispatch_roles` and its default value is shown below:

```yaml
dispatch_roles:
  - {role: settings, var: settings_list, tags: settings}
  - {role: users, var: users_list, tags: users}
  - {role: authenticators, var: authenticators_list, tags: authenticators}
  - {role: authenticator_maps, var: authenticator_maps_list, tags: authenticator_maps}
  - {role: http_ports, var: http_ports_list, tags: http_ports}
  - {role: organizations, var: organizations_list, tags: organizations}
  - {role: teams, var: teams_list, tags: teams}
  - {role: service_clusters, var: service_clusters_list, tags: service_clusters}
  - {role: service_keys, var: service_keys_list, tags: service_keys}
  - {role: service_nodes, var: service_nodes_list, tags: service_nodes}
  - {role: services, var: services_list, tags: services}
  - {role: routes, var: routes_list, tags: routes}
  - {role: role_user_assignments, var: role_user_assignments_list, tags: role_user_assignments}
>>>>>>> 40b40ddac1c00aac7d878bd41af23a6d562296e5
```

Note that each item has three elements:

<<<<<<< HEAD
- `role` which is the name of the role within infra.controller_configuration
- `role` which is the name of the role within infra.eda_configuration
=======
- `role` which is the name of the role within infra.platform_configuration
>>>>>>> 40b40ddac1c00aac7d878bd41af23a6d562296e5
- `var` which is the variable which is used in that role. We use this to prevent the role being called if the variable is not set
- `tags` the tags which are applied to the role so it is possible to apply tags to a playbook using the dispatcher with these tags.

It is possible to redefine this variable with a subset of roles or with different tags. In general we suggest keeping the same structure and perhaps just using a subset.
<<<<<<< HEAD
# galaxy.galaxy.dispatch

## Description

An Ansible Role to run all roles for which variables are found on Ansible Automation Hub.

## Before Using

This collection is most useful for experienced AAP2 users who want to quickly configure a Automation Hub instance.

If you are new to AAP2 and/or to the galaxy.galaxy collection, it is highly recommended that you ensure that you're familiar with both AAP2 and the collection, before using this role.

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
  - {role: namespace, var: [ah_namespaces], tags: namespaces}
  - {role: group, var: [ah_groups], tags: groups}
  - {role: publish, var: [ah_collections], tags: publish}
  - {role: user, var: [ah_users], tags: users}
```

Each item within the variable has three elements:

- `role` which is the name of the role within galaxy.galaxy
- `var` which is the variable or variables in that role. We use this to prevent the role being called if the variable is not set.
- `tags` the tags which are applied to the role so it is possible to apply tags to a playbook using the dispatcher with these tags.

If the functionality of Automation Hub is extended in the future, and more variables are able to trigger a role, the new variable should be added into the `var` list for the role above.

The `ah_configuration_async_dir` variable sets the directory to write the results file for async tasks.
The default value is set to  `null` which uses the Ansible Default of `/root/.ansible_async/`.

### Authentication

|Variable Name|Default Value|Required|Description|Example|
|:---|:---:|:---:|:---|:---|
|`controller_state`|"present"|no|The state all objects will take unless overridden by object default|'absent'|
|`controller_hostname`|""|yes|URL to the Ansible Controller Server.|127.0.0.1|
|`controller_validate_certs`|`True`|no|Whether or not to validate the Ansible Controller Server's SSL certificate.||
|`controller_username`|""|no|Admin User on the Ansible Controller Server. Either username / password or oauthtoken need to be specified.||
|`controller_password`|""|no|Controller Admin User's password on the Ansible Controller Server. This should be stored in an Ansible Vault at vars/controller-secrets.yml or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.||
|`controller_oauthtoken`|""|no|Controller Admin User's token on the Ansible Controller Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.||
|`controller_request_timeout`|`10`|no|Specify the timeout in seconds Ansible should use in requests to the controller host.||
|:---:|:---:|:---:|:---:|:---:|
|`ah_host`|""|yes|URL to the Automation Hub or Galaxy Server. (alias: `ah_hostname`)|127.0.0.1|
|`ah_username`|""|yes|Admin User on the Automation Hub or Galaxy Server.||
|`ah_password`|""|yes|Automation Hub Admin User's password on the Automation Hub Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`ah_token`|""|yes|Tower Admin User's token on the Automation Hub Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`ah_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Hub Server's SSL certificate.||
|`ah_path_prefix`|""|no|API path used to access the api. Either galaxy, automation-hub, or custom||
|`eda_state`|"present"|no|The state all objects will take unless overridden by object default|'absent'|
|`eda_hostname`|""|yes|URL to the EDA Server.|127.0.0.1|
|`eda_validate_certs`|`True`|no|Whether or not to validate the EDA Controller Server's SSL certificate.||
|`eda_username`|""|no|Admin User on the EDA Controller Server.||
|`eda_password`|""|no|EDA Admin User's password on the EDA Controller Server. This should be stored in an Ansible Vault at vars/eda-secrets.yml or elsewhere and called from a parent playbook.||

### Secure Logging Variables

The role defaults to False as normally most projects task does not include sensitive information.
Each role the dispatch role calls has a separate variable which can be turned on to enforce secure logging for that role but defaults to the value of controller_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it. If neither value is set then each role has a default value of true or false depending on the Red Hat COP suggestions.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_secure_logging`|""|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|
Each role the dispatch role calls has a separate variable which can be turned on to enforce secure logging for that role but defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it. If neither value is set then each role has a default value of true or false as determined by best practices for each role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_ee_registry_secure_logging`|`False`|no|Whether or not to include the sensitive Registry role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|""|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|
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
|`controller_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`controller_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`ah_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`ah_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`eda_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`eda_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Playbook to configure ansible controller post installation
  hosts: localhost
  connection: local
  # Define following vars here, or in controller_configs/controller_auth.yml
  # controller_hostname: ansible-controller-web-svc-test-project.example.com
  # controller_username: admin
  # controller_password: changeme
  pre_tasks:
    - name: Include vars from controller_configs directory
      ansible.builtin.include_vars:
        dir: ./yaml
        ignore_files: [controller_config.yml.template]
        extensions: ["yml"]
  roles:
    - infra.controller_configuration.dispatch
- name: Playbook to configure Ansible Automation Hub post installation
  hosts: localhost
  connection: local
  # Define following vars here, or in ah_configs/controller_auth.yml
  # ah_hostname: ansible-ah-web-svc-test-project.example.com
  # ah_username: admin
  # ah_password: changeme
  pre_tasks:
    - name: Include vars from ah_configs directory
      ansible.builtin.include_vars:
        dir: ./yaml
        ignore_files: [ah_config.yml.template]
        extensions: ["yml"]
  roles:
    - galaxy.galaxy.dispatch
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

[GPL-3.0](https://github.com/redhat-cop/controller_configuration#licensing)

## Author

[GPLv3+](https://github.com/ansible/galaxy_collection#licensing)

## Author

[Alan Wong](https://github.com/alawong)
[GPL-3.0](https://github.com/redhat-cop/eda_configuration#licensing)

## Author

[Tom Page](https://github.com/Tompage1994)
=======

For more information about variables, see [top-level README](../../README.md). 
For more information about roles, see each roles' README (also linked in the top-level README)

## License

[GPLv3](https://github.com/ansible/aap-gateway/gateway_configuration_collection/COPYING)
>>>>>>> 40b40ddac1c00aac7d878bd41af23a6d562296e5
