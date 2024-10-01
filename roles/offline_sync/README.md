# galaxy.galaxy.offline_sync

## Description

An Ansible Role to offline_sync collections to Automation Hub or Galaxies. NOTE: if you do not provide an ah_token one will be generated which will invalidate any prior token.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`ah_host`|""|yes|URL to the Automation Hub or Galaxy Server. (alias: `ah_hostname`)|127.0.0.1|
|`ah_username`|""|yes|Admin User on the Automation Hub or Galaxy Server.||
|`ah_password`|""|yes|Automation Hub Admin User's password on the Automation Hub Server. This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`ah_token`|""|no|Admin User's token on the Automation Hub Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`ah_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Hub Server's SSL certificate.||
|`ah_request_timeout`|`10`|no|Specify the timeout Ansible should use in requests to the Galaxy or Automation Hub host.||
|`ah_path_prefix`|""|no|API path used to access the api. Either galaxy, automation-hub, or custom||

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`ah_configuration_collection_async_retries`|`ah_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`ah_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`ah_configuration_collection_async_delay`|`ah_configuration_async_delay`|no|This sets the delay between retries for the role.|

## Data Structure

### ah_collections Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`ah_configuration_working_dir`|`/var/tmp/pah_offline_sync`|no|string|The working directory where the collections will be downloaded and any required files.|
|`ah_configuration_no_deps`|false|no|bool|Whether to download all dependencies for each collection or not, if false it may cause errors if dependency sync is off in Automation Hub.|

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Download all collections from Automation Hub
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
      ansible.builtin.include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  roles:
    - galaxy.galaxy.offline_sync
```

### Playbook to upload to offline Automation Hub after using this role to download the collections

```yaml
---
- name: Upload all collections
  hosts: localhost
  gather_facts: false
  connection: local
  vars_files:
    - "collections.yml"
  pre_tasks:
    - name: Include vars from ah_configs directory with collections.yml file added
      ansible.builtin.include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  tasks:
    - name: Ensure the namespaces exists
      ansible.builtin.import_role:
        name: galaxy.galaxy.namespace

    - name: Upload collections
      ansible.builtin.include_role:
        name: galaxy.galaxy.collection
```

## License

[GPLv3+](https://github.com/ansible/galaxy_collection#licensing)

## Author

[David Danielsson](https://github.com/djdanielsson)
