# Work In Progress
# ansible_tower_genie_inventories
An Ansible role to create inventories and inventory sources.


## Variables
| Variable Name | Default Value | Required | Description | Type |
|---|---|:---:|---|:---:|
|`tower_url`|""|yes|URL to the Ansible Tower Server.| string |
|`tower_verify_ssl`|False|no|Whether or not to validate the Ansible Tower Server's SSL certificate.| boolean |
|`tower_secrets`|False|yes|Whether or not to include variables stored in vars/tower-secrets.yml.  Set this value to `False` if you will be providing your sensitive values from elsewhere.| boolean |
|`tower_user`|""|yes|Admin User on the Ansible Tower Server.| boolean |
|`tower_pass`|""|yes|Tower Admin User's password on the Ansible Tower Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.| boolean |

# License
[MIT](LICENSE)

# Author
[Edward Quail](mailto:equail@redhat.com)  
[Andrew J. Huffman](https://github.com/ahuffman)
