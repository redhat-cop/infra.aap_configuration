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

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|**`output_path`**|"/tmp/filetree_output"|no|The path to the output directory where all the generated `yaml` files with the corresponding Objects as code will be written to.
|**`query_controller_api_max_objects`**|"10000"|no|Maximum number of objects to return from the list. If a list view returns more an max_objects an exception will be raised|


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
