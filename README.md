# Red Hat Communities of Practice AAP Configuration Collection

[![pre-commit tests](https://github.com/redhat-cop/infra.aap_configuration/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/redhat-cop/infra.aap_configuration/actions/workflows/pre-commit.yml)
[![Release - Automated](https://github.com/redhat-cop/infra.aap_configuration/actions/workflows/release_auto.yml/badge.svg)](https://github.com/redhat-cop/infra.aap_configuration/actions/workflows/release_auto.yml)
<!-- markdownlint-disable-line MD033 MD034 --><a href="https://raw.githubusercontent.com/redhat-cop/infra.aap_configuration/devel/docs/aap_config_as_code_public_meeting.ics"><img border="0" alt="Google Calendar invite" width="60" src="https://ssl.gstatic.com/calendar/images/dynamiclogo_2020q4/calendar_20_2x.png"></a>
<!-- Further CI badges go here as above -->

This Ansible collection allows for easy interaction with AAP 2.5+ via Ansible roles using the modules from the certified collections.

## Getting Help

We are on the Ansible Forums and Matrix, if you want to discuss something, ask for help, or participate in the community, please use the #infra-config-as-code tag on the form, or post to the chat in Matrix.

[Ansible Forums](https://forum.ansible.com/tag/infra-config-as-code)

[Matrix Chat Room](https://matrix.to/#/#aap_config_as_code:ansible.com)

## Requirements

The supported collections that contains the modules are required for this collection to work, you can copy this requirements.yml file example.

```yaml
---
collections:
  - name: ansible.platform
  - name: ansible.hub
  - name: ansible.controller
    version: ">=4.6.0"
  - name: ansible.eda
  - name: infra.aap_configuration
...
```

## Links to Ansible Automation Platform Collections

|                                      Collection Name                                |            Purpose            |
|:-----------------------------------------------------------------------------------:|:-----------------------------:|
| [ansible.platform repo](https://github.com/ansible/ansible.platform)                | gateway/platform modules      |
| [ansible.hub repo](https://github.com/ansible-collections/ansible_hub)              | Automation hub modules        |
| [ansible.controller repo](https://github.com/ansible/awx/tree/devel/awx_collection) | Automation controller modules |
| [ansible.eda repo](https://github.com/ansible/event-driven-ansible)                 | Event Driven Ansible modules  |

## Links to other Validated Configuration Collections for Ansible Automation Platform

|                                      Collection Name                                                  |                      Purpose                      |
|:-----------------------------------------------------------------------------------------------------:|:-------------------------------------------------:|
| [AAP Configuration Extended](https://github.com/redhat-cop/aap_configuration_extended)                | Where other useful roles that don't fit here live |
| [EE Utilities](https://github.com/redhat-cop/ee_utilities)                                            | Execution Environment creation utilities          |
| [AAP installation Utilities](https://github.com/redhat-cop/aap_utilities)                             | Ansible Automation Platform Utilities             |
| [AAP Configuration Template](https://github.com/redhat-cop/aap_configuration_template)                | Configuration Template for this suite             |
| [Ansible Validated Gitlab Workflows](https://gitlab.com/redhat-cop/infra/ansible_validated_workflows) | Gitlab CI/CD Workflows for ansible content        |
| [Ansible Validated Github Workflows](https://github.com/redhat-cop/infra.ansible_validated_workflows) | Github CI/CD Workflows for ansible content        |

## Included content

Click the `Content` button to see the list of content included in this collection.

## Installing this collection

You can install the infra.aap_configuration.collection with the Ansible Galaxy CLI:

```console
ansible-galaxy collection install infra.aap_configuration
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: infra.aap_configuration
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
```

## Conversion from controller_configuration

If you were using a version of infra.controller_configuration, please refer to our Conversion Guide here: [Conversion Guide](https://github.com/redhat-cop/infra.aap_configuration/blob/devel/docs/CONVERSION_GUIDE.md)

## Using This Collection

**Install This Collection:**
Ensure this collection (`infra.aap_configuration`) is installed:

```bash
ansible-galaxy collection install infra.aap_configuration
```

**Run Playbooks from This Collection:**
To execute a playbook packaged within this collection (e.g., `configure_aap.yml`):

```console
ansible-playbook infra.aap_configuration.configure_aap.yml
```

**Troubleshooting "couldn't resolve module/action":**
This error usually means the required Ansible collection (e.g., `infra.aap_configuration` or a dependency like ansible.controller) is:

* Not installed.
* Incorrectly named in the playbook.
* Not found in Ansible's configured collection paths.

Verify installation with `ansible-galaxy collection list` and that you have all the stated dependencies listed above in the requirements section.

Define following vars here, or in `aap_configs/controller_auth.yml`
`aap_hostname: ansible-controller-web-svc-test-project.example.com`

You can also specify authentication by a combination of either:

* `aap_hostname`, `aap_username`, `aap_password`
* `aap_hostname`, `aap_token`

The OAuth2 token is the preferred method. You can obtain the token through the preferred `controller_token` module, or through the
AWX CLI [login](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/automation_execution_api_overview/controller-api-auth-methods)
command.

These can be specified via (from highest to lowest precedence):

* direct role variables as mentioned above
* environment variables (most useful when running against localhost)
* a config file path specified by the `controller_config_file` parameter
* a config file at `~/.controller_cli.cfg`
* a config file at `/etc/controller/controller_cli.cfg`

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
      ansible.controller.token:
        description: 'Creating token to test controller jobs'
        scope: "write"
        state: present
        controller_host: "{{ aap_hostname }}"
        aap_username: "{{ aap_username }}"
        aap_password: "{{ aap_password }}"

```

### Error Handling

Many of the roles in this collection use asynchronous tasks to perform their
actions. By default the first failed asynchronous task will cause the playbook to
fail. Setting the `aap_configuration_collect_logs` variable to `true` will
enable collecting all asynchronous task failure messages and allow the playbook
to run to completion.

When `aap_configuration_collect_logs` is enabled the reported errors are
collected in a variable called `aap_configuration_role_errors`. This variable is
a dictionary where each key is the type of the configuration item that failed to
be applied. The value of each key is a list of all the failures of that type.

When the `dispatch` role is used and `aap_configuration_collect_logs` is enabled
it will display any errors encountered while applying the configurations and
fail.

Example Output when using the `dispatch` role and encoutering failures:

```yaml
fatal: [localhost]: FAILED! => {
    "msg": [
        "Errors encountered applying configurations:",
        {
            "aap_organizations_errors": [
                {
                    "ERROR_MESSAGE": "Request to /api/controller/v2/instance_groups/?name=not-real returned 0 items, expected 1",
                    "name": "Test Organization"
                },
                {
                    "ERROR_MESSAGE": "Request to /api/controller/v2/instance_groups/?name=not-real returned 0 items, expected 1",
                    "name": "Test Organization 2"
                }
            ],
            "controller_applications_errors": [
                {
                    "ERROR_MESSAGE": "Request to /api/controller/v2/organizations/?name=UnknownOrg returned 0 items, expected 1",
                    "name": "controller_application-failed-app1",
                    "organization": "UnknownOrg"
                },
                {
                    "ERROR_MESSAGE": "value of authorization_grant_type must be one of: password, authorization-code, got: password2",
                    "name": "controller_application-failed-app2",
                    "organization": "Default"
                }
            ],
        }
    ]
}
```

### Automate the Automation

Every Ansible Controller instance has it's own particularities and needs. Every administrator team has it's own practices and customs. This collection allows adaptation to every need, from small to large scale, having the objects distributed across multiple environments and leveraging Automation Webhook that can be used to link a Git repository and Ansible automation natively.

#### Scale at your needs

The input data can be organized in a very flexible way, letting the user use anything from a single file to an entire file tree to store the controller objects definitions, which could be used as a logical segregation of different applications, as needed in real scenarios.

### Controller Export

The awx command line can export json that is compatible with this collection.
In addition there is an ansible.controller export module that use the awx command line to export.
[More details can be found here](https://github.com/redhat-cop/infra.aap_configuration/blob/devel/docs/EXPORT_README.md)

### Template Example

A [Template to use in order to start using the collections can be found here](https://github.com/redhat-cop/aap_configuration_template)

### See Also

[Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release and Upgrade Notes

For details on changes between versions, please see [the changelog for this collection](https://github.com/redhat-cop/infra.aap_configuration/blob/devel/CHANGELOG.rst).

## Releasing, Versioning and Deprecation

This collection follows [Semantic Versioning](https://semver.org/). More details on versioning can be found [in the Ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html#collection-versions).

We plan to regularly release new minor or bugfix versions once new features or bugfixes have been implemented.

Releasing the current major version happens from the `devel` branch.

## Roadmap

Adding the ability to use direct output from the awx export command in the roles along with the current data model.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Controller Configuration collection repository](https://github.com/redhat-cop/aap_configuration).
More information about contributing can be found in our [Contribution Guidelines.](https://github.com/redhat-cop/aap_configuration/blob/devel/.github/CONTRIBUTING.md)

<!-- markdownlint-disable-line MD033 MD034 -->We have a community meeting every 4 weeks. Find the agenda in the [issues](https://github.com/redhat-cop/infra.aap_configuration/issues) and the calendar invitation here:<a target="_blank" href="https://raw.githubusercontent.com/redhat-cop/infra.aap_configuration/devel/docs/aap_config_as_code_public_meeting.ics"><img border="0" alt="Google Calendar invite" width="20" src="https://ssl.gstatic.com/calendar/images/dynamiclogo_2020q4/calendar_20_2x.png"></a>

## Code of Conduct

This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://github.com/redhat-cop/infra.aap_configuration/blob/devel/LICENSE) to see the full text.
