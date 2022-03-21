# controller_configuration.users
## Description
An Ansible Role to add users to on Ansible Controller.

## Requirements
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx
  or
  ansible.controller

## Variables

### Authentication
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`controller_state`|"present"|no|The state all objects will take unless overridden by object default|'absent'|
|`controller_hostname`|""|yes|URL to the Ansible Controller Server.|127.0.0.1|
|`controller_validate_certs`|`True`|no|Whether or not to validate the Ansible Controller Server's SSL certificate.||
|`controller_username`|""|yes|Admin User on the Ansible Controller Server.||
|`controller_password`|""|yes|Controller Admin User's password on the Ansible Controller Server. This should be stored in an Ansible Vault at vars/controller-secrets.yml or elsewhere and called from a parent playbook.||
|`controller_oauthtoken`|""|yes|Controller Admin User's token on the Ansible Controller Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`controller_user_accounts`|`see below`|yes|Data structure describing your user entries described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add user task does not include sensitive information.
`controller_configuration_user_secure_logging` defaults to the value of `controller_configuration_secure_logging` if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_user_secure_logging`|`False`|no|Whether or not to include the sensitive user role tasks in the log. Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`controller_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables
The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`controller_configuration_users_async_retries`|30|no|This variable sets the number of retries to attempt for the role.|
|`controller_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`controller_configuration_users_async_delay`|1|no|This sets the delay between retries for the role.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`username`|""|yes|str|The username of the user|
|`password`|""|no|str|The password of the user|
|`controller_user_default_password`|""|no|str|Global variable to set the password for all users.|
|`email`|""|yes|str|The email of the user|
|`first_name`|""|no|str|The first name of the user|
|`last_name`|""|no|str|The last name of the user|
|`is_superuser`|false|no|bool|Whether the user is a superuser|
|`is_system_auditor`|false|no|bool|Whether the user is an auditor|
|`organization`|""|no|str|The name of the organization the user belongs to.<br />Added in awx.awx >= 20.0.0 and ansible.controller >= 4.1.1|
|`state`|`present`|no|str|Desired state of the resource.|
|`update_secrets`|true|no|bool| True will always change password if user specifies password, even if API gives $encrypted$ for password. False will only set the password if other values change too.|

### Standard user Data Structure
#### Json Example
```json
{
  "controller_user_accounts": [
    {
      "user": "jsmith",
      "is_superuser": false,
      "password": "p4ssword",
      "email": "jsmith@example.com"
    }
  ]
}
```
#### Yaml Example
```yaml
---
controller_user_accounts:
  - user: controller_user
    is_superuser: false
    password: controller_password
```

## Playbook Examples
### Standard Role Usage
```yaml
---
- name: Playbook to configure ansible controller post installation
  hosts: localhost
  connection: local
  # Define following vars here, or in controller_configs/controller_auth.yml
  # controller_hostname: ansible-controller-web-svc-test-project.example.com
  # controller_username: admin
  # controller_password: changeme
  pre_tasks:
    - name: Include vars from controller_configs directory
      include_vars:
        dir: ./yaml
        ignore_files: [controller_config.yml.template]
        extensions: ["yml"]
  roles:
    - {role: redhat_cop.controller_configuration.users, when: controller_user_accounts is defined}
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
