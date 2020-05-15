# ansible_tower_genie_projects
## Description
An Ansible Role to create Projects in Ansible Tower.

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
|`projects`|`see below`|yes|Data structure describing your orgainzation or orgainzations Described below.||

### Secure Logging Variables
The following Variables compliment each other. 
If Both variables are not set, secure logging defaults to false.  
The role defaults to False as normally the add organization task does not include sensative information.  
tower_genie_projects_secure_logging defaults to the value of tower_genie_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of genie roles with a single variable, or for the user to selectively use it.  

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_genie_projects_secure_logging`|`False`|no|Whether or not to include the sensative Project role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_genie_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Varibles
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`name`|""|yes|Name of Project|
|`description`|`False`|no|Description of the Project.|
|`organization`|`False`|yes|Name of organization for project.|
|`scm_type`|""|no|Type of SCM resource.|
|`scm_url`|""|no|URL of SCM resource.|
|`local_path`|""|no|The server playbook directory for manual projects.|
|`scm_branch`|""|no|The branch to use for the SCM resource.|
|`scm_refspec`|""|no|The refspec to use for the SCM resource.|
|`scm_credential`|""|no|Name of the credential to use with this SCM resource.|
|`scm_clean`|""|no|Remove local modifications before updating.|
|`scm_delete_on_update`|""|no|Remove the repository completely before updating.|
|`scm_update_on_launch`|""|no|Before an update to the local repository before launching a job with this project.|
|`scm_update_cache_timeout`|""|no|Cache Timeout to cache prior project syncs for a certain number of seconds. Only valid if scm_update_on_launch is to True, otherwise ignored.|
|`allow_override`|""|no|Allow changing the SCM branch or revision in a job template that uses this project.|
|`job_timeout`|""|no|The amount of time (in seconds) to run before the SCM Update is canceled. A value of 0 means no timeout.|
|`custom_virtualenv`|""|no|Local absolute file path containing a custom Python virtualenv to use.|
|`notification_templates_started`|""|no|The notifications on started to use for this organization in a list.|
|`notification_templates_success`|""|no|The notifications on success to use for this organization in a list.|
|`notification_templates_error`|""|no|The notifications on error to use for this organization in a list.|
|`state`|`present`|no|Desired state of the resource.|
|`wait`|""|no|Provides option to wait for completed project sync before returning.|

### Standard Project Data Structure
#### Json Example
```json
---
{
    "projects": [
      {
        "name": "Tower Config",
        "organization": "Default",
        "scm_branch": "master",
        "scm_clean": "no",
        "scm_delete_on_update": "no",
        "scm_type": "git",
        "scm_update_on_launch": "no",
        "scm_url": "https://github.com/ansible/tower-example.git",
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
projects:
- name: Tower Config
  organization: Default
  scm_branch: master
  scm_clean: 'no'
  scm_delete_on_update: 'no'
  scm_type: git
  scm_update_on_launch: 'no'
  scm_url: https://github.com/ansible/tower-example.git
  notification_templates_error:
  - Slack_for_testing

```
## Playbook Examples
### Standard Role Usage
```yaml
---

- name: Add Projects to Tower
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
        file: "json/projects.json"
        name: projects_json

    - name: Add Projects
      include_role: 
        name: ../..
      vars:
        projects: "{{ projects_json.projects }}"
```
## License
[MIT](LICENSE)

## Author
[Sean Sullivan](https://github.com/Wilk42)
