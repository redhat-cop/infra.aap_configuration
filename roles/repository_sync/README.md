# redhat_cop.ah_configuration.repository_sync

## Description

An Ansible Role to sync Repositories in Automation Hub.

## Variables

These are the sub options for the vars `ah_repository_certified` and `ah_repository_community` which are dictionaries with the options you want. See examples for details.
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`wait`|"false"|no|Wait for the repository to finish syncing before returning.||
|`interval`|"1"|no|The interval to request an update from Automation Hub.||
|`timeout`|""|no|If waiting for the project to update this will abort after this amount of seconds.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add repository task does not include sensitive information.
ah_configuration_repository_secure_logging defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_repository_secure_logging`|`False`|no|Whether or not to include the sensitive Repository roles tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

## Data Structure

### Standard Project Data Structure

#### Yaml Example

```yaml
---
ah_repository_certified:
  url: 'https://cloud.redhat.com/api/automation-hub/<custom_sync_url_from_cloud>'
  token: 'secretToken'

ah_repository_community:
  url: https://galaxy.ansible.com/api/
  requirements:
    - redhat_cop.ah_configuration
    - redhat_cop.controller_configuration
    - redhat_cop.aap_utilities
    - redhat_cop.ee_utilities
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add repository to Automation Hub
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
    - ../../repository_sync
```

## License

[GPLv3+](LICENSE)

## Author

[Inderpal Tiwana](https://github.com/inderpaltiwana/) and [David Danielsson](https://github.com/djdanielsson)
