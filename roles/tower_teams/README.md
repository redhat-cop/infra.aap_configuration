# tower_teams
## Description
An Ansible Role to create Teams in Ansible Tower.
## Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_hostname`|""|yes|URL to the Ansible Tower Server.|
|`validate_certs`|False|no|Whether or not to validate the Ansible Tower Server's SSL certificate.|
|`tower_secrets`|False|yes|Whether or not to include variables stored in vars/tower-secrets.yml.  Set this value to `False` if you will be providing the `tower_password` value from elsewhere.|
|`tower_username`|""|yes|Admin User on the Ansible Tower Server.|
|`tower_password`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.|
|`tower_org`|""|yes|Ansible Tower organization to create the Ansible Tower team in.|
|`tower_team_name`|""|yes| Name of the Ansible Tower Team to create.|
|`tower_team_desc`|""|no|Description of the Ansible Tower Team to create.|
## Playbook Examples
### Standard Role Usage
``` yaml
---
- name: Test playbook for local testing
  hosts: localhost
  connection: local
  vars:
    tower_hostname: "https://tower.example.com"
    validate_certs: false
    tower_username: "admin"
    tower_password: "password"
    tower_teams:
      - name: "team1"
        desc: "My first team"
        organization: "Default"
      - name: "team2"
        desc: "My second team"
        organization: "Default"
      - name: "team3"
        desc: "My third team"
        organization: "Default"
  roles:
    - tower_teams
```

## License
[MIT](License)

## Author
[Andrew J. Huffman](https://github.com/ahuffman)
[Kedar Kulkarni](https://github.com/kedark3)
