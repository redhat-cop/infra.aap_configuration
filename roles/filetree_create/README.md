controller_configuration.filetree_create
=========

The role `filetree_create` is intended to be used as the first step to begin using the Configuration as Code on Ansible Tower or Ansible Automation Platform, when you already have a running instance of any of them. Obviously, you also could start to write your objects as code from scratch, but the idea behind the creation of that role is to simplify your lives and make that task a little bit easier.

Requirements
------------

That role requires the following:

- [awx.awx](https://docs.ansible.com/ansible/latest/collections/awx/awx/index.html) or [ansible.controller]ansible collection.

Role Variables
--------------

The following variables are required for that role to work properly:

| Variable Name | Default Value | Required | Description |
| :------------ | :-----------: | :------: | :---------- |
| `controller_api_plugin` | `ansible.controller` | yes | Full path for the controller_api_plugin to be used. <br/> Can have two possible values: <br/>&nbsp;&nbsp;- awx.awx.controller_api             # For the community Collection version <br/>&nbsp;&nbsp;- ansible.controller.controller_api  # For the Red Hat Certified Collection version|
| `output_path` | `/tmp/filetree_output` | yes | The path to the output directory where all the generated `yaml` files with the corresponding Objects as code will be written to. |

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
