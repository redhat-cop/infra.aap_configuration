# Red Hat Communities of Practice Controller Configuration Collection

![pre-commit tests](https://github.com/redhat-cop/controller_configuration/actions/workflows/pre-commit.yml/badge.svg)
![Galaxy Release](https://github.com/redhat-cop/controller_configuration/workflows/galaxy-release/badge.svg)
<!-- markdownlint-disable-line MD033 MD034 --><a href="https://raw.githubusercontent.com/redhat-cop/controller_configuration/devel/docs/aap_config_as_code_public_meeting.ics"><img border="0" src="https://www.google.com/calendar/images/ext/gc_button1_en-GB.gif"></a>
<!-- Further CI badges go here as above -->

This Ansible collection allows for easy interaction with an AWX or Ansible Controller server via Ansible roles using the AWX/Controller collection modules.

## Getting Help

We are on the Ansible Forums and Matrix, if you want to discuss something, ask for help, or participate in the community, please use the #infra-config-as-code tag on the fourm, or post to the chat in Matrix.

[Ansible Forums](https://forum.ansible.com/tag/infra-config-as-code)

[Matrix Chat Room](https://matrix.to/#/#aap_config_as_code:ansible.com)

## Requirements

The awx.awx or ansible.controller collections MUST be installed in order for this collection to work. It is recommended they be invoked in the playbook in the following way.

```yaml
---
- name: Playbook to configure ansible controller post installation
  hosts: localhost
  connection: local
  vars:
    controller_validate_certs: false
  collections:
    - awx.awx
```

## Links to Ansible Automation Platform Collections

|                                      Collection Name                                         |                 Purpose                  |
|:--------------------------------------------------------------------------------------------:|:----------------------------------------:|
| [awx.awx/Ansible.controller repo](https://github.com/ansible/awx/tree/devel/awx_collection) |   Automation controller modules          |
|        [Ansible Hub Configuration](https://github.com/ansible/automation_hub_collection)     |       Automation hub configuration       |

## Links to other Validated Configuration Collections for Ansible Automation Platform

|                                      Collection Name                                       |                 Purpose                  |
|:------------------------------------------------------------------------------------------:|:----------------------------------------:|
| [Controller Configuration](https://github.com/redhat-cop/controller_configuration) |   Automation controller configuration    |
|             [EE Utilities](https://github.com/redhat-cop/ee_utilities)             | Execution Environment creation utilities |
|     [AAP installation Utilities](https://github.com/redhat-cop/aap_utilities)      |  Ansible Automation Platform Utilities   |
|   [AAP Configuration Template](https://github.com/redhat-cop/aap_configuration_template)   |  Configuration Template for this suite   |

## Included content

Click the `Content` button to see the list of content included in this collection.

## Installing this collection

You can install the infra.controller_configuration.collection with the Ansible Galaxy CLI:

```console
ansible-galaxy collection install infra.controller_configuration
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: infra.controller_configuration
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
```

## Conversion from tower_configuration

If you were using a version of redhat_cop.tower_configuration, please refer to our Conversion Guide here: [Conversion Guide](docs/CONVERSION_GUIDE.md)

## Using this collection

The awx.awx or ansible.controller collection must be invoked in the playbook in order for Ansible to pick up the correct modules to use.

The following command will invoke the collection playbook. This is considered a starting point for the collection.

```console
ansible-playbook infra.controller_configuration.configure_controller.yml
```

Otherwise it will look for the modules only in your base installation. If there are errors complaining about "couldn't resolve module/action" this is the most likely cause.

```yaml
- name: Playbook to configure ansible controller post installation
  hosts: localhost
  connection: local
  vars:
    controller_validate_certs: false
  collections:
    - awx.awx
```

Define following vars here, or in `controller_configs/controller_auth.yml`
`controller_hostname: ansible-controller-web-svc-test-project.example.com`

You can also specify authentication by a combination of either:

- `controller_hostname`, `controller_username`, `controller_password`
- `controller_hostname`, `controller_oauthtoken`

The OAuth2 token is the preferred method. You can obtain the token through the preferred `controller_token` module, or through the
AWX CLI [login](https://docs.ansible.com/automation-controller/latest/html/controllerapi/authentication.html)
command.

These can be specified via (from highest to lowest precedence):

- direct role variables as mentioned above
- environment variables (most useful when running against localhost)
- a config file path specified by the `controller_config_file` parameter
- a config file at `~/.controller_cli.cfg`
- a config file at `/etc/controller/controller_cli.cfg`

Config file syntax looks like this:

```ini
[general]
host = https://localhost:8043
verify_ssl = true
oauth_token = LEdCpKVKc4znzffcpQL5vLG8oyeku6
```

Controller token module would be invoked with this code:

```yaml
    - name: Create a new token using controller username/password
      awx.awx.token:
        description: 'Creating token to test controller jobs'
        scope: "write"
        state: present
        controller_host: "{{ controller_hostname }}"
        controller_username: "{{ controller_username }}"
        controller_password: "{{ controller_password }}"

```

### Automate the Automation

Every Ansible Controller instance has it's own particularities and needs. Every administrator team has it's own practices and customs. This collection allows adaptation to every need, from small to large scale, having the objects distributed across multiple environments and leveraging Automation Webhook that can be used to link a Git repository and Ansible automation natively.

A complete example of how to use all of the roles present in the collection is available at the following [README.md](roles/filetree_create/automatetheautomation.md), where all the phases to allow CI/CD for the Controller Configuration are provided.

#### Scale at your needs

The input data can be organized in a very flexible way, letting the user use anything from a single file to an entire file tree to store the controller objects definitions, which could be used as a logical segregation of different applications, as needed in real scenarios.

### Controller Export

The awx command line can export json that is compatible with this collection.
In addition there is an awx.awx/ansible.controller export module that use the awx command line to export.
More details can be found [here](EXPORT_README.md)

There's another possible way to export the controller configuration, which is using the `filetree_create` module. It can generate output files in two different ways:

- **Structured output**:

  The output files are distributed in separate directories, by organization first, and then by object type. Into each of these directories, one file per object is generated. This way allows to organize the files using different criteria, for example, by funcionalities or applications.

  The expotation can be triggered with the following command:

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

### Template Example

A Template to use in order to start using the collections can be found [here](https://github.com/redhat-cop/aap_configuration_template)

### See Also

- [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release and Upgrade Notes

For details on changes between versions, please see [the changelog for this collection](CHANGELOG.rst).

## Releasing, Versioning and Deprecation

This collection follows [Semantic Versioning](https://semver.org/). More details on versioning can be found [in the Ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html#collection-versions).

We plan to regularly release new minor or bugfix versions once new features or bugfixes have been implemented.

Releasing the current major version happens from the `devel` branch.

## Roadmap

Adding the ability to use direct output from the awx export command in the roles along with the current data model.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Controller Configuration collection repository](https://github.com/redhat-cop/controller_configuration).
More information about contributing can be found in our [Contribution Guidelines.](https://github.com/redhat-cop/controller_configuration/blob/devel/.github/CONTRIBUTING.md)

We have a community meeting every 4 weeks. Find the agenda in the [issues](https://github.com/redhat-cop/controller_configuration/issues) and the calendar invitation below:

<!-- markdownlint-disable-next-line MD033 MD034 -->
<a target="_blank" href="https://raw.githubusercontent.com/redhat-cop/controller_configuration/devel/docs/aap_config_as_code_public_meeting.ics"><img border="0" src="https://www.google.com/calendar/images/ext/gc_button1_en-GB.gif"></a>

## Code of Conduct

This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
