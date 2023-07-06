# Red Hat Ansible Automation Hub Configuration Collection

[![pre-commit tests](https://github.com/ansible/automation_hub_collection/actions/workflows/pre-commit.yml/badge.svg?branch=devel)](https://github.com/ansible/automation_hub_collection/actions/workflows/pre-commit.yml)
![Code style: flake8](https://img.shields.io/badge/Code%20style-flake8-orange)
<!-- Further CI badges go here as above -->

This Ansible collection allows for easy interaction with an Ansible Automation Hub or Galaxy NG server via Ansible playbooks.

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

You can install the ansible automation_hub collection with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install ansible.automation_hub
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: ansible.automation_hub
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
```

## Using this collection

Define following vars here, or in `galaxy_configs/galaxy_auth.yml`
`galaxy_server: ansible-galaxy-web-svc-test-project.example.com`

You can also specify authentication by setting the following variables:

- `galaxy_server`, `galaxy_oauthtoken`, `ah_token`

The OAuth2 token is the only method. You can obtain the token through the web interface. If you only pass a username and password to galaxy API roles/modules a new OAUTH2 token will be generated, invalidating the previous user token. To ensure this doesn't occur always set the ah_token variable to the users OAUTH2 token before executing automation. This does not affect pulp API calls.

Galaxy API calls

- group
- namespace
- publish
- repository
- repository_sync
- user

These can be specified via (from highest to lowest precedence):

- direct role variables as mentioned above

### See Also

- [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release and Upgrade Notes

For details on changes between versions, please see [the changelog for this collection](CHANGELOG.rst).

## Roadmap

Add more roles and modules for endpoints on the Automation Hub.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Automation Hub Configuration collection repository](https://github.com/ansible/automation_hub_collection).
More information about contributing can be found in our [Contribution Guidelines.](https://github.com/ansible/automation_hub_collection/blob/devel/.github/CONTRIBUTING.md)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

All content in this folder is licensed under the same license as Ansible,
which is the same as license that applied before when the base for this
code was derived form the [AWX.AWX](https://galaxy.ansible.com/awx/awx) collection.

## Documentation

Documentation for Automation hub URI can be found at
[Documentation for Automation hub URI.](https://github.com/ansible/galaxy_ng/wiki/Automating-Collection-Uploads)
