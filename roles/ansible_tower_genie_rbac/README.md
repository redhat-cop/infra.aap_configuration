# ansible_tower_genie_rbac
## Description
An Ansible role to assign role based access controls on Ansible Tower objects to a given team.
## Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_url`|""|yes|URL to the Ansible Tower Server.|
|`tower_verify_ssl`|False|no|Whether or not to validate the Ansible Tower Server's SSL certificate.|
|`tower_secrets`|False|yes|Whether or not to include variables stored in vars/tower-secrets.yml.  Set this value to `False` if you will be providing your sensitive values from elsewhere.|
|`tower_user`|""|yes|Admin User on the Ansible Tower Server.|
|`tower_pass`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.|
|`tower_org`|""|yes|Ansible Tower organization to apply the RBAC controls in.|
|`tower_rbac_credential`||no|Credential to apply the `tower_rbac_role` to.|
|`tower_rbac_inventory`||no|Inventory to apply the `tower_rbac_role` to.|
|`tower_rbac_job_template`||no|Job Template to apply the `tower_rbac_role` to.|
|`tower_rbac_workflow`||no|Workflow to apply the `tower_rbac_role` to.|
|`tower_rbac_project`||no|Project to apply the `tower_rbac_role` to.|
|`tower_rbac_role`|""|yes|Role to assign to the `tower_rbac_team` for the `tower_rbac_cred`, `tower_rbac_inventory`, `tower_rbac_job_template`, `tower_rbac_workflow`, or `tower_rbac_project`. Can be one of the following options: `admin`, `read`, `member`, `execute`, `adhoc`, `update`, `use`, or `auditor`.|
|`tower_rbac_team`|""|yes|Team to assign the role based access control (`tower_rbac_role`) to.|
## Playbook Examples
### Standard Role Usage
```yaml
---
- hosts: all
  roles:
    - role: "genie-rbac"
      tower_url: "https:/my-tower-server.foo.bar"
      tower_verify_ssl: False
      tower_user: "admin"
      tower_pass: "{{ my_tower_vault_pass }}"
      tower_org: "MY_ORG"
      tower_rbac_credential: "Demo Credential"
      tower_rbac_role: "use"
      tower_rbac_team: "team1"
```
## License
[MIT](LICENSE)

## Author
[Andrew J. Huffman](https://github.com/ahuffman)
