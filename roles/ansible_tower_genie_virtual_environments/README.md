# ansible_tower_genie_virtual_environments

## Description
An Ansible Role to manage Python virtual environments in Ansible Tower.

## Variables
|Variable Name|Default Value|Required|Description|Type|
|---|:---:|:---:|---|:---:|
|tower_venv_pylibs | ["ansible-tower-cli"] | yes | List of Python libraries to install from pip.  This should be a list of Python libraries that certain Ansible modules require to run. If just the package name is provided (i.e. without [package-name]-[version] **example:** *`ansible-tower-cli-3.3.2`*) the latest version will be installed (**example:** *`ansible-tower-cli`* will get latest version available). | list |
| tower_venv_path | "/var/lib/awx/venv/ansible" | no | Path to the Ansible Tower virtual environment you would like to operate on. If the path does not exist, the directory, along with the required Ansible Tower base depencenies (`python-memcached psutil`).| string |
| tower_venv_umask | "0022" | no | System umask to apply before installing the pip package. | string |

## Playbook Examples
### Standard Role Usage
```yaml
---
- hosts: "all"
  roles:
    - role: "ansible_tower_genie_virtual_environments"
      tower_venv_pylibs:
        - "ansible-tower-cli"
        - "boto"
```
### Imported Role
```yaml
---
- hosts: "all"
  vars:
    tower_venv_pylibs:
      - "ansible-tower-cli"
      - "boto"
  tasks:
    - name: "Ensure Ansible Prerequisites are installed"
      import_role:
        name: "ansible_tower_genie_virtual_environments"
```
### Included Role
```yaml
---
- hosts: "all"
  tasks:
    - name: "Ensure Ansible Prerequisites are installed"
      include_role:
        name: "ansible_tower_genie_virtual_environments"
      vars:
        tower_venv_pylibs:
          - "ansible-tower-cli"
          - "boto"
```
## License
[MIT](LICENSE)

## Author
[Andrew J. Huffman](https://github.com/ahuffman)
