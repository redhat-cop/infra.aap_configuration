# controller_configuration.license
## Description
An Ansible Role to deploy a license on Ansible Controller.

## Requirements
ansible-galaxy collection install  -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx
  or
  ansible.controller

## Variables

### Authentication
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`controller_state`|"present"|no|The state all objects will take unless overriden by object default|'absent'|
|`controller_hostname`|""|yes|URL to the Ansible Controller Server.|127.0.0.1|
|`controller_validate_certs`|`True`|no|Whether or not to validate the Ansible Controller Server's SSL certificate.||
|`controller_username`|""|yes|Admin User on the Ansible Controller Server.||
|`controller_password`|""|yes|Controller Admin User's password on the Ansible Controller Server.  This should be stored in an Ansible Vault at vars/controller-secrets.yml or elsewhere and called from a parent playbook.||
|`controller_oauthtoken`|""|yes|Controller Admin User's token on the Ansible Controller Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`controller_license`|`see below`|yes|Data structure describing your license for controller, described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add license task does not include sensitive information.
controller_configuration_license_secure_logging defaults to the value of controller_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_license_secure_logging`|`False`|no|Whether or not to include the sensitive license role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`controller_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`manifest`|""|yes|obj|File path to a Red Hat subscription manifest (a .zip file)|
|`eula_accepted`|""|yes|bool|Whether to accept the End User License Agreement for Ansible controller|
|`force`|`False`|no|bool|By default, the license manifest will only be applied if controller is currentlyunlicensed or trial licensed.  When force=true, the license is always applied.|

For further details on fields see https://docs.ansible.com/ansible-tower/latest/html/userguide/credential_plugins.html

### Standard Project Data Structure
#### Json Example
```json
---
{
    "controller_license": {
        "data": "{{ lookup('file', '/tmp/my_controller.license') }}",
        "force": true
      }
}
```
#### Yaml Example
```yaml
---
controller_license:
  data: "{{ lookup('file', '/tmp/my_controller.license') }}"
  force: false
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
    - {role: redhat_cop.controller_configuration.license, when: controller_license is defined}
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
