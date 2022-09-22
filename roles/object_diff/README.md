controller_configuration.object_diff
=========

An ansible role to manage the object diff of the AWX or Automation Controller configuration. This role leverage the controller_object_diff.py lookup plugin of the redhat_cop.controller_configuration, comparing two lists, one taken directly from the API and the other one from the git repository, and it could be used to delete objects in the AWX or Automation Controller that are not defined in the git repository list.


Requirements
------------

`ansible-galaxy collection install -r tests/collections/requirements.yml` to be installed. Currently: `awx.awx` or `ansible.controller` and `redhat_cop.controller_configuration`.

Role Variables
--------------

### Organization and Environment Variables
The following Variables set the organization where should be applied the configuration, the absolute or relative of the directory structure where the variables will be stored and the life-cycle enviroment to use.

| Variable Name | Default Value | Required | Description |
| :------------ | :-----------: | :------: | :---------- |
| `controller_api_plugin` | `ansible.controller` | yes | Full path for the controller_api_plugin to be used. <br/> Can have two possible values: <br/>&nbsp;&nbsp;- awx.awx.controller_api             # For the community Collection version <br/>&nbsp;&nbsp;- ansible.controller.controller_api  # For the Red Hat Certified Collection version|
| `drop_user_external_accounts` | `False` | no | When is true, all users will be taken to compare with SCM configuration as code |
| `drop_teams` | `False` | no | When is true, all teams will be taken to compare with SCM configuration as code |

Role Tags
----------------

The role is designed to be used with tags, each tags correspond to an AWX or Automation Controller object to be managed by ansible.

> :warning: List of object type managed by this role: credentials, credential_types, groups, hosts, inventories, inventory_sources, job_templates, organizations, projects, teams, users, workflow_job_templates.

```bash
$ ansible-playbook object_diff.yml --list-tags
      TASK TAGS: [credentials, credential_types, groups, hosts, inventories, inventory_sources, job_templates, organizations, projects, teams, users, workflow_job_templates]

```

Example Playbook
----------------

```bash
---
- hosts: localhost
  connection: local
  gather_facts: false
  roles:
    - role: redhat_cop.controller_configuration.filetree_read
    - role: redhat_cop.controller_configuration.object_diff
    - role: redhat_cop.controller_configuration.dispatch
      vars:
        controller_configuration_dispatcher_roles:
          - {role: workflow_job_templates, var: controller_workflows, tags: workflow_job_templates}
          - {role: job_templates, var: controller_templates, tags: job_templates}
          - {role: teams, var: controller_teams, tags: teams}
          - {role: users, var: controller_user_accounts, tags: users}
          - {role: groups, var: controller_groups, tags: inventories}
          - {role: hosts, var: controller_hosts, tags: hosts}
          - {role: inventory_sources, var: controller_inventory_sources, tags: inventory_sources}
          - {role: inventories, var: controller_inventories, tags: inventories}
          - {role: projects, var: controller_projects, tags: projects}
          - {role: credentials, var: controller_credentials, tags: credentials}
          - {role: credential_types, var: controller_credential_types, tags: credential_types}
          - {role: organizations, var: controller_organizations, tags: organizations}

$ ansible-playbook drop_diff.yml --tags ${CONTROLLER_OBJECT} -e "{orgs: ${ORGANIZATION}, dir_orgs_vars: orgs_vars, env: ${ENVIRONMENT} }" --vault-password-file ./.vault_pass.txt -e @orgs_vars/env/${ENVIRONMENT}/configure_connection_controller_credentials.yml ${OTHER}
```

License
-------

GPLv3+

Author Information
------------------

- silvinux
  - email: <silvio@redhat.com>
  - github: https://github.com/silvinux

- Ivan Aragonés:
  - email: <iaragone@redhat.com>
  - github: https://github.com/ivarmu

Important things to take into account
-------------------------------------
- Issues:
  - Users and Teams must be managed by users with privileges.
  - Due to the Team Object doesn't return from API any field related to external account on Controller API, which help to filter if the teams comes from an External Source and not to be deleted by the Object Diff Ansible automation process.
