# ansible_tower_genie_teams
## Description
An Ansible Role to create Teams in Ansible Tower.
## Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_url`|""|yes|URL to the Ansible Tower Server.|
|`tower_verify_ssl`|False|no|Whether or not to validate the Ansible Tower Server's SSL certificate.|
|`tower_secrets`|False|yes|Whether or not to include variables stored in vars/tower-secrets.yml.  Set this value to `False` if you will be providing the `tower_pass` value from elsewhere.|
|`tower_user`|""|yes|Admin User on the Ansible Tower Server.|
|`tower_pass`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.|
|`tower_org`|""|yes|Ansible Tower organization to create the Ansible Tower team in.|
|`tower_team_name`|""|yes| Name of the Ansible Tower Team to create.|
|`tower_team_desc`|""|no|Description of the Ansible Tower Team to create.|
## Playbook Examples
### Standard Role Usage
```yaml
---
- hosts: all
  roles:
    - role: "genie-teams"
      tower_url: "https:/my-tower-server.foo.bar"
      tower_verify_ssl: False
      tower_user: "admin"
      tower_pass: "{{ my_tower_vault_pass }}"
      tower_org: "MY_ORG"
      tower_team_name: "Developers"
      tower_team_desc: "Team for Development of software deployments."
```
### Included Role within a Loop
``` yaml
---
- hosts: all
  vars:
    tower_url: "https://my-tower-server.foo.bar"
    tower_verify_ssl: False
    tower_user: "admin"
    tower_pass: "{{ my_tower_vault_pass }}"
    tower_org: "MY_ORG"
    teams:
      - name: "team1"
        desc: "My first team"
      - name: "team2"
        desc: "My second team"
      - name: "team3"
        desc: "My third team"
  tasks:
    - name: Create my Ansible Tower Teams
      include_role:
        name: "genie-teams"
      vars:
        tower_team_name: "{{ team.name }}"
        tower_team_desc: "{{ team.desc }}"
      with_items: "{{ teams }}"
      loop_control:
        loop_var: team
```

## License
[MIT](License)

## Author
[Andrew J. Huffman](https://github.com/ahuffman)
