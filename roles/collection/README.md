# redhat_cop.ah_configuration.collection

## Description

An Ansible Role to update, or destroy Automation Hub Collections.

## Variables

These are the sub options for the vars `ah_collections` which are dictionaries with the options you want. See examples for details.
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`namespace`|""|yes|Namespace name. Must be lower case containing only alphanumeric characters and underscores.|"awx"|
|`name`|""|yes|Collection name. Must be lower case containing only alphanumeric characters and underscores.||
|`version`|""|no|Collection Version. Must be lower case containing only alphanumeric characters and underscores.||
|`path`|""|no|Collection artifact file path.||
|`wait`|"true"|no|Waits for the collection to be uploaded||
|`auto_approve`|"true"|no|Approves a collection and requires version to be set.||
|`overwrite_existing`|"true"|no|Overwrites an existing collection and requires version to be set.||
|`state`|"present"|no|Desired state of the resource||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add repository task does not include sensitive information.
ah_configuration_repository_secure_logging defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_repository_secure_logging`|`False`|no|Whether or not to include the sensitive Namespace role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

## Data Structure

### Standard Project Data Structure

#### Yaml Example

```yaml
---
collection:
  namespace: 'awx'
  name: 'awx'
  path: /var/tmp/collections/awx_awx-15.0.0.tar.gz
  state: present

- name: Remove collection
  ah_collection:
    namespace: test_collection
    name: test
    version: 4.1.2
    state: absent
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add collection
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
    - ../../collection
```

## License

[GPLv3+](LICENSE)

## Author

[Inderpal Tiwana](https://github.com/inderpaltiwana/)
