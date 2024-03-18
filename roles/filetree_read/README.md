# controller_configuration.filetree_read

An ansible role which reads variables from a hierarchical and scalable directory structure which is grouped based on the configuration code life-cycle. It could be used to run the role filetree_read to load variables followed by dispatch role to apply the configuration.

## Requirements

This role requires the [awx.awx](https://docs.ansible.com/ansible/latest/collections/awx/awx/index.html) or [ansible.controller](https://console.redhat.com/ansible/automation-hub/repo/published/ansible/controller) Ansible collection.

## Role Variables

### Organization and Environment Variables

The following Variables set the organization where should be applied the configuration, the absolute or relative of the directory structure where the variables will be stored and the life-cycle environment to use.

|Variable Name|Type|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|:---:|
|`orgs`|String|N/A|yes|This variable sets the organization where should be applied the configuration.|
|`dir_orgs_vars`|String|N/A|yes|This variable sets the directory path where the variables will be store.|
|`env:`|String|dev|no|This variable sets the life-cycle environment to use.|
|`controller_location`|String|''|no|This variable sets object localtion. It is useful when the configuration need to be replicated in an active/passive sites architecture|
|`filetree_controller_settings`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/{{ env }}/controller_settings.d/|no|Directory path to load controller object variables|
|`filetree_controller_organizations`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_organizations.d/|no|Directory path to load controller object variables|
|`filetree_controller_labels`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_labels.d/|no|Directory path to load controller object variables|
|`filetree_controller_user_accounts`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/{{ env }}/controller_users.d/|no|Directory path to load controller object variables|
|`filetree_controller_teams`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_teams.d/|no|Directory path to load controller object variables|
|`filetree_controller_credential_types`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_credential_types.d/|no|Directory path to load controller object variables|
|`filetree_controller_credentials`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/{{ env }}/controller_credentials.d/|no|Directory path to load controller object variables|
|`filetree_controller_credential_input_sources`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_credential_input_sources.d/|no|Directory path to load controller object variables|
|`filetree_controller_notifications`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_notification_templates.d/|no|Directory path to load controller object variables|
|`filetree_controller_projects`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_projects.d/|no|Directory path to load controller object variables|
|`filetree_controller_execution_environments`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/{{ env }}/controller_execution_environments.d/|no|Directory path to load controller object variables|
|`filetree_controller_applications`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_applications.d/|no|Directory path to load controller object variables|
|`filetree_controller_inventories`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_inventories.d/|no|Directory path to load controller object variables|
|`filetree_controller_inventory_sources`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/{{ env }}/controller_inventory_sources.d/|no|Directory path to load controller object variables|
|`filetree_controller_instance_groups`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/{{ env }}/controller_instance_groups.d/|no|Directory path to load controller object variables|
|`filetree_controller_hosts`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/{{ env }}/controller_hosts.d/|no|Directory path to load controller object variables|
|`filetree_controller_groups`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_groups.d/|no|Directory path to load controller object variables|
|`filetree_controller_templates`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_job_templates.d/|no|Directory path to load controller object variables|
|`filetree_controller_workflow_job_templates`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_workflow_job_templates.d/|no|Directory path to load controller object variables|
|`filetree_controller_schedules`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_schedules.d/|no|Directory path to load controller object variables|
|`filetree_controller_roles`|String/List(String)|{{ dir_orgs_vars }}/{{ orgs }}/env/common/controller_roles.d/|no|Directory path to load controller object variables|

### Data Structure

- It accepts two data models as the roles in the infra.controller_configuration collection,a simple straightforward easy to maintain model, and another based on the controller api.
- Variables should be stored in yaml files. It could be used vault to encrypt sensitive data when needed.
- All variables should be taken from the awx or automation controller object roles from the infra.controller_configuration collection.

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

### Directory and Variables Data Structure for Authentication (Optional)

- It could be created in the following path encrypted variables to be loaded to authenticate against the different controllers.

```bash
 tree -L 5 orgs_vars/env/
orgs_vars/env/
├── demo-dev
│   └── configure_connection_controller_credentials.yml
└── demo-prd
    └── configure_connection_controller_credentials.yml

$ $ ansible-vault view orgs_vars/env/demo-dev/configure_connection_controller_credentials.yml
Vault password:
---
vault_controller_username: 'ldap-admin-org1'
vault_controller_password: 'password'
vault_controller_hostname: controller-dev.lab.example.com
vault_controller_validate_certs: false
...

```

### Directory and Variables Data Structure

- A directory structure should be created to store the variables files as below:

```bash
orgs_vars/Organization1
└── env
    ├── common
    │   ├── controller_credential_types.d
    │   │   ├── app-example
    │   │   │   ├── controller_credential_types_aap_monitor.yml
    │   │   │   ├── controller_credential_types_acme_key.yml
    │   │   │   ├── controller_credential_types_cloudforms.yml
    │   │   │   ├── controller_credential_types_multiple.yml
    │   │   │   └── controller_credential_types_servicenow.yml
    │   │   └── controller_credential_types.yml
    │   ├── controller_groups.d
    │   │   └── controller_groups.yml
    │   ├── controller_inventories.d
    │   │   ├── app-casc
    │   │   │   └── controller_inventories_localhost.yml
    │   │   ├── app-example
    │   │   │   ├── controller_inventories_excel.yml
    │   │   │   ├── controller_inventories_smart_org1.yml
    │   │   │   └── controller_inventories_smart_org2.yml
    │   │   └── controller_inventories.yml
    │   ├── controller_job_templates.d
    │   │   ├── app-casc
    │   │   │   └── controller_job_templates_casc.yml
    │   │   ├── app-example
    │   │   │   ├── controller_job_templates_container_groups.yml
    │   │   │   ├── controller_job_templates_crossteams.yml
    │   │   │   └── controller_job_templates_demo_push.yml
    │   │   └── controller_job_templates.yml
    │   ├── controller_organizations.d
    │   │   ├── app-casc
    │   │   │   └── controller_organizations_Global.yml
    │   │   ├── app-example
    │   │   │   ├── controller_organizations_ExampleOrg.yml
    │   │   │   ├── controller_organizations_Organizations1-2.yml
    │   │   │   └── controller_organizations_OrgCrossTeams.yml
    │   │   └── controller_organizations.yml
    │   ├── controller_projects.d
    │   │   ├── app-casc
    │   │   │   └── controller_projects_casc.yml
    │   │   ├── app-ocp
    │   │   │   └── controller_projects_container_groups.yml
    │   │   ├── controller_projects.yml
    │   │   └── inventories
    │   │       ├── controller_projects_inventory_sourcea_dev.yml
    │   │       ├── controller_projects_inventory_sourcea_prod.yml
    │   │       ├── controller_projects_inventory_sourceb_dev.yml
    │   │       └── controller_projects_inventory_sourceb_prod.yml
    │   ├── controller_roles.d                                  (1)
    │   │   ├── app-example                                     (1)
    │   │   │   ├── controller_roles_cmdb_approvals.yml         (1)
    │   │   │   ├── controller_roles_inventories.yml            (1)
    │   │   │   ├── controller_roles_inventory_wf_update.yml    (1)
    │   │   │   ├── controller_roles_teams.yml                  (1)
    │   │   │   └── controller_roles_users.yml                  (1)
    │   │   └── controller_roles.yml                            (1)
    │   ├── controller_schedules.d
    │   │   ├── app-casc
    │   │   │   └── controller_schedules_casc.yml
    │   │   ├── app-example
    │   │   │   └── controller_schedules_example.yml
    │   │   └── controller_schedules.yml
    │   ├── controller_teams.d
    │   │   ├── app-demo
    │   │   │   ├── controller_teams_org1.yml
    │   │   │   └── controller_teams_org2.yml
    │   │   └── controller_teams.yml
    │   └── controller_workflow_job_templates.d
    │       ├── app-casc
    │       │   └── controller_workflow_job_templates_casc.yml
    │       ├── app-examples
    │       │   └── controller_workflow_job_templates_InventoryUpdate.yml
    │       └── controller_workflow_job_templates.yml
    ├── demo-dev
    │   ├── controller_credentials.d
    │   │   ├── app-examples
    │   │   │   ├── controller_credentials_aap.yml
    │   │   │   ├── controller_credentials_galaxy.yml
    │   │   │   ├── controller_credentials_machine.yml
    │   │   │   ├── controller_credentials_ocp.yml
    │   │   │   ├── controller_credentials_registry.yml
    │   │   │   ├── controller_credentials_scm.yml
    │   │   │   └── controller_credentials_vault.yml
    │   │   ├── controller_credentials_aap.yml
    │   │   ├── controller_credentials_galaxy.yml
    │   │   ├── controller_credentials_machine.yml
    │   │   ├── controller_credentials_ocp.yml
    │   │   ├── controller_credentials_registry.yml
    │   │   ├── controller_credentials_scm.yml
    │   │   └── controller_credentials_vault.yml
    │   ├── controller_execution_environments.d
    │   │   ├── app-casc
    │   │   │   └── controller_execution_environments_ee-casc.yml
    │   │   ├── app-examples
    │   │   │   └── controller_execution_environments_ee-xlsx.yml
    │   │   └── controller_execution_environments.yml
    │   ├── controller_hosts.d
    │   │   ├── app-casc
    │   │   │   └── controller_hosts_localhost.yml
    │   │   └── controller_hosts.yml
    │   ├── controller_instance_groups.d
    │   │   ├── app-example
    │   │   │   └── controller_instance_groups_otlc.yml
    │   │   └── controller_instance_groups.yml
    │   ├── controller_users.d
    │   │   ├── app-demo
    │   │   │   ├── controller_user_accounts_org1.yml
    │   │   │   └── controller_user_accounts_org2.yml
    │   │   └── controller_user_accounts.yml
    │   ├── controller_inventory_sources.d
    │   │   ├── app-examples
    │   │   │   ├── controller_inventory_sources_sourcea_dev.yml
    │   │   │   ├── controller_inventory_sources_sourcea_prod.yml
    │   │   │   ├── controller_inventory_sources_sourceb_dev.yml
    │   │   │   └── controller_inventory_sources_sourceb_prod.yml
    │   │   └── controller_inventory_sources.yml
    │   └── controller_settings.d                               (2)
    │       ├── app-examples                                    (2)
    │       │   ├── controller_settings_jobs.yml                (2)
    │       │   ├── controller_settings_ldap.yml                (2)
    │       │   ├── controller_settings_system.yml              (2)
    │       │   └── controller_settings_user_interface.yml      (2)
    │       └── controller_settings.yml                         (2)
    └── demo-prd
        ├── controller_credentials.d
        │   ├── app-examples
        │   │   ├── controller_credentials_aap.yml
        │   │   ├── controller_credentials_galaxy.yml
        │   │   ├── controller_credentials_machine.yml
        │   │   ├── controller_credentials_ocp.yml
        │   │   ├── controller_credentials_registry.yml
        │   │   ├── controller_credentials_scm.yml
        │   │   └── controller_credentials_vault.yml
        │   ├── controller_credentials_aap.yml
        │   ├── controller_credentials_galaxy.yml
        │   ├── controller_credentials_machine.yml
        │   ├── controller_credentials_ocp.yml
        │   ├── controller_credentials_registry.yml
        │   ├── controller_credentials_scm.yml
        │   └── controller_credentials_vault.yml
        ├── controller_execution_environments.d
        │   ├── app-casc
        │   │   └── controller_execution_environments_ee-casc.yml
        │   ├── app-examples
        │   │   └── controller_execution_environments_ee-xlsx.yml
        │   └── controller_execution_environments.yml
        ├── controller_hosts.d
        │   └── controller_hosts.ym
        ├── controller_instance_groups.d
        │   ├── app-example
        │   │   └── controller_instance_groups_otlc.yml
        │   └── controller_instance_groups.yml
        ├── controller_users.d
        │   ├── app-demo
        │   │   ├── controller_user_accounts_org1.yml
        │   │   └── controller_user_accounts_org2.yml
        │   └── controller_user_accounts.yml
        ├── controller_inventory_sources.d
        │   ├── app-examples
        │   │   ├── controller_inventory_sources_sourcea_dev.yml
        │   │   ├── controller_inventory_sources_sourcea_prod.yml
        │   │   ├── controller_inventory_sources_sourceb_dev.yml
        │   │   └── controller_inventory_sources_sourceb_prod.yml
        │   └── controller_inventory_sources.yml
        └── controller_settings.d                               (2)
            ├── app-examples                                    (2)
            │   ├── controller_settings_jobs.yml                (2)
            │   ├── controller_settings_ldap.yml                (2)
            │   ├── controller_settings_system.yml              (2)
            │   └── controller_settings_user_interface.yml      (2)
            └── controller_settings.yml                         (2)
```

> **NOTE (1):** These directory and files may belong to SuperAdmin Organization ONLY. If any other organization defines it's own `roles`, they must duplicate the ones given by the SuperAdmin Organization or they will be dropped.
>
> **NOTE (2):** These directories and files must belong to SuperAdmin Organization ONLY, because must have admin super powers.

## Role Tags

The role is designed to be used with tags, each tags correspond to an AWX or Automation Controller object to be managed by ansible.

```bash
[ansible@demo-ctr1-dev global]$  ansible-playbook config-controller-filetree.yml --list-tags
  play #1 (localhost): localhost TAGS: []
      TASK TAGS: [always, applications, credential_input_sources, credential_types, credentials, execution_environments, groups, hosts, instance_groups, inventories, inventory_sources, job_templates, labels, notifications, notifications_templates, organizations, projects, roles, schedules, settings, teams, users, workflow_job_templates]
```

## Example Playbook

```yaml
---
- hosts: all
  connection: local
  gather_facts: false
  vars:
    controller_configuration_projects_async_retries: 60
    controller_configuration_projects_async_delay: 2
    controller_username: "{{ vault_controller_username | default(lookup('env', 'CONTROLLER_USERNAME')) }}"
    controller_password: "{{ vault_controller_password | default(lookup('env', 'CONTROLLER_PASSWORD')) }}"
    controller_hostname: "{{ vault_controller_hostname | default(lookup('env', 'CONTROLLER_HOST')) }}"
    controller_validate_certs: "{{ vault_controller_validate_certs | default(lookup('env', 'CONTROLLER_VERIFY_SSL')) }}"

  pre_tasks:
    - name: "Setup authentication (block)"
      block:
        - name: "Get the Authentication Token for the future requests"
          ansible.builtin.uri:
            url: "https://{{ controller_hostname }}/api/v2/tokens/"
            user: "{{ controller_username }}"
            password: "{{ controller_password }}"
            method: POST
            force_basic_auth: true
            validate_certs: "{{ controller_validate_certs }}"
            status_code: 201
          register: authtoken_res

        - name: "Set the oauth token to be used since now"
          ansible.builtin.set_fact:
            controller_oauthtoken: "{{ authtoken_res.json.token }}"
            controller_oauthtoken_url: "{{ authtoken_res.json.url }}"
          no_log: true
      when: controller_oauthtoken is not defined
      tags:
        - always

    - block:
        - name: Include Tasks to load Galaxy credentials to be added to Organizations
          ansible.builtin.include_role:
            name: infra.controller_configuration.filetree_read
            tasks_from: "{{ create_orgs_credentials }}"
          loop:
            - organizations.yml
            - credentials.yml
          loop_control:
            loop_var: create_orgs_credentials

        - name: Include Tasks to add Galaxy credentials to Organizations
          ansible.builtin.include_role:
            name: infra.controller_configuration.dispatch
            apply:
              tags:
                - organizations
                - credentials
          vars:
            assign_galaxy_credentials_to_org: false
            controller_configuration_dispatcher_roles:
              - {role: organizations, var: controller_organizations, tags: organizations}
              - {role: credentials, var: controller_credentials, tags: credentials}

  roles:
    - {role: infra.controller_configuration.filetree_read }
    - {role: infra.controller_configuration.dispatch }

  post_tasks:
    - name: "Delete the Authentication Token used"
      ansible.builtin.uri:
        url: "https://{{ controller_hostname }}{{ controller_oauthtoken_url }}"
        user: "{{ controller_username }}"
        password: "{{ controller_password }}"
        method: DELETE
        force_basic_auth: true
        validate_certs: "{{ controller_validate_certs }}"
        status_code: 204
      when: controller_oauthtoken_url is defined
...

```

```bash
ansible-playbook config-controller-filetree.yml --tags ${CONTROLLER_OBJECT} -e "{orgs: ${ORGANIZATION}, dir_orgs_vars: orgs_vars, env: ${ENVIRONMENT} }" --vault-password-file ./.vault_pass.txt -e @orgs_vars/env/${ENVIRONMENT}/configure_connection_controller_credentials.yml

```

## License

GPLv3+

## Author Information

- [Silvio Perez](https://github.com/silvinux)
