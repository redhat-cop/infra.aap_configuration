# tower_configuration.notifications
## Description
An Ansible Role to add notifications to Ansible Tower.

## Requirements
ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx

## Variables
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`tower_state`|"present"|no|The state all objects will take unless overriden by object default|'absent'|
|`tower_hostname`|""|yes|URL to the Ansible Tower Server.|127.0.0.1|
|`validate_certs`|`False`|no|Whether or not to validate the Ansible Tower Server's SSL certificate.||
|`tower_username`|""|yes|Admin User on the Ansible Tower Server.||
|`tower_password`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`tower_oauthtoken`|""|yes|Tower Admin User's token on the Ansible Tower Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`tower_notifications`|`see below`|yes|Data structure describing your notification entries described below.||

### Secure Logging Variables
The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add notification task does not include sensative information.
`tower_configuration_notification_secure_logging` defaults to the value of `tower_configuration_secure_logging` if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_notification_secure_logging`|`False`|no|Whether or not to include the sensitive notification role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Variables
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|The name of the notification|
|`description`|""|no|str|The description of the notification|
|`host`|""|yes|str|The host for the notification|
|`channels`|""|no|list|The channels for the notification|
|`nickname`|""|no|str|The nickname of the notification|
|`notification_type`|""|no|str|The type of notification|
|`organization`|""|no|str|The organization applicable to the notification|
|`username`|""|no|str|The username applicable to the notification|
|`password`|""|no|str|The password applicable to the notification|
|`port`|""|no|str|The port applicable to the notification|
|`recipients`|[]|no|list|The notification recipients|
|`sender`|""|no|str|The notification sender|
|`server`|""|no|str|The notification server|
|`targets`|""|no|list|The notification targets|
|`use_ssl`|false|no|bool|Whether the notification uses SSL|
|`use_tls`|false|no|bool|Whether the notification uses TLS|
|`state`|`present`|no|str|Desired state of the resource.|


### Standard notification Data Structure
#### Json Example
```json
{
  "tower_notification": [
    {
      "name": "localhost",
      "inventory": "My Inv",
      "variables": {
        "my_var": true
      }
    }
  ]
}
```
#### Ymal Example
```yaml
---
tower_notifications:
  - name: localhost
    inventory: localhost
    variables:
      some_var: some_val
      ansible_connection: local
```

## Playbook Examples
### Standard Role Usage
```yaml
---

- name: Add notification entry to Tower
  hosts: localhost
  connection: local
  gather_facts: false
  tasks:
    - name: Get token for use during play
      uri:
        url: "https://{{ tower_hostname }}/api/v2/tokens/"
        method: POST
        user: "{{ tower_username }}"
        password: "{{ tower_passname }}"
        force_basic_auth: true
        status_code: 201
        validate_certs: false
      register: user_token
      no_log: True

    - name: Set Tower oath Token
      set_fact:
        tower_oauthtoken: "{{ user_token.json.token }}"

    - name: Import JSON
      include_vars:
        file: "json/notification.json"
        name: notification_json

    - name: Add Projects
      include_role:
        name: tower_notification
      vars:
        tower_notification: "{{ notification_json.tower_notification }}"
```
## License
[MIT](LICENSE)

## Author
[Tom Page](https://github.com/Tompage1994)
