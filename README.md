# Red Hat Event Driven Ansible Controller Configuration Collection

[![pre-commit tests](https://github.com/ansible/galaxy_collection/actions/workflows/pre-commit.yml/badge.svg?branch=devel)](https://github.com/ansible/galaxy_collection/actions/workflows/pre-commit.yml)
![Code style: flake8](https://img.shields.io/badge/Code%20style-flake8-orange)
<!-- Further CI badges go here as above -->

This Ansible collection allows for easy interaction with an EDA Controller server via Ansible playbooks.

## Work In Progress

At present this collection is a work in progress and modules and roles will be added when available.

The work which will be done will be tracked in the issues. Feel free to add questions or feature requests there which can be answered or resolved once we begin work on this collection.

If you're interested in assisting with this collection please reach out to the maintainers.

## Links to Ansible Automation Platform Collections

|                                      Collection Name                                         |                 Purpose                  |
|:--------------------------------------------------------------------------------------------:|:----------------------------------------:|
| [awx.awx/Ansible.controller repo](https://github.com/ansible/awx/tree/devel/awx_collection) |   Automation Controller modules          |
|        [Ansible Hub Configuration](https://github.com/ansible/galaxy_collection)     |       Automation Hub configuration       |

## Links to other Validated Configuration Collections for Ansible Automation Platform

|                                      Collection Name                                       |                 Purpose                  |
|:------------------------------------------------------------------------------------------:|:----------------------------------------:|
| [Controller Configuration](https://github.com/redhat-cop/controller_configuration) |   Automation Controller configuration    |
| [EDA Controller Configuration](https://github.com/redhat-cop/eda_configuration) |   EDA Controller configuration    |
|             [EE Utilities](https://github.com/redhat-cop/ee_utilities)             | Execution Environment creation utilities |
|     [AAP installation Utilities](https://github.com/redhat-cop/aap_utilities)      |  Ansible Automation Platform utilities   |
|   [AAP Configuration Template](https://github.com/redhat-cop/aap_configuration_template)   |  Configuration Template for this suite   |

## Included content

Click the `Content` button to see the list of content included in this collection.

## Installing this collection

You can install the ansible EDA Controller collection with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install infra.eda_configuration
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: infra.eda_configuration
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
```

## Using this collection

You can make use of this collection by directly invoking the roles or modules using the FQCN (fully qualified collection name).

In a playbook this might look like:

```yaml
- name: Call Project role
  hosts: localhost
  roles:
    - infra.eda_configuration.projects
```

or

```yaml
- name: Call Project role
  hosts: localhost
  tasks:
    - name: Add a project
      infra.eda_configuration.project:
        name: my_project
        url: https://github.com/my/project.git
```

### See Also

- [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release and Upgrade Notes

For details on changes between versions, please see [the changelog for this collection](CHANGELOG.rst).

## Roadmap

Add more roles and modules for endpoints on the EDA Controller.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against [this repository](https://github.com/redhat-cop/eda_configuration).
More information about contributing can be found in our [Contribution Guidelines.](https://github.com/redhat-cop/eda_configuration/blob/devel/.github/CONTRIBUTING.md)

## Code of Conduct

This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
