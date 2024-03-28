# infra.eda_configuration.rulebook_activation

## Description

An Ansible Role to create rulebook activations in EDA Controller.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`eda_host`|""|yes|URL to the EDA Controller (alias: `eda_hostname`)|127.0.0.1|
|`eda_username`|""|yes|Admin User on the EDA Controller ||
|`eda_password`|""|yes|EDA Controller Admin User's password on the EDA Controller Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`eda_validate_certs`|`False`|no|Whether or not to validate the Ansible EDA Controller Server's SSL certificate.||
|`eda_request_timeout`|`10`|no|Specify the timeout Ansible should use in requests to the EDA Controller host.||
|`eda_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.||
|`eda_rulebook_activations`|`see below`|yes|Data structure describing your rulebook activations, described below.||

### Secure Logging Variables

The following Variables complement each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add project task does not include sensitive information.
eda_configuration_project_secure_logging defaults to the value of eda_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of EDA Controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`eda_configuration_project_secure_logging`|`False`|no|Whether or not to include the sensitive Project role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`eda_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`eda_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`eda_configuration_project_async_retries`|`eda_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`eda_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`eda_configuration_project_async_delay`|`eda_configuration_async_delay`|no|This sets the delay between retries for the role.|

## Data Structure

### Rulebook activation Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Rulebook activation name. Must be lower case containing only alphanumeric characters and underscores.|
|`description`|""|no|str|Description to use for the Activation.|
|`project`|""|no|str|project to use for the Activation.|
|`rulebook`|""|yes|str|rulebook to use for the Activation.|
|`decision_environment`|""|yes|str|decision_environment to use for the Activation.|
|`restart_policy`|"always"|no|str|restart_policy to use for the Activation, choice of ["always", "never", "on_failure"]|
|`extra_vars`|""|no|str|extra_vars to use for the Activation.|
|`enabled`|"true"|no|str|Whether the rulebook activation is automatically enabled to run.|
|`state`|`present`|no|str|Desired state of the rulebook activation.|

### Standard rulebook activation Data Structure

#### Yaml Example

```yaml
---
eda_rulebook_activations:
  - name: Github Hook
    description: Hook to listen for changes in GitHub
    project: EDA_example
    rulebook: git-hook-deploy-rules.yml
    decision_environment: Automation Hub Default Decision Environment
    extra_vars:
      provider: github-local
      repo_url: https://github.com/ansible/ansible-rulebook.git
    enabled: false
    state: present
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add rulebook activation to EDA Controller
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    eda_validate_certs: false
  # Define following vars here, or in eda_configs/eda_auth.yml
  # eda_host: ansible-eda-web-svc-test-project.example.com
  # eda_token: changeme
  pre_tasks:
    - name: Include vars from eda_configs directory
      ansible.builtin.include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  roles:
    - ../../rulebook_activation
```

## License

[GPLv3+](https://github.com/redhat-cop/eda_configuration#licensing)

## Author

[Tom Page](https://github.com/Tompage1994/)
