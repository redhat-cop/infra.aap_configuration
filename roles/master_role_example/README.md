# tower_configuration_***********
## Description
An Ansible Role to create Job Templates in Ansible Tower.

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
|`tower_************`|`see below`|yes|Data structure describing your orgainzation or orgainzations Described below.||

### Secure Logging Variables
The following Variables compliment each other. 
If Both variables are not set, secure logging defaults to false.  
The role defaults to False as normally the add organization task does not include sensative information.  
tower_configuration_*******_secure_logging defaults to the value of tower_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of tower configuration roles with a single variable, or for the user to selectively use it.  

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_configuration_*******_secure_logging`|`False`|no|Whether or not to include the sensative Project role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`tower_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared accross multiple roles, see above.|

## Data Structure
### Varibles
|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Name of Job Template|
|`new_name`|""|str|no|Setting this option will change the existing name (looked up via the name field).|
|`description`|`False`|no|str|Description to use for the job template.|

|`state`|`present`|no|str|Desired state of the resource.|



### Standard Project Data Structure
#### Json Example
```json
---
 
```
#### Ymal Example
```yaml
---

```

## Playbook Examples
### Standard Role Usage
```yaml

```
## License
[MIT](LICENSE)

## Author
[************](************)
