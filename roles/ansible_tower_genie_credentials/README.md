# ansible_tower_genie_credentials
## Description
An Ansible Role to create a Credential in Ansible Tower.
## Variables
|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`tower_url`|""|yes|URL to the Ansible Tower Server.|
|`tower_verify_ssl`|False|no|Whether or not to validate the Ansible Tower Server's SSL certificate.|
|`tower_secrets`|False|yes|Whether or not to include variables stored in vars/tower-secrets.yml.  Set this value to `False` if you will be providing your sensitive values from elsewhere.|
|`tower_user`|""|yes|Admin User on the Ansible Tower Server.|
|`tower_pass`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at= vars/tower-secrets.yml or elsewhere and called from a parent playbook.|
|`tower_org`|""|yes|Ansible Tower organization to create the Ansible Tower team in.|
|`tower_cred_name`|""|yes|Name of the credential to create in Ansible Tower.|
|`tower_cred_user`|""|yes|Username of the credential. For AWS credentials, this is the access key.|
|`tower_cred_pass`|"ASK"|no|Password of the credential.  Not required when using SSH keys.  This value should be stored in an Ansible Vault at vars/tower-secrets.yml.  Use the value "ASK" for password prompting. This is **required** for **AWS credentials** and is your secret key.|
|`tower_cred_desc`|""|no|Description of the credential.|
|`tower_cred_type`|""|yes|Type of Ansible Tower credential to create.  Value can be one of the following types ssh, vault, net, scm, aws, vmware, satellite6, cloudforms, gce, azure_rm, openstack, rhv, insights, tower.|
|`tower_cred_ssh_key_path`|""|no|Path to a SSH private key for an Ansible Tower credential to use.|
|`tower_cred_ssh_key_pass`|"ASK"|no|Password to unlock a SSH private key.  Use the value "ASK" for password prompting.|
|`tower_cred_vault_pass`|"ASK"|no|Password for your Ansible Vault file. Use the value "ASK" for password prompting.|
|`tower_cred_authorize`|False|no|Whether or not to enable Authorize for network devices.|
|`tower_cred_authorize_password`|""|no|Authorize password for network devices.|


## Playbook Examples
### Standard Role Usage
```yaml
---
- hosts: all
  roles:
    - role: "genie-credentials"
      tower_url: "https:/my-tower-server.foo.bar"
      tower_verify_ssl: False
      tower_user: "admin"
      tower_pass: "{{ my_tower_vault_pass }}"
      tower_org: "MY_ORG"
      tower_cred_name: "doG"
      tower_cred_user: "root"
      tower_cred_pass: "{{ my_cred_vault_pass }}"
      tower_cred_desc: "High-level special account for doing Ansible work"
      tower_cred_type: "ssh"
      tower_cred_ssh_key_path: "/home/myuser/.ssh/id_rsa"
      tower_cred_ssh_key_pass: "{{ my_cred_vaulted_ssh_key_pass }}"
```
### Included Role within a Loop
```yaml
---
- hosts: all
  vars:
    tower_url: "https://my-tower-server.foo.bar"
    tower_verify_ssl: False
    tower_user: "admin"
    tower_pass: "{{ my_tower_vault_pass }}"
    tower_org: "MY_ORG"
    my_cred_loop_var:
      - name: "doG"
        tower_cred_user: "root"
        tower_cred_pass: "{{ my_cred_vault_pass }}"
        tower_cred_desc: "High-level special account for doing Ansible work"
        tower_cred_type: "ssh"
        tower_cred_ssh_key_path: "/home/myuser/.ssh/id_rsa"
        tower_cred_ssh_key_pass: "{{ my_cred_vaulted_ssh_key_pass }}"
      - name: "My Special Project's Vault"
        tower_cred_vault_pass: "{{ my_vaulted_vault_pass }}"
        tower_cred_desc: "A vault password for the cool project that deploys stuff to production."
        tower_cred_type: "vault"
  tasks:
    - name: "Create a bunch of credentials in Ansible Tower"
      include_role:
        name: "genie-credentials"
      vars:
        tower_cred_name: "{{ cred.name }}"
        tower_cred_user: "{{ cred.tower_cred_user }}"
        tower_cred_pass: "{{ cred.tower_cred_pass }}"
        tower_cred_vault_pass: "{{ cred.tower_cred_vault_pass }}"
        tower_cred_desc: "{{ cred.tower_cred_desc }}"
        tower_cred_type: "{{ cred.tower_cred_type }}"
        tower_cred_ssh_key_path: "{{ cred.tower_cred_ssh_key_path }}"
        tower_cred_ssh_key_pass: "{{ cred.tower_cred_ssh_key_pass }}"
      with_items: "{{ my_cred_loop_var }}"
      loop_control:
        loop_var: "cred"
        label: "{{ cred.name }}"
      no_log: True #if you don't use this your passwords could be exposed to standard out
```
## License
[MIT](LICENSE)

## Author  
[Andrew J. Huffman](https://github.com/ahuffman)  
