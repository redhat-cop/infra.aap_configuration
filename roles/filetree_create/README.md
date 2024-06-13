# controller_configuration.filetree_create

The role `filetree_create` is intended to be used as the first step to begin using the Configuration as Code on Ansible Tower or Ansible Automation Platform, when you already have a running instance of any of them. Obviously, you also could start to write your objects as code from scratch, but the idea behind the creation of that role is to simplify your lives and make that task a little bit easier.

## Requirements

This role requires the [awx.awx](https://docs.ansible.com/ansible/latest/collections/awx/awx/index.html) or [ansible.controller](https://console.redhat.com/ansible/automation-hub/repo/published/ansible/controller) ansible collection.

## Role Variables

The following variables are required for that role to work properly:

| Variable Name | Default Value | Required | Type | Description |
| :------------ | :-----------: | :------: | :------: | :---------- |
| `controller_api_plugin` | `ansible.controller` | yes | str | Full path for the controller_api_plugin to be used. <br/> Can have two possible values: <br/>&nbsp;&nbsp;- awx.awx.controller_api             # For the community Collection version <br/>&nbsp;&nbsp;- ansible.controller.controller_api  # For the Red Hat Certified Collection version|
| `organization_filter` | N/A | no | str | Exports only the objects belonging to the specified organization (applies to all the objects that can be assigned to an organization). |
| `organization_id` | N/A | no | int | Alternative to `organization_filter`, but specifiying the current organization's ID to filter by. Exports only the objects belonging to the specified organization (applies to all the objects that can be assigned to an organization). |
| `project_id` | N/A | no | int | Specifiying the project id to filter by. Exports the project belonging to the specified organization. |
| `job_template_id` | N/A | no | int | Specifiying the job template id to filter by. Exports the job template belonging to the specified organization. |
| `workflow_job_template_id` | N/A | no | int | Specifiying the workflow job template id to filter by. Exports the workflow job template belonging to the specified organization. |
| `output_path` | `/tmp/filetree_output` | yes | str | The path to the output directory where all the generated `yaml` files with the corresponding Objects as code will be written to. |
| `input_tag` | `['all']` | no | List of Strings | The tags which are applied to the 'sub-roles'. If 'all' is in the list (the default value) then all roles will be called.  Valid tags include ['all', 'labels', 'applications', 'instance_groups', 'settings', 'inventory', 'credentials', 'credential_types', 'notification_templates', 'users', 'teams', 'roles', 'organizations', 'projects', 'execution_environments', 'job_templates', 'workflow_job_templates', 'workflow_job_template_nodes', 'schedules'] |
| `flatten_output` | N/A | no | bool | Whether to flatten the output in single files per each object type instead of the normal exportation structure |
| `show_encrypted` | N/A | no | bool | Whether to remove the string '\$encrypted\$' in credentials output (not the actual credential value) |

## Dependencies

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

## Example Playbook

```yaml
---
- hosts: all
  connection: local
  gather_facts: false
  vars:
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
      no_log: "{{ controller_configuration_filetree_create_secure_logging | default('false') }}"
      when: controller_oauthtoken is not defined
      tags:
        - always


  roles:
    - infra.controller_configuration.filetree_create

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

This role can generate output files in two different ways:

- **Structured output**:

  The output files are distributed in separate directories, by organization first, and then by object type. Into each of these directories, one file per object is generated. This way allows to organize the files using different criteria, for example, by funcionalities or applications.

  The export can be triggered with the following command:

  ```console
  ansible-playbook -i localhost, filetree_create.yml -e '{controller_validate_certs: false, controller_hostname: localhost:8443, controller_username: admin, controller_password: password}'
  ```

  One example of this approach follows:

  ```console
  /tmp/filetree_output_distributted
  ├── current_credential_types.yaml
  ├── current_execution_environments.yaml
  ├── current_instance_groups.yaml
  ├── current_settings.yaml
  ├── Default
  │   ├── applications
  │   │   ├── 23_controller_application-app2.yaml
  │   │   └── 24_controller_application-app3.yaml
  │   ├── credentials
  │   │   ├── 82_Demo Credential.yaml
  │   │   └── 84_Demo Custom Credential.yaml
  │   ├── current_organization.yaml
  │   ├── inventories
  │   │   ├── Demo Inventory
  │   │   │   └── 81_Demo Inventory.yaml
  │   │   └── Test Inventory - Smart
  │   │       ├── 78_Test Inventory - Smart.yaml
  │   │       └── current_hosts.yaml
  │   ├── job_templates
  │   │   ├── 177_test-template-1.yaml
  │   │   └── 190_Demo Job Template.yaml
  │   ├── labels
  │   │   ├── 52_Prod.yaml
  │   │   ├── 53_differential.yaml
  │   ├── notification_templates
  │   │   ├── Email notification differential.yaml
  │   │   └── Email notification.yaml
  │   ├── projects
  │   │   ├── 169_Test Project.yaml
  │   │   ├── 170_Demo Project.yaml
  │   ├── teams
  │   │   ├── 28_satellite-qe.yaml
  │   │   └── 29_tower-team.yaml
  │   └── workflow_job_templates
  │       ├── 191_Simple workflow schema.yaml
  │       └── 200_Complicated workflow schema.yaml
  ├── ORGANIZATIONLESS
  │   ├── credentials
  │   │   ├── 2_Ansible Galaxy.yaml
  │   │   └── 3_Default Execution Environment Registry Credential.yaml
  │   └── users
  │       ├── admin.yaml
  │       ├── controller_user.yaml
  ├── schedules
  │   ├── 1_Cleanup Job Schedule.yaml
  │   ├── 2_Cleanup Activity Schedule.yaml
  │   ├── 4_Cleanup Expired Sessions.yaml
  │   ├── 52_Demo Schedule.yaml
  │   ├── 53_Demo Schedule 2.yaml
  │   └── 5_Cleanup Expired OAuth 2 Tokens.yaml
  ├── team_roles
  │   ├── current_roles_satellite-qe.yaml
  │   └── current_roles_tower-team.yaml
  └── user_roles
      └── current_roles_controller_user.yaml
  ```

- **Flatten files**:

  The output files are all located in the same directory. Each file contains a YAML list with all the objects belonging to the same object type. This output format allows to load all the objects both from the standard Ansible `group_vars` and from the `infra.controller_configuration.filetree_read` role.

  The expotation can be triggered with the following command:

  ```console
  ansible-playbook -i localhost, filetree_create.yml -e '{controller_validate_certs: false, controller_hostname: localhost:8443, controller_username: admin, controller_password: password, flatten_output: true}'
  ```

  One example of this approach follows:

  ```console
  /tmp/filetree_output_flatten
  ├── applications.yaml
  ├── credentials.yaml
  ├── current_credential_types.yaml
  ├── current_execution_environments.yaml
  ├── current_instance_groups.yaml
  ├── current_settings.yaml
  ├── groups.yaml
  ├── hosts.yaml
  ├── inventories.yaml
  ├── inventory_sources.yaml
  ├── job_templates.yaml
  ├── labels.yaml
  ├── notification_templates.yaml
  ├── organizations.yaml
  ├── projects.yaml
  ├── schedules.yaml
  ├── team_roles.yaml
  ├── teams.yaml
  ├── user_roles.yaml
  ├── users.yaml
  └── workflow_job_templates.yaml
  ```

A playbook to convert from the structured output to the flattened one is provided, and can be executed with the following command:

```console
ansible-playbook infra.controller_configuration.flatten_filetree_create_output.yaml -e '{filetree_create_output_dir: /tmp/filetree_output}'
```

## License

GPLv3+

## Author Information

- [Ivan Aragonés](https://github.com/ivarmu)
