# controller_configuration.filetree_create

The role `filetree_create` is intended to be used as the first step to begin using the Configuration as Code on Ansible Tower or Ansible Automation Platform, when you already have a running instance of any of them. Obviously, you also could start to write your objects as code from scratch, but the idea behind the creation of that role is to simplify your lives and make that task a little bit easier.

## Requirements

That role requires the following:

- [awx.awx](https://docs.ansible.com/ansible/latest/collections/awx/awx/index.html) or [ansible.controller]ansible collection.

## Role Variables

The following variables are required for that role to work properly:

| Variable Name | Default Value | Required | Type | Description |
| :------------ | :-----------: | :------: | :------: | :---------- |
| `controller_api_plugin` | `ansible.controller` | yes | str | Full path for the controller_api_plugin to be used. <br/> Can have two possible values: <br/>&nbsp;&nbsp;- awx.awx.controller_api             # For the community Collection version <br/>&nbsp;&nbsp;- ansible.controller.controller_api  # For the Red Hat Certified Collection version|
| `organization_filter` | N/A | no | str | Exports only the objects belonging to the specified organization (applies to all the objects that can be assigned to an organization). |
| `organization_id` | N/A | no | int | Alternative to `organization_filter`, but specifiying the current organization's ID to filter by. Exports only the objects belonging to the specified organization (applies to all the objects that can be assigned to an organization). |
| `output_path` | `/tmp/filetree_output` | yes | str | The path to the output directory where all the generated `yaml` files with the corresponding Objects as code will be written to. |
| `input_tag` | `['all']` | no | List of Strings | The tags which are applied to the 'sub-roles'. If 'all' is in the list (the default value) then all roles will be called. |

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

## License

GPLv3+

## Author Information

- [Ivan Aragonés](https://github.com/ivarmu)
