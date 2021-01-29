# ah_configuration_ah_namespace
## Description
An Ansible Role to create Namespaces in Automation Hub.


## Requirements
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx


## Variables
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`ah_server`|""|yes|URL to the Ansible Tower Server.|127.0.0.1|
|`validate_certs`|`False`|no|Whether or not to validate the Ansible Tower Server's SSL certificate.||
|`ah_token`|""|yes|Tower Admin User's token on the Automation Hub Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`ah_namespaces`|`see below`|yes|Data structure describing your namespaces, described below.||


### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add application task does not include sensitive information.
ah_configuration_namespace_secure_logging defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_namespace_secure_logging`|`False`|no|Whether or not to include the sensitive Namepsace role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|


## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Namespace name. Must be lower case containing only alphanumeric characters and underscores.|
|`new_name`|""|yes|str|Setting this option will change the existing name (looked up via the name field.|
|`description`|""|yes|str|Description to use for the Namespace.|
|`company`|""|no|str|Namespace owner company name.|
|`email`|"password"|yes|str|Namespace contact email.|
|`avatar_url`|"public"|yes|str|Namespace logo URL.|
|`resources`|""|no|str|Namespace resource page in Markdown format.|
|`links`|[]|no|list|A list of dictionaries of Name and url values for links related the Namespace. See below for details.|
|`groups`|[]|yes|list|A list of dictionaries of the Names and object_permissions values for groups that control the Namespace. See below for details.|
|`state`|`present`|no|str|Desired state of the namespace.|

#### Links
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Link Text.|
|`description`|""|yes|str|Link URL.|

#### Groups
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Group Name or ID.|
|`object_permissions`|""|yes|list|List of Permisions granted to the group. Choices of 'change_namespace', 'upload_to_namespace'|

### Standard Project Data Structure

#### Ymal Example
```yaml
---
ah_namespace:
  - name: abc15
    company: Redhat
    email: user@example.com
    avatar_url: https://static.redhat.com/libs/redhat/brand-assets/latest/corp/logo.svg
    description: string
    resources: "# Redhat\nA Namespace test with changes"
    links:
      - name: "New_Google"
        url: "http://www.google.com"
    groups:
      - name: system:partner-engineers
        object_permissions:
          - "change_namespace"
          - "upload_to_namespace"
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
  # ah_server: ansible-ah-web-svc-test-project.example.com
  # ah_token: changeme
  pre_tasks:
    - name: Include vars from ah_configs directory
      include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  roles:
    - ../../namespace
```
## License
[MIT](LICENSE)

## Author
[Mike Shriver](https://github.com/mshriver)
