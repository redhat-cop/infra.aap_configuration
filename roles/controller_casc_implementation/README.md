controller_configuration.controller_casc_implementation
=========

An ansible role which implements the roles of the awx o automation controller objects from the redhat_cop.controller_configuration collection using a hierarchical and scalable directory structure which is grouped based on the configuration code life-cycle. Addionally, is possible to leverage the gitlab or github webhook sender and the Automation Controller webhook receiver to create a pipeline to apply the configuration which will be triggered when changes has been made in a git repository.


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


### Data Structure

- It accepts two data models as the roles in the redhat_cop.controller_configuration collection,a simple straightforward easy to maintain model, and another based on the controller api.
- Variables should be stored in yaml files. It could be used vault to encrypt sensitive data when needed.
- All variables should be taken from the awx or automation controller object roles from the redhat_cop.controller_configuration collection.

```yaml
---
controller_templates:
  - name: "{{ orgs }} JT_Container_Group TEST DEMO First Push"
    description: "Template to  test Container Groups"
    organization: "{{ orgs }}"
    project: "{{ orgs }} Demo Push"
    inventory: "Global Localhost"
    playbook: "dummy-playbooks.yml"
    job_type: run
    concurrent_jobs_enabled: true
    credentials:
      - "{{ orgs }} {{ env }} aap_vault_credentials"
    execution_environment: "Default execution environment"
...
```

### Directory  and Variables Data Structure
- A directory structure should be created to store the variables files as below:

```bash
orgs_vars/Organization1/
└── env
    ├── common
    │   ├── controller_credential_types.d
    │   ├── controller_groups.d
    │   ├── controller_instance_groups.d
    │   ├── controller_inventories.d
    │   │   └── controller_inventories.yml
    │   ├── controller_job_templates.d
    │   │   ├── app-casc
    │   │   │   └── controller_job_templates_casc.yml
    │   │   ├── app-example
    │   │   │   ├── controller_job_templates_demo_push.yml
    │   │   │   └── controller_job_templates_gather_facts.yml
    │   │   └── controller_job_templates.yml
    │   ├── controller_organizations.d
    │   │   └── controller_organizations.yml
    │   ├── controller_projects.d
    │   │   ├── app-casc
    │   │   │   └── controller_projects_casc.yml
    │   │   ├── app-example
    │   │   │   └── controller_projects.yml
    │   │   └── controller_projects.yml
    │   ├── controller_roles.d
    │   │   ├── app-example
    │   │   │   ├── controller_roles_credentials.yml
    │   │   │   ├── controller_roles_devs.yml
    │   │   │   └── controller_roles_gatherfacts.yml
    │   │   └── controller_roles.yml
    │   ├── controller_schedules.d
    │   │   ├── app-casc
    │   │   │   └── controller_schedules_casc.yml
    │   │   └── controller_schedules.yml
    │   ├── controller_teams.d
    │   │   └── controller_teams.yml
    │   ├── controller_users.d
    │   │   └── controller_user_accounts.yml
    │   └── controller_workflow_job_templates.d
    │       ├── app-casc
    │       │   └── controller_workflow_job_templates_casc.yml
    │       ├── app-examples
    │       │   └── controller_workflow_job_templates_example.yml
    │       └── controller_workflow_job_templates.yml
    ├── dev
    │   ├── controller_credentials.d
    │   │   ├── controller_credentials_aap.yml
    │   │   ├── controller_credentials_machine.yml
    │   │   ├── controller_credentials_ocp.yml
    │   │   ├── controller_credentials_registry.yml
    │   │   ├── controller_credentials_scm.yml
    │   │   └── controller_credentials_vault.yml
    │   ├── controller_execution_environments.d
    │   │   └── controller_execution_environments.yml
    │   ├── controller_hosts.d
    │   │   └── controller_hosts.yml
    │   ├── controller_inventory_sources.d
    │   │   └── controller_inventory_sources.yml
    │   └── controller_settings.d
    │       └── controller_settings.yml
    └── prod
        ├── controller_credentials.d
        │   ├── controller_credentials_aap.yml
        │   ├── controller_credentials_galaxy.yml
        │   ├── controller_credentials_machine.yml
        │   ├── controller_credentials_ocp.yml
        │   ├── controller_credentials_registry.yml
        │   ├── controller_credentials_scm.yml
        │   └── controller_credentials_vault.yml
        ├── controller_execution_environments.d
        │   └── controller_execution_environments.yml
        ├── controller_hosts.d
        │   └── controller_hosts.yml
        ├── controller_inventory_sources.d
        │   └── controller_inventory_sources.yml
        └── controller_settings.d
            └── controller_settings.yml
```


Role Tags
----------------

The role is designed to be used with tags, each tags correspond to an AWX or Automation Controller object to be managed by ansible.

```bash
$ ansible-playbook config-controller.yml --list-tags
      TASK TAGS: [ad_hoc_command, ad_hoc_command_cancel, applications, ci_webhook_trigger, credential_input_sources, credential_types, credentials, execution_environments, groups, hosts, instance_groups, inventories, inventory_source_update, inventory_sources, job_launch, job_templates, jobs_cancel, labels, license, notifications, organizations, project_update, projects, roles, schedules, settings, teams, users, workflow_job_templates, workflow_launch]
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
    - controller_casc_implementation

```bash
$ ansible-playbook config-controller.yml --tags ${CONTROLLER_OBJECT} -e "{orgs: ${ORGANIZATION}, dir_orgs_vars: orgs_vars, env: ${ENVIRONMENT} }" --vault-password-file ./.vault_pass.txt -e @orgs_vars/env/${ENVIRONMENT}/configure_connection_controller_credentials.yml ${OTHER}

```

License
-------

GPLv3+

Author Information
------------------

- silvinux
  - email: <silvio@redhat.com>
  - github: https://github.com/silvinux
