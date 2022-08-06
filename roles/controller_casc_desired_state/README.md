controller_configuration.casc_desired_state
=========

An ansible role to manage the desired state of the AWX or Automation Controller configuration. This role leverage the controller_object_diff.py lookup plugin of the redhat_cop.controller_configuration, comparing two lists, one taken directly from the API and the other one from the git repository, that was previosly created and implemented for the controller_configuration.casc_implementation, and deletes the objects in the AWX or Automation Controller that are not defined in the git repository list.


Requirements
------------

ansible-galaxy collection install -r tests/collections/requirements.yml to be installed Currently: awx.awx or ansible.controller and redhat_cop.controller_configuration.

Role Variables
--------------

### Organization and Environment Variables
The following Variables set the organization where should be applied the configuration, the absolute or relative of the directory structure where the variables will be stored and the life-cycle enviroment to use.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`orgs:`|Acme|yes|This variable sets the organization where should be applied the configuration.|
|`dir_orgs_vars:`|orgs_vars|yes|This variable sets the directory path where the variables will be store.|
|`env:`|dev|yes|This variable sets the life-cycle enviroment to use.|

Role Tags
----------------

The role is designed to be used with tags, each tags correspond to an AWX or Automation Controller object to be managed by ansible.

```bash
$ ansible-playbook desired-state.yml --list-tags
      TASK TAGS: [desired_state, desired_state_credentials, desired_state_groups, desired_state_hosts, desired_state_inventories, desired_state_inventory_sources, desired_state_job_templates, desired_state_organizations, desired_state_projects, desired_state_teams, desired_state_user_accounts, desired_state_workflow_job_template_nodes, desired_state_workflow_job_templates]
```

Example Playbook
----------------
---
- hosts: controller
  connection: local
  gather_facts: false
  collections:
    - ansible.controller
    - redhat_cop.controller_configuration
  roles:
    - controller_casc_desired_state

```bash
$ ansible-playbook config-controller.yml --tags desired_state_${CONTROLLER_OBJECT} -e "{orgs: ${ORGANIZATION}, dir_orgs_vars: orgs_vars, env: ${ENVIRONMENT} }" --vault-password-file ./.vault_pass.txt -e @orgs_vars/env/${ENVIRONMENT}/configure_connection_controller_credentials.yml ${OTHER}

```

License
-------

GPLv3+

Author Information
------------------

- silvinux
  - email: <silvio@redhat.com>
  - github: https://github.com/silvinux

ToDo
------------------
- desired_state_roles
- Issue: Due to the Team Object doesn't return any field related to external account on Controller API, which help to filter if the teams comes from an External Source and not to be deleted by the Desired State Ansible automation process.
