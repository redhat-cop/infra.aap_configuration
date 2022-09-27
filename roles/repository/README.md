# redhat_cop.ah_configuration.repository

## Description

An Ansible Role to create Repositories in Automation Hub.

## Variables

These are the sub options for the vars `ah_repository_certified` and `ah_repository_community` which are dictionaries with the options you want. See examples for details.
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`url`|"https://cloud.redhat.com/api/automation-hub/"|no|(`ah_repository_certified`)Remote URL for the repository.|"https://console.redhat.com/api/automation-hub/content/1234567-synclist/"|
|`url`|"https://galaxy.ansible.com/api/"|no|(`ah_repository_community`)Remote URL for the repository.||
|`auth_url`|"https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"|no|(`ah_repository_certified`)Remote URL for the repository authentication if separate.||
|`token`|""|no|Token to authenticate to the remote repository.||
|`username`|""|no|Username to authenticate to the remote repository.||
|`password`|""|no|Password to authenticate to the remote repository.||
|`requirements`|""|no|(`ah_repository_community`)Requirements to download from remote.||
|`requirements_file`|""|no|(`ah_repository_community`)A yaml requirements file to download from remote.||
|`proxy_url`|""|no|Proxy URL to use for the connection.||
|`proxy_username`|""|no|Proxy URL to use for the connection.||
|`proxy_password`|""|no|Proxy URL to use for the connection.||
|`ah_token`|""|yes|Tower Admin User's token on the Automation Hub Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`download_concurrency`|"10"|no| Number of concurrent collections to download.||
|`rate_limit`|"8"|no|Limits total download rate in requests per second||
|`signed_only`|"False"|no|Only download signed collections|True|
|`tls_validation`|"True"|no|Whether to use TLS validation against the remote repository|False|
|`client_key`|""|no|A PEM encoded private key file used for authentication||
|`client_cert`|""|no|A PEM encoded client certificate used for authentication||
|`ca_cert`|""|no|A PEM encoded CA certificate used for authentication||
|`client_key_path`|""|no|Path to a PEM encoded private key file used for authentication||
|`client_cert_path`|""|no|Path to a PEM encoded client certificate used for authentication||
|`ca_cert_path`|""|no|Path to a PEM encoded CA certificate used for authentication||

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
    - ../../repository
```

## License

[GPLv3+](LICENSE)

## Author

[Inderpal Tiwana](https://github.com/inderpaltiwana/) and [David Danielsson](https://github.com/djdanielsson)
