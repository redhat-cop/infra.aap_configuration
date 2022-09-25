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
|`ah_host`|""|yes|URL to the Automation Hub or Galaxy Server. (alias: `ah_hostname`)|127.0.0.1|
|`ah_username`|""|yes|Admin User on the Automation Hub or Galaxy Server.||
|`ah_password`|""|yes|Automation Hub Admin User's password on the Automation Hub Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`ah_token`|""|yes|Tower Admin User's token on the Automation Hub Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`ah_validate_certs`|`False`|no|Whether or not to validate the Ansible Automation Hub Server's SSL certificate.||
|`ah_namespaces`|`see below`|yes|Data structure describing your namespaces, described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the ansible config task does not by default include sensitive information, we highly recommend the use of ansible vault for passwords and tokens.
ah_configuration_ansible_config_secure_logging defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_ansible_config_secure_logging`|`False`|no|Whether or not to include the sensitive ansible config role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

## Data Structure

### Namespaces Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`ansible_config_mode`|'0644'|no|int/str|The permissions the resulting ansible config file or directory should have.|
|`ah_configuration_working_dir`|"/var/tmp"|no|path|Location to render the ansible config file to.|
|`automation_hub_list`|""|yes|list|A list of Automation hubs and galaxies to put in the ansible config, see below for details.|
|`ansible_config_list`|""|no|list|A set of ansible config settings, a default is set, but can be overridden, see below for details.|
|`ah_validate_certs`|"false"|no|list|Set to determine if certificates should be validated.|

#### automation_hub_list

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Name of the Automation Hub or Galaxy Server.|
|`url`|""|yes|str|URL to the Automatin Hub or Galaxy Server|
|`auth_url`|""|yes|str|URL to use for alternate authentication to the Automatin Hub or Galaxy Server.|
|`ah_token`|""|yes|str|Automatin Hub or Galaxy Server token.|
|`ah_username`|""|yes|str|Automatin Hub or Galaxy Server username.|
|`ah_password`|""|yes|str|Automatin Hub or Galaxy Server password.|

#### ansible_config_list

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`header`|""|yes|str|Header of the section that contains keypairs.|
|`keypairs`|""|yes|list|List key value pairs for settings in the ansible.cfg.|

#### ansible_config_list[].keypairs

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`key`|""|yes|str|Key for entry under this header.|
|`value`|""|yes|str|Value for entry for the cooresponding key.|

### Standard Project Data Structure

#### Yaml Example

```yaml
---
ansible_config_list:
  - header: galaxy
    keypairs:
      - key: ignore_certs
        value: "{{ validate_certs | bool }}"
      - key: server_list
        value: "{{ automation_hub_list | map(attribute="name") | join(",") }}"

automation_hub_list:
  - name: automation_hub
    url: "{{ah_host}}/api/automation-hub/"
    username: "{{ ah_username }}"
    password: "{{ ah_password }}"
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
    - ../../ansible_config
```

## License

[GPLv3+](LICENSE)

## Author

[Sean Sullivan](https://github.com/sean-m-sullivan/)
