# ah_configuration_ah_namespace
## Description
An Ansible Role to publish collections to Automation Hub or Galaxies.


## Variables
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`ah_host`|""|yes|URL to the Automation Hub or Galaxy Server.|127.0.0.1|
|`validate_certs`|`False`|no|Whether or not to validate the Ansible Tower Server's SSL certificate.||
|`ah_token`|""|no|Admin User's token on the Automation Hub Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`ah_collections`|`see below`|no|Data structure describing your collections, mutually exclusive to ah_collection_list, described below.||
|`ah_collection_list`|`list`|no|Data structure file paths to pre built collections, mutually exclusive with ah_collections.||
|`ah_configuration_working_dir`|`/var/tmp`|no|Data structure describing your namespaces, described below.||
|`ansible_config_path`|`{{ ah_configuration_working_dir }}/ansible.cfg`|no|Data structure describing your namespaces, described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add publish collections task does not include sensitive information.
ah_configuration_publish_secure_logging defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_publish_secure_logging`|`False`|no|Whether or not to include the sensitive publish collections role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|


## Data Structure
### ah_collections Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`repo_name`|""|yes|str|Name of repo, normally the last part before the / in a url.|
|`git_url`|""|yes|str|Url to git repo.|

### Standard Project Data Structure

#### Ymal Example
```yaml
---
ah_collections:
  - repo_name: cisco.iosxr
    git_url: https://github.com/ansible-collections/cisco.iosxr

ansible_config_path: "{{ ah_configuration_working_dir }}/ansible.cfg"

```

## Playbook Examples
### Standard Role Usage
```yaml
---
- name: Add namespace to Automation Hub
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
    - ../../publish
```
## License
[GPLv3+](LICENSE)

## Author
[Sean Sullivan](https://github.com/sean-m-sullivan/)
