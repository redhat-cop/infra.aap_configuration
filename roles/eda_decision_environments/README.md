# infra.aap_configuration.eda_decision_environments

## Description

An Ansible Role to create Decision Environments in EDA Controller.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---|:---:|:---:|:---|:---|
|`platform_state`|"present"|no|The state all objects will take unless overridden by object default|'absent'|
|`aap_hostname`|""|yes|URL to the Ansible Automation Platform Server.|127.0.0.1|
|`aap_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Platform Server's SSL certificate.||
|`aap_username`|""|no|Admin User on the Ansible Automation Platform Server. Either username / password or oauthtoken need to be specified.||
|`aap_password`|""|no|Platform Admin User's password on the Server.  This should be stored in an Ansible Vault at vars/platform-secrets.yml or elsewhere and called from a parent playbook.||
|`aap_token`|""|no|Controller Admin User's token on the Ansible Automation Platform Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.||
|`aap_request_timeout`|`10`|no|Specify the timeout in seconds Ansible should use in requests to the controller host.||
|`aap_configuration_collect_logs`|`false`|no|Specify whether to collect async results and continue for all failed async tasks instead of failing on the first error. Collected results are available in the `aap_configuration_role_errors` variable.||
|`aap_configuration_register`|""|no|Specify a variable to register the values of all aap_configuration tasks. This will create an object with each aap object as an element containing a list of each item created.||
|`eda_decision_environments`|`see below`|yes|Data structure describing your users Described below.||

### Secure Logging Variables

The following Variables complement each other.
If Both variables are not set, secure logging defaults to false.
The role-specific setting below controls secure logging. It can be set for this role or shared across roles with `aap_configuration_secure_logging`.
eda_configuration_decision_environments_secure_logging uses the shared `aap_configuration_secure_logging` setting unless explicitly overridden. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`eda_configuration_decision_environments_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|Whether to hide sensitive task output for this role.|
|`aap_configuration_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|Whether to hide sensitive task output across roles.|

### Asynchronous Retry Variables

The following variables control asynchronous result collection and the delay between items in a loop.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---|
|`aap_configuration_async_retries`|50|no|Default number of result checks across roles.|
|`eda_configuration_decision_environments_async_retries`|`aap_configuration_async_retries`|no|Number of result checks for this role.|
|`aap_configuration_async_delay`|1|no|Default delay between asynchronous result checks across roles.|
|`eda_configuration_decision_environments_async_delay`|`aap_configuration_async_delay`|no|Delay between asynchronous result checks for this role.|
|`aap_configuration_loop_delay`|0|no|Default pause between loop items across roles.|
|`eda_configuration_decision_environments_loop_delay`|`aap_configuration_loop_delay`|no|Pause between loop items for this role.|
|`aap_configuration_async_dir`|`null`|no|Directory for async task result files; `null` uses Ansible's default `/root/.ansible_async/`.|

## Data Structure

### Decision Environment Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Decision Environment name. Must be lower case containing only alphanumeric characters and underscores.|
|`new_name`|""|no|str|Setting this option will change the existing name (looked up via the name field.)|
|`description`|""|no|str|Description to use for the Project.|
|`image_url`|""|yes|str|A URL to a a container image to use for the decision environment.|
|`credential`|""|no|str|The credential used to access the container registry holding the image.|
|`organization`|""|no|str|Organization this decision environment belongs to.|
|`state`|`present`|no|str|Desired state of the decision environment.|
|`register`|""|no|str|Variable to set based on the result of the object creation/modification|

### Standard Decision Environment Data Structure

#### Yaml Example

```yaml
---
eda_decision_environments:
  - name: my_default_de
    description: my default decision environment
    image_url: "image_registry.example.com/default-de:latest"
    credential: my_credential
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add decision environment to EDA Controller
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    eda_validate_certs: false
  # Define following vars here, or in eda_configs/eda_auth.yml
  # controller_host: ansible-eda-web-svc-test-project.example.com
  # eda_token: changeme
  pre_tasks:
    - name: Include vars from eda_configs directory
      ansible.builtin.include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  roles:
    - infra.aap_configuration.eda_decision_environments
```

## License

[GPLv3+](https://github.com/redhat-cop/infra.aap_configuration/blob/devel/LICENSE)

## Author

[Derek Waters](https://github.com/derekwaters/)
