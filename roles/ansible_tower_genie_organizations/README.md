# ansible_tower_genie_organizations
## Description
An Ansible Role to create Organizations in Ansible Tower.

## Requirements 
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed 
Currently:
  awx.awx
## Variables
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`tower_server`|""|yes|URL to the Ansible Tower Server.|127.0.0.1|
|`tower_verify_ssl`|`False`|no|Whether or not to validate the Ansible Tower Server's SSL certificate.||
|`tower_username`|""|yes|Admin User on the Ansible Tower Server.||
|`tower_password`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`tower_oauthtoken`|""|yes|Tower Admin User's token on the Ansible Tower Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`organizations`|`see below`|yes|Data structure describing your orgainzation or orgainzations Described below.||

### Secure Logging Variables
The following Variables compliment each other. 
If Both variables are not set, secure logging defaults to false.  
The role defaults to False as normally the add organization task does not include sensative information.  
tower_genie_organizations_secure_logging defaults to the value of tower_genie_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of genie roles with a single variable, or for the user to selectively use it.  

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_genie_organizations_secure_logging`|`False`|no|Whether or not to include the sensative Organization role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_genie_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Varibles
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`name`|""|yes|Name of Organization|
|`description`|`False`|no|Description of  of Organization.|
|`custom_virtualenv`|""|no|Local absolute file path containing a custom Python virtualenv to use.|
|`max_hosts`|""|no|The max hosts allowed in this organization.|
|`notification_templates_started`|""|no|The notifications on started to use for this organization in a list.|
|`notification_templates_success`|""|no|The notifications on success to use for this organization in a list.|
|`notification_templates_error`|""|no|The notifications on error to use for this organization in a list.|
|`notification_templates_approvals`|""|no|The notifications for approval to use for this organization in a list.|
|`state`|`present`|no|Desired state of the resource.|

### Standard Organization Data Structure
#### Json Example
```json
---
{
    "organizations": [
      {
        "name": "Default",
        "description": "This is the Default Group"
      },
      {
        "name": "Automation Group",
        "description": "This is the Automation Group",
        "custom_virtualenv": "/opt/cust/enviroment/",
        "max_hosts": 10,
        "notification_templates_error": [
          "Slack_for_testing"
        ]
      }      
    ]
}
```
#### Ymal Example
```yaml
---
organizations:
- name: Default
  description: This is the Default Group
- name: Automation Group
  description: This is the Automation Group
  custom_virtualenv: "/opt/cust/enviroment/"
  max_hosts: 10
```
## Playbook Examples
### Standard Role Usage
```yaml
---

- name: Add Organizations to Tower
  hosts: localhost
  connection: local
  gather_facts: false

#Bring in vaulted Ansible Tower secrets
  vars_files:
    - ../tests/vars/tower_secrets.yml

  tasks:

    - name: Get token for use during play
      uri:
        url: "https://{{ tower_server }}/api/v2/tokens/"
        method: POST
        user: "{{ tower_username }}"
        password: "{{ tower_passname }}"
        force_basic_auth: yes
        status_code: 201
        validate_certs: no
      register: user_token
      no_log: True

    - name: Set Tower oath Token
      set_fact:
        tower_oauthtoken: "{{ user_token.json.token }}"

    - name: Import JSON
      include_vars:
        file: "json/organizations.json"
        name: organizations_json

    - name: Add Organizations
      include_role: 
        name: ../..
      vars:
        organizations: "{{ organizations_json.organizations }}"
```
## License
[MIT](LICENSE)

## Author
[Sean Sullivan](https://github.com/Wilk42)
