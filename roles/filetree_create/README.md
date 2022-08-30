controller_configuration.filetree_create
=========

The role `filetree_create` is intended to be used as the first step to begin using the Configuration as Code on Ansible Tower or Ansible Automation Platform, when you already have a running instance of any of them. Obviously, you also could start to write your objects as code from scratch, but the idea behind the creation of that role is to simplify your lives and make that task a little bit easier.

Requirements
------------

That role requires the following:

- [awx.awx](https://docs.ansible.com/ansible/latest/collections/awx/awx/index.html) or [ansible.controller]ansible collection.
- [Community.General](https://docs.ansible.com/ansible/latest/collections/community/general/index.html#plugins-in-community-general)
- jmespath library needs to be installed on the host running the playbook (needed for the json_query filter)

```bash
$ ansible-galaxy collection install community.general -p collections
$ ansible-galaxy collection install ansible.controller -p collections
$ pip3 install jmespath
```

Role Variables
--------------

The following variables are required for that role to work properly:

- **`output_path`**: The path to the output directory where all the generated `yaml` files with the corresponding Objects as code will be written to. The default path is `/tmp/filetree_output`.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

```yaml
---
- hosts: localhost
  connection: local
  gather_facts: false
  vars:
    controller_hostname: "{{ vault_controller_hostname }}"
    controller_username: "{{ vault_controller_username }}"
    controller_password: "{{ vault_controller_password }}"
    controller_validate_certs: "{{ vault_controller_validate_certs }}"
  pre_tasks:
    - name: "Check if the required input variables are present"
      assert:
        that:
          - input_tag is defined
          - (input_tag | type_debug) == 'list'
        fail_msg: 'A variable called ''input_tag'' of type ''list'' is needed: -e ''{input_tag: [organizations, projects]}'''
        quiet: true

    - name: "Check if the required input values are correct"
      assert:
        that:
          - tag_item in valid_tags
        fail_msg: "The valid tags are the following ones: {{ valid_tags | join(', ') }}"
        quiet: true
      loop: "{{ input_tag }}"
      loop_control:
        loop_var: tag_item
  roles:
    - redhat_cop.controller_configuration.filetree_create
...
```

License
-------

GPLv3+

Author Information
------------------

- Ivan Aragonés:
  - email: <iaragone@redhat.com>
  - github: https://github.com/ivarmu
