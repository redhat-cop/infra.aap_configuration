# ansible_tower_genie_projects
## Description
An Ansible Role to create Projects in Ansible Tower.
## Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_url`|""|yes|URL to the Ansible Tower Server.|
|`tower_verify_ssl`|False|no|Whether or not to validate the Ansible Tower Server's SSL certificate.|
|`tower_secrets`|False|yes|Whether or not to include variables stored in vars/tower-secrets.yml.  Set this value to `False` if you will be providing your sensitive values from elsewhere.|
|`tower_user`|""|yes|Admin User on the Ansible Tower Server.|
|`tower_pass`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.|
|`tower_org`|""|yes|Ansible Tower organization to create the Ansible Tower team in.|
|`tower_proj_name`|""|yes|Name of the project to create in Ansible Tower.|
|`tower_proj_desc`|""|yes|Description of the project to create in Ansible Tower.|
|`tower_proj_type`|"git"|yes|Type of project to create in Ansible Tower.  Choices are git, hg, and svn.|
|`tower_proj_branch`|"master"|yes|Branch of the project repository to map to the Ansible Tower project. May also be a specific repository commit or tag.|
|`tower_proj_url`|""|yes|URL to the source control project to create in Ansible Tower.|
|`tower_proj_credential`|""|yes|Credential to use for synchronizing the project in Ansible Tower. Required when creating source control management type projects. Manual projects do not require a credential.|
|`tower_proj_clean`|True|no|Whether or not to clean the local changes in a project during synchronization.|
|`tower_proj_delete`|False|no|Whether or not to delete and re-clone the project during synchronization.|
|`tower_proj_update_on_launch`|False|no|Whether or not to synchronize project prior to launching a job template.|
## Playbook Examples
### Standard Role Usage
```yaml
---
- hosts: all
  roles:
    - role: "genie-projects"
      tower_url: "https:/my-tower-server.foo.bar"
      tower_verify_ssl: False
      tower_user: "admin"
      tower_pass: "{{ my_tower_vault_pass }}"
      tower_org: "MY_ORG"
      tower_proj_name: "Dev - Ansible Playbooks"
      tower_proj_desc: "A collection of playbooks for automating stuff."
      tower_proj_type: "git"
      tower_proj_branch: "dev"
      tower_proj_credential: "My SCM Credential"
      tower_proj_clean: False
      tower_proj_delete: False
      tower_proj_update_on_launch: False
```
## License
[MIT](LICENSE)

## Author
[Andrew J. Huffman](https://github.com/ahuffman)
