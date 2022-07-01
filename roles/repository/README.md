# redhat_cop.ah_configuration.repository
## Description
An Ansible Role to create Namespaces in Automation Hub.

## Variables
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes| Repository name. Probably one of community or rh-certified||
|`url`|""|yes|Remote URL for the repository.||
|`auth_url`|""|no|Remote URL for the repository authentication if seperate.||
|`token`|""|no|Token to authenticate to the remote repository.||
|`username`|""|no|Username to authenticate to the remote repository.||
|`password`|""|no|Password to authenticate to the remote repository.||
|`requirements`|""|no|Requirements to download from remote.||
|`requirements_file`|""|no|A yaml requirements file to download from remote.||
|`proxy_url`|""|no|Proxy URL to use for the connection.||
|`proxy_username`|""|no|Proxy URL to use for the connection.||
|`proxy_password`|""|no|Proxy URL to use for the connection.||
|`download_concurrency`|""|no| Number of concurrent collections to download.||



### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add repository task does not include sensitive information.
ah_configuration_repository_secure_logging defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_repository_secure_logging`|`False`|no|Whether or not to include the sensitive Namepsace role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|


### Asynchronous Retry Variables
The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`ah_configuration_repository_async_retries`|`ah_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`ah_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`ah_configuration_repository_async_delay`|`ah_configuration_async_delay`|no|This sets the delay between retries for the role.|


## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Namespace name. Must be lower case containing only alphanumeric characters and underscores.|
<!-- |`new_name`|""|yes|str|Setting this option will change the existing name (looked up via the name field.| -->

### Standard Project Data Structure

#### Yaml Example
```yaml
---
ah_repositories:
  - name: abc15
    description: string
    readme: "# My repo"
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
[Tom Page](https://github.com/Tompage1994/)
