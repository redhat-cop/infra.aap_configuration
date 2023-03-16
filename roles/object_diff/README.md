# controller_configuration.object_diff

An ansible role to manage the object diff of the AWX or Automation Controller configuration. This role leverage the controller_object_diff.py lookup plugin of the infra.controller_configuration, comparing two lists, one taken directly from the API and the other one from the git repository, and it could be used to delete objects in the AWX or Automation Controller that are not defined in the git repository list.

## Requirements

`ansible-galaxy collection install -r tests/collections/requirements.yml` to be installed. Currently: `awx.awx` or `ansible.controller` and `infra.controller_configuration`.

## Role Variables

### Organization and Environment Variables

The following Variables set the organization where should be applied the configuration, the absolute or relative of the directory structure where the variables will be stored and the life-cycle environment to use.

| Variable Name | Default Value | Required | Description |
| :------------ | :-----------: | :------: | :---------- |
| `controller_api_plugin` | `ansible.controller` | yes | Full path for the controller_api_plugin to be used. <br/> Can have two possible values: <br/>&nbsp;&nbsp;- awx.awx.controller_api             # For the community Collection version <br/>&nbsp;&nbsp;- ansible.controller.controller_api  # For the Red Hat Certified Collection version |
| `drop_user_external_accounts` | `False` | no | When is true, all users will be taken to compare with SCM configuration as code |
| `protect_not_empty_orgs` | `N/A` | no | When is true, orgs which are not empty, will not be removed |
| `query_controller_api_max_objects` | 10000 | no | Sets the maximum number of objects to be returned from the API |
<!--- | `drop_teams` | `False` | no | When is true, all teams will be taken to compare with SCM configuration as code | -->

## Role Tags

The role is designed to be used with tags, each tags correspond to an AWX or Automation Controller object to be managed by ansible.

> :warning: List of object type managed by this role: credentials, credential_types, groups, hosts, inventories, inventory_sources, job_templates, organizations, projects, teams, users, workflow_job_templates.

```bash
$ ansible-playbook object_diff.yml --list-tags
      TASK TAGS: [credentials, credential_types, groups, hosts, inventories, inventory_sources, job_templates, organizations, projects, teams, users, workflow_job_templates]

```

## IMPORTANT

To correctly manage `roles`, they can only be defined by a super-admin organization, so all the roles in the Ansible Controller instance are managed by only one organization.

## Example Playbook

```bash
---
- hosts: localhost
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
      no_log: "{{ controller_configuration_object_diff_secure_logging }}"
      when: controller_oauthtoken is not defined
      tags:
        - always

  roles:
    - role: infra.controller_configuration.filetree_read
    - role: infra.controller_configuration.object_diff
      vars:
        controller_configuration_object_diff_tasks:
          - {name: workflow_job_templates, var: controller_workflows, tags: workflow_job_templates}
          - {name: job_templates, var: controller_templates, tags: job_templates}
          - {name: user_accounts, var: controller_user_accounts, tags: users}
          - {name: groups, var: controller_groups, tags: groups}
          - {name: hosts, var: controller_hosts, tags: hosts}
          - {name: inventory_sources, var: controller_inventory_sources, tags: inventory_sources}
          - {name: inventories, var: controller_inventories, tags: inventories}
          - {name: projects, var: controller_projects, tags: projects}
          - {name: credentials, var: controller_credentials, tags: credentials}
          - {name: credential_types, var: controller_credential_types, tags: credential_types}
          - {name: organizations, var: controller_organizations, tags: organizations}
    - role: infra.controller_configuration.dispatch
      vars:
        controller_configuration_dispatcher_roles:
          - {role: workflow_job_templates, var: controller_workflows, tags: workflow_job_templates}
          - {role: job_templates, var: controller_templates, tags: job_templates}
          - {role: users, var: controller_user_accounts, tags: users}
          - {role: groups, var: controller_groups, tags: inventories}
          - {role: hosts, var: controller_hosts, tags: hosts}
          - {role: inventory_sources, var: controller_inventory_sources, tags: inventory_sources}
          - {role: inventories, var: controller_inventories, tags: inventories}
          - {role: projects, var: controller_projects, tags: projects}
          - {role: credentials, var: controller_credentials, tags: credentials}
          - {role: credential_types, var: controller_credential_types, tags: credential_types}
          - {role: organizations, var: controller_organizations, tags: organizations}

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

$ ansible-playbook drop_diff.yml --tags ${CONTROLLER_OBJECT} -e "{orgs: ${ORGANIZATION}, dir_orgs_vars: orgs_vars, env: ${ENVIRONMENT} }" --vault-password-file ./.vault_pass.txt -e @orgs_vars/env/${ENVIRONMENT}/configure_connection_controller_credentials.yml ${OTHER}
```

## License

GPLv3+

## Author Information

- [Silvio Perez](https://github.com/silvinux)

- [Ivan Aragonés](https://github.com/ivarmu)

- [Adonis García](https://github.com/adonisgarciac)

## Important things to take into account

- Issues:
  - Users and Teams must be managed by users with privileges.
  - Due to the Team Object doesn't return from API any field related to external account on Controller API, which help to filter if the teams comes from an External Source and not to be deleted by the Object Diff Ansible automation process.
