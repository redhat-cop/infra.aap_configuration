# controller_configuration.roles
## Description
An Ansible Role to create RBAC Entries on Ansible Controller.

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
|`controller_roles`|`see below`|yes|Data structure describing your RBAC entries described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add rbac task does not include sensitive information.
`controller_configuration_role_secure_logging` defaults to the value of `controller_configuration_secure_logging` if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_role_secure_logging`|`False`|no|Whether or not to include the sensitive rbac role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`controller_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`user`|""|no|str|The user for which the role applies|
|`team`|""|no|str|The team for which the role applies|
|`role`|""|no|str (see note below)|The role which is applied to one of {`target_team`, `inventory`, `job_template`, `target_team`, `inventory`, `job_template`} for either `user` or `team` |
|`target_team`|""|no|str|The team the role applies against|
|`target_teams`|""|no|list|The teams the role applies against|
|`inventory`|""|no|str|The inventory the role applies against|
|`inventories`|""|no|list|The inventories the role applies against|
|`job_template`|""|no|str|The job template the role applies against|
|`job_templates`|""|no|list|The job templates the role applies against|
|`workflow`|""|no|str|The workflow the role applies against|
|`workflows`|""|no|list|The workflows the role applies against|
|`credential`|""|no|str|The credential the role applies against|
|`credentials`|""|no|list|The credentials the role applies against|
|`organization`|""|no|str|The organization the role applies against|
|`organizations`|""|no|list|The organizations the role applies against|
|`lookup_organization`|""|no|str|Organization the inventories, job templates, projects, or workflows the items exists in. Used to help lookup the object, for organization roles see organization. If not provided, will lookup by name only, which does not work with duplicates.|
|`project`|""|no|str|The project the role applies against|
|`projects`|""|no|list|The project the role applies against|
|`state`|`present`|no|str|Desired state of the resource.|

#### Role
`role` must be one of the following:
- `admin`
- `read`
- `member`
- `execute`
- `adhoc`
- `update`
- `use`
- `auditor`
- `project_admin`
- `inventory_admin`
- `credential_admin`
- `workflow_admin`
- `notification_admin`
- `job_template_admin`

### Standard RBAC Data Structure
#### Json Example
```json
{
  "controller_roles": [
    {
      "user": "jdoe",
      "target_team": "My Team",
      "role": "member"
    },
    {
      "team": "My Team",
      "organization": "Default",
      "role": "execute"
    }
  ]
}
```
#### Yaml Example
```yaml
---
controller_roles:
- user: jdoe
  target_team: "My Team"
  role: member
- team: "My Team"
  organization: "Default"
  role: execute
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
    - {role: redhat_cop.controller_configuration.roles, when: controller_roles is defined}
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
