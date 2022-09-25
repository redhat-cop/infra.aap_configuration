# redhat_cop.ah_configuration.ee_namespace

## Description

An Ansible Role to create Namespaces in Automation Hub.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`ah_host`|""|yes|URL to the Automation Hub or Galaxy Server. (alias: `ah_hostname`)|127.0.0.1|
|`ah_username`|""|yes|Admin User on the Automation Hub or Galaxy Server.||
|`ah_password`|""|yes|Automation Hub Admin User's password on the Automation Hub Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`ah_token`|""|yes|Tower Admin User's token on the Automation Hub Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`ah_validate_certs`|`False`|no|Whether or not to validate the Ansible Automation Hub Server's SSL certificate.||
|`ah_path_prefix`|""|no|API path used to access the api. Either galaxy, automation-hub, or custom||
|`ah_ee_namespaces`|`see below`|yes|Data structure describing your ee_namespaces, described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add ee_namespace task does not include sensitive information.
ah_configuration_ee_namespace_secure_logging defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_ee_namespace_secure_logging`|`False`|no|Whether or not to include the sensitive Namespace role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`ah_configuration_ee_namespace_async_retries`|`ah_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`ah_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`ah_configuration_ee_namespace_async_delay`|`ah_configuration_async_delay`|no|This sets the delay between retries for the role.|

## Data Structure

### EE Namespace Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Namespace name. Must be lower case containing only alphanumeric characters and underscores.|
<!-- |`new_name`|""|yes|str|Setting this option will change the existing name (looked up via the name field.)| -->
|`append`|true|no|bool|Whether to append or replace the groups specified for the ee_namespace.|
|`groups`|[]|yes|list|A list of names for groups that control the Namespace.|
|`state`|`present`|no|str|Desired state of the ee_namespace.|

### Standard Project Data Structure

#### Yaml Example

```yaml
---
ah_ee_namespaces:
  - name: abc15
    append: true
    groups:
      - system:partner-engineers
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add ee_namespace to Automation Hub
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    ah_validate_certs: false
  # Define following vars here, or in ah_configs/ah_auth.yml
  # ah_host: ansible-ah-web-svc-test-project.example.com
  # ah_token: changeme
  pre_tasks:
    - name: Include vars from ah_configs directory
      include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  roles:
    - ../../ee_namespace
```

## License

[GPLv3+](LICENSE)

## Author

[Tom Page](https://github.com/Tompage1994/)
